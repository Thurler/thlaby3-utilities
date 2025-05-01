import math
from PIL import Image, ImageDraw, ImageFont

# Break item modifiers
reduce_enemy_count = False
increase_enemy_count = False
double_rare_enemy = False
triple_rare_enemy = False

# Output control
export_detailed_tile_info = False
export_probability_spreadsheet = False
export_probability_heatmap = True
enemy_for_heatmap = "Guardian Great Tree"
legend_text_color = (255, 255, 255) # white
legend_size = 100 # How many pixels the legend will take up
legend_width = 25 # How wide each legend color will be
max_legend_height = 50 # How tall each legend color can be at max
legend_padding = 10 # How much padding between legend text and color
heatmap_sin_factor = 1 # Sine exponent to take when making heatmap gradient
heatmap_colors = {
  100: (255, 0, 0), # For pure 100%
  99: (230, 100, 100), # For the intermediary values - will get hue-shifted
  0: (127, 127, 127), # For the pure 0%
}

cell_size = 15 # How large each grid cell is

grid_size = 1 # How wide the grid is between cells
grid_dim = 150 # How many columns and rows to draw
grid_color = (52, 52, 52) # 80% dark grey

border_width = 20 # How wide the grid border is
border_text_color = (0, 0, 0) # black
text_font = ImageFont.truetype("arial.ttf", 16)

img_size = grid_dim * cell_size + (grid_dim + 1)

heatmap_scale = [] # Filled with the heatmap values that will be rendered

# The heatmap color for a factor [0, 1]
def heatmap_color(factor):
  shift = (factor + 0.2) / 1.2 # Clip to 0.2 - 1 to avoid rolling back to red
  r, g, b = heatmap_colors[99]
  # Complicated maths to hueshift the color
  sinf = math.sin(2 * math.pi * (1 - shift))
  cosf = math.cos(2 * math.pi * (1 - shift))
  sq3 = (1 / 3) ** 0.5
  shift_matrix = [
    [
      cosf + (1 - cosf) / 3,
      1 / 3 * (1 - cosf) - sq3 * sinf,
      1 / 3 * (1 - cosf) + sq3 * sinf,
    ],
    [
      1 / 3 * (1 - cosf) + sq3 * sinf,
      cosf + 1 / 3 * (1 - cosf),
      1 / 3 * (1 - cosf) - sq3 * sinf,
    ],
    [
      1 / 3 * (1 - cosf) - sq3 * sinf,
      1 / 3 * (1 - cosf) + sq3 * sinf,
      cosf + 1 / 3 * (1 - cosf),
    ],
  ]
  rf, gf, bf = (
    r * shift_matrix[0][0] + g * shift_matrix[0][1] + b * shift_matrix[0][2],
    r * shift_matrix[1][0] + g * shift_matrix[1][1] + b * shift_matrix[1][2],
    r * shift_matrix[2][0] + g * shift_matrix[2][1] + b * shift_matrix[2][2],
  )
  return (
    0 if rf < 0 else 255 if rf > 255 else int (rf + 0.5),
    0 if gf < 0 else 255 if gf > 255 else int (gf + 0.5),
    0 if bf < 0 else 255 if bf > 255 else int (bf + 0.5),
  )

# An enemy spawn weight, possibly conditioned to grid positions
class EnemyWeight:
  def __init__(self, value, condition = None):
    self.value = value
    self.condition = condition if condition is not None else lambda x, y: True

# An enemy that can spawn, with its associated weights
class Enemy:
  def __init__(self, name, rare, weights):
    self.name = name
    self.rare = rare
    self.weights = weights

  def weight_at_coord(self, x, y):
    for weight in self.weights:
      if weight.condition(x, y):
        value = weight.value
        if self.rare and double_rare_enemy:
          value += weight.value
        if self.rare and triple_rare_enemy:
          value += 2 * weight.value
        return value
    return 0

# A special tile spawn check that might force an enemy's spawn
class TileProximity:
  def __init__(self, name, graphic_id, max_dist, weight):
    self.name = name
    self.graphic_id = graphic_id
    self.max_dist = max_dist
    self.weight = weight

  def value(self, distance):
    return min(1, self.weight / (100 * (distance + 1)))

# A cell that is filled in in the grid, at position (X, Y)
class Cell:
  def __init__(self, x, y, walkable, tile, decorator):
    self.walkable = walkable
    self.tile = int(tile)
    self.decorator = int(decorator)
    self.color = (255, 255, 255)
    self.x = x
    self.y = y

  def draw(self, pixels):
    if not self.walkable:
      return
    for i in range(cell_size):
      for j in range(cell_size):
        pixels[self.x + i, self.y + j] = self.color

# A floor that will be drawn in the map
class Floor:
  def __init__(self, stratum, floor, enemies, special_tiles):
    self.stratum = stratum
    self.floor = floor
    self.fileprefix = './data/'
    self.fileprefix += str(stratum) if stratum > 9 else ('0' + str(stratum))
    self.fileprefix += '0' + str(floor) + '_'
    self.enemies = enemies
    self.special_tiles = special_tiles
    self.init_grid()

  def init_grid(self):
    self.grid = []
    # Keep track of min/max for x/y coords so we can crop the map later
    minx = 149
    maxx = 0
    miny = 149
    maxy = 0
    with open(self.fileprefix + "OD.txt", "rb") as walkable_data:
      with open(self.fileprefix + "H.txt", 'r') as hidden_data:
        with open(self.fileprefix + "G.txt", 'r') as tile_data:
          with open(self.fileprefix + "M.txt", 'r') as decorator_data:
            for row in range(grid_dim):
              self.grid.append([])
              y = (cell_size + grid_size) * row
              hidden_line = hidden_data.readline().split(',')[:-1]
              tile_line = tile_data.readline().split(',')[:-1]
              decorator_line = decorator_data.readline().split(',')[:-1]
              for col in range(grid_dim):
                self.grid[row].append(None)
                x = (cell_size + grid_size) * col
                # Check if cell is walkable (1 = visible, 2 = walkable)
                walkable = walkable_data.read(1)[0] == 2
                # Check if cell is a hidden path (0 = not hidden)
                hidden = hidden_line[col] != '0'
                # Check if cell has a tile associated (0 = not visible)
                has_tile = tile_line[col] != '0'
                # Check if cell has a decorator associated (0 = not visible)
                has_decorator = decorator_line[col] != '0'
                if walkable or hidden or has_tile or has_decorator:
                  # Make the cell and add it to the grid
                  self.grid[row][col] = self.make_cell(
                    row, col, x, y,
                    walkable or hidden,
                    tile_line[col],
                    decorator_line[col],
                  )
                  # Update the boundaries for later cropping, but only if
                  # walkable or hidden
                  if walkable or hidden:
                    if col < minx:
                      minx = col
                    if col > maxx:
                      maxx = col
                    if row < miny:
                      miny = row
                    if row > maxy:
                      maxy = row
    self.boundaries = (minx, maxx, miny, maxy)

  def make_cell(self, row, col, x, y, walkable, tile, decorator):
    return Cell(x + grid_size, y + grid_size, walkable, tile, decorator)

  def enemy_count_probabilities(self):
    # Basic logic found from game - calculate ranges and evenly distribute odds
    lower = 1 if self.floor < 4 else 2
    upper = min(5, self.floor + 2)
    probs = {}
    for i in range(lower, upper + 1):
      probs[i] = 1 / (upper - lower + 1)
    # Break item logic - lowering enemy count shifts values down
    if reduce_enemy_count and not increase_enemy_count:
      # If the lower bound was above 1, we just cancel the highest value and
      # make it lower - 1, otherwise we stack the max value's prob into 1's
      if lower > 1:
        probs[lower - 1] = probs[upper]
        del probs[upper]
      else:
        probs[1] += probs[upper]
        del probs[upper]
    # Break item logic - increasing enemy count shifts values up
    if increase_enemy_count and not reduce_enemy_count:
      # If the upper bound was below 5, we just cancel the lowest value and
      # make it upper + 1, otherwise we stack the min value's prob into 5's
      if upper < 5:
        probs[upper + 1] = probs[lower]
        del probs[lower]
      else:
        probs[5] += probs[lower]
        del probs[lower]
    return probs

  def proximity_spawn_probabilities(self, row, col):
    cells_to_check = [
      # Distance 0
      (self.grid[row][col], 0),
      # Distance 1
      (self.grid[row][col + 1], 1),
      (self.grid[row][col - 1], 1),
      (self.grid[row + 1][col], 1),
      (self.grid[row - 1][col], 1),
      # Distance 2
      (self.grid[row][col + 2], 2),
      (self.grid[row][col - 2], 2),
      (self.grid[row + 2][col], 2),
      (self.grid[row - 2][col], 2),
      (self.grid[row + 1][col + 1], 2),
      (self.grid[row - 1][col - 1], 2),
      (self.grid[row - 1][col + 1], 2),
      (self.grid[row + 1][col - 1], 2),
      # Distance 3
      (self.grid[row][col + 3], 3),
      (self.grid[row][col - 3], 3),
      (self.grid[row + 3][col], 3),
      (self.grid[row - 3][col], 3),
      (self.grid[row + 1][col + 2], 3),
      (self.grid[row - 1][col - 2], 3),
      (self.grid[row + 2][col + 1], 3),
      (self.grid[row - 2][col - 1], 3),
      (self.grid[row - 1][col + 2], 3),
      (self.grid[row + 1][col - 2], 3),
      (self.grid[row + 2][col - 1], 3),
      (self.grid[row - 2][col + 1], 3),
    ]
    prob_checks = []
    # For each of the 25 vicinity cells, check if it matches a special tile,
    # and add that data to the probability checks that will be returned
    for cell, distance in cells_to_check:
      if cell is None:
        continue
      for tile in self.special_tiles:
        graphic_match = (
          cell.tile == tile.graphic_id or
          cell.decorator == tile.graphic_id
        )
        if graphic_match and distance <= tile.max_dist:
          prob_checks += [(tile.name, tile.value(distance))]
    return prob_checks

  def global_enemy_probabilities(self, row, col):
    # First we add up all the available weights for this tile
    weight_sum = 0
    for enemy in self.enemies:
      weight_sum += enemy.weight_at_coord(col, row)
    # Then we divide each individual weight by the sum, to get individual
    # probabilities
    probs = {}
    if weight_sum == 0:
      return probs
    for enemy in self.enemies:
      probs[enemy.name] = enemy.weight_at_coord(col, row) / weight_sum
    return probs

  def compute_encounters(
    self, remaining, base_prob, proximity, weights, spawned,
  ):
    # If there are no remaining slots, there is nothing to do, so just return
    if remaining == 0:
      return [(spawned, base_prob)]
    # If we have remaining proximity checks, we perform those
    if len(proximity) > 0:
      check_name, check_prob = proximity[0]
      # Success spawns an enemy, so it reduces the remaining slots by 1
      success_result = self.compute_encounters(
        remaining - 1,
        base_prob * check_prob,
        proximity[1:],
        weights,
        spawned + [check_name],
      )
      # Failure does not, so it keeps the remaining slots
      failure_result = self.compute_encounters(
        remaining,
        base_prob * (1 - check_prob),
        proximity[1:],
        weights,
        spawned,
      )
      # We simply return the possible outcomes from either branch
      return success_result + failure_result
    # Otherwise, we just follow the global weights - we iterate on each
    # outcome recursively, following the same logic as we did for proximity's
    # boolean check
    results = []
    for name, probability in weights.items():
      if probability == 0:
        continue
      results += self.compute_encounters(
        remaining - 1,
        base_prob * probability,
        proximity,
        weights,
        spawned + [name],
      )
    return results

  def compute_odds(self, export_txt, export_csv):
    text_file = open("encounter_data.txt", 'w') if export_txt else None
    csv_expected = open("encounter_expected.csv", 'w') if export_csv else None
    csv_prob = open("encounter_probability.csv", 'w') if export_csv else None
    heatmap_values = []
    # Enemy counts are global for the floor
    enemy_counts = self.enemy_count_probabilities()
    if export_txt:
      text_file.write("Enemy count probability distribution:\n\n")
      for count, probability in enemy_counts.items():
        enemy_text = "enemies" if count > 1 else "enemy"
        probability = round(probability * 100, 2)
        text_file.write(f"- {count} {enemy_text}: {probability}%\n")
      text_file.write('\n')
    enemy_names = [e.name for e in self.enemies]
    if export_csv:
      csv_expected.write(f"X,Y,{','.join(enemy_names)}\n")
      csv_prob.write(f"X,Y,{','.join(enemy_names)}\n")
    # When iterating, we skip the first and last 2 rows/cols to avoid dealing
    # with missing squares for tile logic - the game doesn't use valid data in
    # those tiles anyway and is likely to crash, so why bother
    for row in range(2, grid_dim - 2):
      print(f"Row {row}...")
      for col in range(2, grid_dim - 2):
        cell = self.grid[row][col]
        # We only care about cells the player can step on
        if cell is None or not cell.walkable:
          continue
        if export_txt:
          text_file.write(f"=== Tile ({col}, {row}) ===\n\n")
        # Check for proximity special tiles that prioritize enemy spawns
        proximity_checks = self.proximity_spawn_probabilities(row, col)
        if export_txt:
          if len(proximity_checks) > 0:
            text_file.write("Proximity tile checks:\n\n")
            for name, probability in proximity_checks:
              text_file.write(f"- {name}: {round(probability * 100, 2)}%\n")
            text_file.write('\n')
          else:
            text_file.write("No tile checks to be performed\n\n")
        # Global weights set what happens to remainder slots
        enemy_weights = self.global_enemy_probabilities(row, col)
        if export_txt:
          text_file.write("Global spawn probabilities:\n\n")
          for enemy, probability in enemy_weights.items():
            probability = round(probability * 100, 2)
            text_file.write(f"- {enemy}: {probability}%\n")
          text_file.write('\n')
        # Now we simulate enemy spawns to brute force all possible battle
        # encounters and their probabilities
        possible_battles = []
        for count, count_prob in enemy_counts.items():
          possible_battles += self.compute_encounters(
            count, count_prob, proximity_checks, enemy_weights, [],
          )
        # We iterate over the possible battles, adding up probabilities for each
        # enemy to figure the expected number and probability of at least one
        expected = {}
        spawn_probability = {}
        for name in enemy_names:
          expected[name] = 0
          spawn_probability[name] = 0
          for battle in possible_battles:
            spawns, probability = battle
            expected[name] += spawns.count(name) * probability
            if name in spawns:
              spawn_probability[name] += probability
          if export_probability_heatmap and name == enemy_for_heatmap:
            # Save the final probability as a heatmap value for these coords
            final_probability = spawn_probability[name]
            heatmap_values.append((row, col, final_probability))
        # Export the text data in both txt and csv formats
        if export_txt:
          text_file.write("Final spawn probabilities:\n\n")
          for name in enemy_names:
            if expected[name] == 0:
              continue
            expected_count = round(expected[name], 4)
            prob = round(spawn_probability[name] * 100, 2)
            text_file.write(
              f"- {name}: Expected {expected_count}, at least one: {prob}%\n",
            )
          text_file.write('\n')
        if export_csv:
          # Write the resulting expected count in its own csv file
          csv_expected.write(f"{col},{row},")
          expecteds = [str(round(expected[name], 4)) for name in enemy_names]
          csv_expected.write(','.join(expecteds))
          csv_expected.write('\n')
          # Write the resulting probability to spawn in its own csv file
          csv_prob.write(f"{col},{row},")
          probs = [spawn_probability[name] for name in enemy_names]
          probs = [f"{round(prob * 100, 2)}%" for prob in probs]
          csv_prob.write(','.join(probs))
          csv_prob.write('\n')
    # Close the text files so they can be flushed to disk
    if export_txt:
      text_file.close()
    if export_csv:
      csv_expected.close()
      csv_prob.close()
    # Lastly, we update each cell's color with the expected probability for
    # the heatmap enemy, based on the possible probabilities
    if export_probability_heatmap:
      # We first need to know if any tile has 100% spawn and what the non-zero
      # min value and non-100 max value are; also the list of possible values
      has_hundred = False
      max_prob = 0
      min_prob = 1
      for value in heatmap_values:
        _, _, probability = value
        if probability <= 0.000001 or probability >= 0.999999:
          continue
        if probability > max_prob:
          max_prob = probability
        if probability < min_prob:
          min_prob = probability
        if probability not in heatmap_scale:
          heatmap_scale.append(probability)
      # Now we iterate again, computing the gradient and setting the colors:
      for value in heatmap_values:
        row, col, probability = value
        color = None
        if probability >= 0.999999:
          color = heatmap_colors[100]
        elif probability <= 0.000001:
          color = heatmap_colors[0]
        else:
          factor = (probability - min_prob) / (max_prob - min_prob)
          color = heatmap_color(factor)
        self.grid[row][col].color = color

  def draw(self, image, pixels):
    # Draw the base grid and cells
    for row in range(grid_dim):
      y = (cell_size + grid_size) * row
      # Draw the top part of the grid
      self.draw_grid_row(y)
      # Draw the cells in this row
      for col in range(grid_dim):
        x = (cell_size + grid_size) * col
        # Left grid - offset Y by grid_size since we already drew top grid
        self.draw_grid_col(x, y + grid_size)
        # Draw the cell, if available
        if self.grid[row][col] is not None:
          self.grid[row][col].draw(pixels)
      # Draw the remaining right grid
      x = (cell_size + grid_size) * 150
      self.draw_grid_col(x, y + grid_size)
    # Draw the remaining bottom grid
    y = (cell_size + grid_size) * 150
    self.draw_grid_row(y)

  def draw_grid_row(self, y):
    for x in range(img_size):
      for g in range(grid_size):
        pixels[x, y + g] = grid_color

  def draw_grid_col(self, x, y):
    for c in range(cell_size):
      for g in range(grid_size):
        pixels[x + g, y + c] = grid_color

# Helper class because python is stupid and can't do static members properly
class BoundaryCheck:
  # Oblivion 1F starting area
  def o1_start_area_check(x, y):
    if x > 83:
      return True
    if x > 71 and x < 84 and y > 47 and y < 76:
      return True
    return False

  # And its inverse
  def o1_start_area_check_inv(x, y):
    return not BoundaryCheck.o1_start_area_check(x, y)

  # Oblivion 1F starting area plus the extra fairy check
  def o1_fairy_check(x, y):
    return BoundaryCheck.o1_start_area_check(x, y) and x < 87 and y > 55

# These classes literally just hold the enemies and special tiles for each floor
class Oblivion1F(Floor):
  enemies = [
    Enemy(
      "Weakling Kedama", False, [
        EnemyWeight(100, BoundaryCheck.o1_start_area_check),
      ],
    ),
    Enemy(
      "Seed of Forgetfulness", False, [
        EnemyWeight(75, BoundaryCheck.o1_start_area_check),
        EnemyWeight(80, BoundaryCheck.o1_start_area_check_inv),
      ],
    ),
    Enemy(
      "Giant Walnut-Cracking Squirrel", False, [
        EnemyWeight(50, BoundaryCheck.o1_start_area_check),
        EnemyWeight(100, BoundaryCheck.o1_start_area_check_inv),
      ],
    ),
    Enemy(
      "Forest Flower Fairy", False, [
        EnemyWeight(66, BoundaryCheck.o1_fairy_check),
        EnemyWeight(100, BoundaryCheck.o1_start_area_check_inv),
      ],
    ),
    Enemy(
      "Fairytale Flower Girl", False, [
        EnemyWeight(80, BoundaryCheck.o1_start_area_check_inv),
      ],
    ),
    Enemy(
      "Sea of Trees Kedama", False, [
        EnemyWeight(50, BoundaryCheck.o1_start_area_check_inv),
      ],
    ),
    Enemy(
      "Golden Seed", True, [
        EnemyWeight(5, BoundaryCheck.o1_start_area_check_inv),
      ],
    ),
  ]
  tiles = [
    TileProximity("Seed of Forgetfulness", 4, 2, 100),
    TileProximity("Forest Flower Fairy", 5, 1, 200),
    TileProximity("Giant Walnut-Cracking Squirrel", 8, 0, 100),
    TileProximity("Fairytale Flower Girl", 9, 0, 100),
    TileProximity("Giant Walnut-Cracking Squirrel", 10, 1, 100),
    TileProximity("Juvenile Great Tree", 11, 1, 200),
    TileProximity("Storybook Assassin Girl", 12, 2, 50),
    TileProximity("Juvenile Great Tree", 13, 1, 100),
    TileProximity("Juvenile Great Tree", 14, 0, 100),
    TileProximity("Guardian Great Tree", 15, 3, 50),
    TileProximity("Fairytale Man-Eating Wolf", 16, 1, 200),
    TileProximity("Gluttonous Memorytrap", 18, 1, 200),
    TileProximity("Gluttonous Memorytrap", 19, 1, 200),
    TileProximity("Gluttonous Memorytrap", 20, 0, 100),
    TileProximity("Golden Seed", 23, 3, 100),
    TileProximity("Storybook Assassin Girl", 24, 2, 50),
  ]

  def __init__(self):
    super().__init__(1, 1, self.enemies, self.tiles)

class Oblivion2F(Floor):
  enemies = [
    Enemy("Seed of Forgetfulness", False, [EnemyWeight(0)]),
    Enemy("Giant Walnut-Cracking Squirrel", False, [EnemyWeight(0)]),
    Enemy("Forest Flower Fairy", False, [EnemyWeight(80)]),
    Enemy("Fairytale Flower Girl", False, [EnemyWeight(100)]),
    Enemy("Sea of Trees Kedama", False, [EnemyWeight(100)]),
    Enemy("Nightmare Chrysalis", False, [EnemyWeight(100)]),
    Enemy("Juvenile Great Tree", False, [EnemyWeight(40)]),
    Enemy("Fairytale Man-Eating Wolf", False, [EnemyWeight(0)]),
    Enemy("Golden Seed", True, [EnemyWeight(3)]),
    Enemy("Giant Gold-Cracking Squirrel", True, [EnemyWeight(3)]),
    Enemy("Storybook Assassin Girl", True, [EnemyWeight(3)]),
    Enemy("Guardian Great Tree", True, [EnemyWeight(0)]),
  ]
  tiles = [
    TileProximity("Seed of Forgetfulness", 4, 2, 100),
    TileProximity("Forest Flower Fairy", 5, 1, 200),
    TileProximity("Fairytale Man-Eating Wolf", 7, 1, 100),
    TileProximity("Giant Walnut-Cracking Squirrel", 8, 0, 100),
    TileProximity("Fairytale Flower Girl", 9, 0, 100),
    TileProximity("Giant Walnut-Cracking Squirrel", 10, 1, 100),
    TileProximity("Juvenile Great Tree", 11, 1, 200),
    TileProximity("Storybook Assassin Girl", 12, 2, 50),
    TileProximity("Juvenile Great Tree", 13, 1, 100),
    TileProximity("Juvenile Great Tree", 14, 0, 100),
    TileProximity("Guardian Great Tree", 15, 3, 50),
    TileProximity("Fairytale Man-Eating Wolf", 16, 1, 200),
    TileProximity("Gluttonous Memorytrap", 18, 1, 200),
    TileProximity("Gluttonous Memorytrap", 19, 1, 200),
    TileProximity("Gluttonous Memorytrap", 20, 0, 100),
    TileProximity("Golden Seed", 23, 3, 100),
    TileProximity("Storybook Assassin Girl", 24, 2, 50),
  ]

  def __init__(self):
    super().__init__(1, 2, self.enemies, self.tiles)

class Oblivion3F(Floor):
  enemies = []
  tiles = []

  def __init__(self):
    super().__init__(1, 3, self.enemies, self.tiles)

class DreamPath1F(Floor):
  enemies = []
  tiles = []

  def __init__(self):
    super().__init__(2, 1, self.enemies, self.tiles)

class DreamPath2F(Floor):
  enemies = []
  tiles = []

  def __init__(self):
    super().__init__(2, 2, self.enemies, self.tiles)

# Instantiate floor data for analysis
# floor = Oblivion1F()
floor = Oblivion2F()
# floor = Oblivion3F()
# floor = DreamPath1F()
# floor = DreamPath2F()

# Compute probabilities and export data as requested
floor.compute_odds(export_detailed_tile_info, export_probability_spreadsheet)

if not export_probability_heatmap:
  exit()

# Make a 150x150 canvas so we can fill out the grid
map_img = Image.new("RGBA", (img_size, img_size), "black")
pixels = map_img.load()

# Actually draw the grid and cells
floor.draw(map_img, pixels)

# Figure out the crop coordinates - we want a multiple of 5 on x/y axis, and
# for the map to be centered in the final crop
bounds = floor.boundaries
width = bounds[1] - bounds[0] + 3 # +1 to get count, add 1 padding on each side
height = bounds[3] - bounds[2] + 3 # +1 to get count, add 1 padding on each side
# Group tiles in groups of 5
groupsx = math.ceil(width / 5)
groupsy = math.ceil(height / 5)
# Compute differences in expected width/height with actual width/height
diffx = (groupsx * 5) - width
diffy = (groupsy * 5) - height
# Find the crop positions based on the data above, centering the crop
offsetx = diffx // 2
offsety = diffy // 2
left = bounds[0] - 1 - offsetx
top = bounds[2] - 1 - offsety

# Perform the crop based on the topleft corner and amount of x/y groups
map_img = map_img.crop((
  left * (cell_size + grid_size),
  top * (cell_size + grid_size),
  (left + (5 * groupsx)) * (cell_size + grid_size) + grid_size,
  (top + (5 * groupsy)) * (cell_size + grid_size) + grid_size,
))

# Make a new image with a white canvas to have the coordinate border
border_img = Image.new(
  "RGBA",
  (map_img.size[0] + (border_width * 2), map_img.size[1] + (border_width * 2)),
  "white",
)
pixels = border_img.load()
draw = ImageDraw.Draw(border_img)
labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def draw_vertical_divisor(pixels, draw, xcount, text=True):
  # Horizontal groups use number, start at 1
  label = str(xcount + 1)
  # Compute x offset and draw the grid
  x = border_width + (xcount * 5 * (cell_size + grid_size))
  for g in range(grid_size):
    for h in range(border_width):
      pixels[x + g, h] = border_text_color
      pixels[x + g, border_img.size[1] - h - 1] = border_text_color
  # If drawing text, make sure it's centered
  if text:
    W, H = ((cell_size + grid_size) * 5, border_width)
    _, _, w, h = draw.textbbox((0, 0), label, font=text_font)
    # Top row
    draw.text(
      (x + ((W - w) / 2), (H - h) / 2),
      label,
      fill=border_text_color,
      font=text_font,
    )
    # Bottom row
    draw.text(
      (x + ((W - w) / 2), border_img.size[1] - border_width + ((H - h) / 2)),
      label,
      fill=border_text_color,
      font=text_font,
    )

def draw_horizontal_divisor(pixels, draw, ycount, text=True):
  # Vertical groups use letters, start at A
  label = labels[ycount]
  # Compute y offset and draw the grid
  y = border_width + (ycount * 5 * (cell_size + grid_size))
  for g in range(grid_size):
    for h in range(border_width):
      pixels[h, y + g] = border_text_color
      pixels[border_img.size[0] - h - 1, y + g] = border_text_color
  # If drawing text, make sure it's centered
  if text:
    W, H = (border_width, (cell_size + grid_size) * 5)
    _, _, w, h = draw.textbbox((0, 0), label, font=text_font)
    # Left column
    draw.text(
      ((W - w) / 2, y + ((H - h) / 2)),
      label,
      fill=border_text_color,
      font=text_font,
    )
    # Right column
    draw.text(
      (border_img.size[0] - border_width + ((W - w) / 2), y + ((H - h) / 2)),
      label,
      fill=border_text_color,
      font=text_font,
    )

# Draw the horizontal groups
for i in range(groupsx):
  draw_vertical_divisor(pixels, draw, i)
# Last stroke has no text associated with it
draw_vertical_divisor(pixels, draw, groupsx, False)

# Draw the vertical groups
for i in range(groupsy):
  draw_horizontal_divisor(pixels, draw, i)
# Last stroke has no text associated with it
draw_horizontal_divisor(pixels, draw, groupsy, False)

# Paste the original map in this new image
border_img.paste(map_img, (border_width, border_width))

# Make a new image with a black canvas to have the heatmap scale
heatmap_x = border_img.size[0] + (legend_padding // 2)
final_height = border_img.size[1]
final_img = Image.new(
  "RGBA",
  (border_img.size[0] + legend_size, final_height),
  "black",
)
pixels = final_img.load()
draw = ImageDraw.Draw(final_img)

# Sort the values and collapse neighbor percents to the same color
heatmap_scale.sort(reverse=True)
legend_colors = {}
ordered_colors = []
for value in heatmap_scale:
  # The last element will be the smallest after the reverse sort
  factor = (value - heatmap_scale[-1]) / (heatmap_scale[0] - heatmap_scale[-1])
  color = heatmap_color(factor)
  if color not in ordered_colors:
    ordered_colors.append(color)
    legend_colors[color] = []
  legend_colors[color].append(value)

# Figure out how big each legend step is going to be - cap at 50px
step_size = int(
  min(max_legend_height, final_height / (len(ordered_colors) + 2))
)
# The remainder will be used as padding - odd pixel count will be added to grey
remainder = final_height - (step_size * (len(ordered_colors) + 2))
vpadding = remainder // 2
vextra = remainder % 2

# Draws text next to the color, centered around the height of the color
def draw_legend_text(size, offset_y, value):
  rounded = round(value * 100, 2)
  rounded = 99.99 if value < 0.999999 and rounded >= 100 else rounded
  text = f"{rounded}%"
  _, _, _, h_value = draw.textbbox((0, 0), text, font=text_font)
  h_text = (size - h_value) / 2
  draw.text(
    (heatmap_x + legend_width + legend_padding, offset_y + h_text),
    text,
    fill=legend_text_color,
    font=text_font,
  )

# Draw the hardcoded heatmap values for 100% and 0%
for i in range(legend_width):
  for j in range(step_size):
    pixels[heatmap_x + i, vpadding + j] = heatmap_colors[100]
  for j in range(step_size + vextra):
    color = heatmap_colors[0]
    pixels[heatmap_x + i, final_height - vpadding - vextra - j] = color
draw_legend_text(step_size, vpadding, 1)
draw_legend_text(
  step_size + vextra, vpadding + ((len(ordered_colors) + 1) * step_size), 0,
)

# Draw the remaining heatmap values, in order
for c, color in enumerate(ordered_colors):
  offset_y = vpadding + ((c + 1) * step_size)
  for i in range(legend_width):
    for j in range(step_size):
      pixels[heatmap_x + i, offset_y + j] = color
  # For the text, we always take the highest % value in that color threshold,
  # unless it's the final step, in which case we use the lowest one
  values = sorted(legend_colors[color], reverse=True)
  value = values[0] if c < (len(ordered_colors) - 1) else values[-1]
  draw_legend_text(step_size, offset_y, value)

# Paste the original map in this new image
final_img.paste(border_img, (0, 0))

# Render the final product
final_img.show()
final_img.save("out.png")
