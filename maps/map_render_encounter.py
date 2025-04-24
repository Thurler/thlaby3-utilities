import math
from PIL import Image, ImageDraw, ImageFont

# Break item modifiers
reduce_enemy_count = False
increase_enemy_count = False
double_rare_enemy = False
triple_rare_enemy = False

# Output control
export_detailed_tile_info = True
export_probability_spreadsheet = True
export_probability_heatmap = False
enemy_for_heatmap = ""

cell_size = 15 # How large each grid cell is

grid_size = 1 # How wide the grid is between cells
grid_dim = 150 # How many columns and rows to draw
grid_color = (52, 52, 52) # 80% dark grey

border_width = 20 # How wide the grid border is
border_text_color = (0, 0, 0) # black
text_font = ImageFont.truetype("arial.ttf", 16)

img_size = grid_dim * cell_size + (grid_dim + 1)

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
    return self.weight / (distance + 1)

# A cell that is filled in in the grid, at position (X, Y)
class Cell:
  def __init__(self, x, y, walkable, tile, decorator):
    self.walkable = walkable
    self.tile = int(tile)
    self.decorator = int(decorator)
    self.x = x
    self.y = y

  def draw(self, pixels):
    if not self.walkable:
      return
    color = (255, 255, 255)
    for i in range(cell_size):
      for j in range(cell_size):
        pixels[self.x + i, self.y + j] = color

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
      (self.grid[row][col + 2], 2),
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
      weight_sum += enemy.weight_at_coord(row, col)
    # Then we divide each individual weight by the sum, to get individual
    # probabilities
    probs = {}
    if weight_sum == 0:
      return probs
    for enemy in self.enemies:
      probs[enemy.name] = enemy.weight_at_coord(row, col) / weight_sum
    return probs

  def compute_spread(self, remaining, base_prob, proximity, weights):
    # If there are no remaining slots, there is nothing to do, so just return
    if remaining == 0:
      return {}
    # If we have remaining proximity checks, we perform those
    if len(proximity) > 0:
      # Proximity probability comes as percentage, so we divide by 100
      check_name, check_prob = proximity[0][0], (proximity[0][1] / 100)
      # Success spawns an enemy, so it reduces the remaining slots by 1
      success_result = self.compute_spread(
        remaining - 1, base_prob * check_prob, proximity[1:], weights,
      )
      # Failure does not, so it keeps the remaining slots
      failure_result = self.compute_spread(
        remaining, base_prob * (1 - check_prob), proximity[1:], weights,
      )
      # We add the compunded probability to the success result, as it spawned
      # the enemy
      if check_name not in success_result:
        success_result[check_name] = 0
      success_result[check_name] += base_prob * check_prob
      # And finally merge the results to return them
      for name, probability in failure_result.items():
        if name not in success_result:
          success_result[name] = 0
        success_result[name] += probability
      return success_result
    # Otherwise, we just follow the global weights - we iterate on each
    # outcome recursively, following the same logic as we did for proximity's
    # boolean check
    results = []
    for name, probability in weights.items():
      result = self.compute_spread(
        remaining - 1, base_prob * probability, proximity, weights,
      )
      # We add the compunded probability to the success result, as it spawned
      # the enemy
      if name not in result:
        result[name] = 0
      result[name] += base_prob * probability
      results.append(result)
    # And finally, we merge the independent and mutually exclusive results to
    # get the final spread
    spread = {}
    for result in results:
      for name, probability in result.items():
        if name not in spread:
          spread[name] = 0
        spread[name] += probability
    return spread

  def compute_odds(self, export_txt, export_csv):
    text_file = open("encounter_data.txt", 'w') if export_txt else None
    csv_file = open("encounter_data.csv", 'w') if export_csv else None
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
      csv_file.write(f"X,Y,{','.join(enemy_names)}\n")
    # When iterating, we skip the first and last 2 rows/cols to avoid dealing
    # with missing squares for tile logic - the game doesn't use valid data in
    # those tiles anyway and is likely to crash, so why bother
    for row in range(2, grid_dim - 2):
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
              text_file.write(f"- {name}: {round(probability, 2)}%\n")
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
        # Now comes the fun part - compounding the probabilities and adding
        # them up as we go through them
        result = {}
        for count, count_prob in enemy_counts.items():
          probability_spread = self.compute_spread(
            count, count_prob, proximity_checks, enemy_weights,
          )
          for name, probability in probability_spread.items():
            if name not in result:
              result[name] = 0
            result[name] += probability
        if export_txt:
          text_file.write("Final spawn probabilities:\n\n")
          for enemy, probability in result.items():
            if probability == 0:
              continue
            probability = round(probability * 100, 2)
            text_file.write(f"- {enemy}: {probability}%\n")
          text_file.write('\n')
        if export_csv:
          csv_file.write(f"{col},{row},")
          values = [result[n] if n in result else 0 for n in enemy_names]
          values = [f"{round(value * 100, 2)}%" for value in values]
          csv_file.write(','.join(values))
          csv_file.write('\n')
    if export_txt:
      text_file.close()
    if export_csv:
      csv_file.close()

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
    Enemy("Fairytale Man-Eating Wolf", False, [EnemyWeight(0)]),
    Enemy(
      "Golden Seed", True, [
        EnemyWeight(5, BoundaryCheck.o1_start_area_check_inv),
      ],
    ),
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
    super().__init__(1, 1, self.enemies, self.tiles)

class Oblivion2F(Floor):
  enemies = []
  tiles = []

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
floor = Oblivion1F()
# floor = Oblivion2F()
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
final_img = Image.new(
  "RGBA",
  (map_img.size[0] + (border_width * 2), map_img.size[1] + (border_width * 2)),
  "white",
)
pixels = final_img.load()
draw = ImageDraw.Draw(final_img)
labels = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def draw_vertical_divisor(pixels, draw, xcount, text=True):
  # Horizontal groups use number, start at 1
  label = str(xcount + 1)
  # Compute x offset and draw the grid
  x = border_width + (xcount * 5 * (cell_size + grid_size))
  for g in range(grid_size):
    for h in range(border_width):
      pixels[x + g, h] = border_text_color
      pixels[x + g, final_img.size[1] - h - 1] = border_text_color
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
      (x + ((W - w) / 2), final_img.size[1] - border_width + ((H - h) / 2)),
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
      pixels[final_img.size[0] - h - 1, y + g] = border_text_color
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
      (final_img.size[0] - border_width + ((W - w) / 2), y + ((H - h) / 2)),
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
final_img.paste(map_img, (border_width, border_width))

# Render the final product
final_img.show()
final_img.save("out.png")
