import math
from PIL import Image, ImageDraw, ImageFont

cell_size = 15 # How large each grid cell is
icon_size = 3 * cell_size # How large each icon is

grid_size = 1 # How wide the grid is between cells
grid_dim = 150 # How many columns and rows to draw
grid_color = (52, 52, 52) # 80% dark grey

draw_paths = False # Whether warp paths will be rendered or not
path_color = (0, 69, 255) # blue

border_width = 20 # How wide the grid border is
border_text_color = (0, 0, 0) # black
text_font = ImageFont.truetype("arial.ttf", 16)

img_size = grid_dim * cell_size + (grid_dim + 1)

# A cell that is filled in in the grid, at position (X, Y)
class Cell:
  def __init__(self, x, y, hidden, color_override = None):
    self.color_override = color_override
    self.hidden = hidden
    self.x = x
    self.y = y

  def draw(self, pixels):
    color = (255, 255, 255)
    # Override color if specified
    if self.color_override is not None:
      color = self.color_override
    # Use a pink shade when path is hidden, even if override applies
    if self.hidden:
      color = (255, 169, 255)
    for i in range(cell_size):
      for j in range(cell_size):
        pixels[self.x + i, self.y + j] = color

  def draw_icon(self, image):
    pass

  def draw_path(self, grid, imagedraw):
    pass

# A cell that houses an icon
class IconCell(Cell):
  def __init__(self, x, y, icon, size):
    super().__init__(x, y, False)
    self.icon = icon
    self.icon.thumbnail(size)
    self.shift_x = (self.icon.size[0] - (cell_size, cell_size)[0]) // 2
    self.shift_y = (self.icon.size[1] - (cell_size, cell_size)[1]) // 2

  def draw_icon(self, image):
    image.paste(
      self.icon,
      (self.x - self.shift_x, self.y - self.shift_y),
      self.icon,
    )

class PathCell(IconCell):
  def __init__(self, x, y, icon, size, dstx, dsty):
    super().__init__(x, y, icon, size)
    self.dstx = dstx
    self.dsty = dsty

  def draw_path(self, grid, imagedraw):
    target = grid[self.dsty][self.dstx]
    offset = math.ceil(cell_size / 2)
    src = (self.x + offset, self.y + offset)
    dst = (target.x + offset, target.y + offset)
    imagedraw.line(
      (src[0], src[1], dst[0], dst[1]),
      fill=path_color,
    )

# A cell that houses a boss fight event
class BossCell(IconCell):
  icon = Image.open("./assets/boss.png")

  def __init__(self, x, y, text):
    super().__init__(x, y, self.icon, (icon_size, icon_size))
    self.text = text

# A cell that houses a miniboss fight event
class MiniBossCell(IconCell):
  icon = Image.open("./assets/miniboss.png")

  def __init__(self, x, y, text):
    super().__init__(x, y, self.icon, (icon_size, icon_size))
    self.text = text

# A cell that houses a dungeon event
class EventCell(IconCell):
  icon = Image.open("./assets/event.png")

  def __init__(self, x, y, text):
    super().__init__(x, y, self.icon, (icon_size, icon_size))
    self.text = text

# A cell that houses a regular treasure chest
class TreasureCell(IconCell):
  icon = Image.open("./assets/treasure.png")

  def __init__(self, x, y, text):
    super().__init__(x, y, self.icon, (icon_size, icon_size))
    self.text = text

# A cell that houses a locked treasure chest
class LockedTreasureCell(IconCell):
  icon = Image.open("./assets/lockedtreasure.png")

  def __init__(self, x, y, text):
    super().__init__(x, y, self.icon, (icon_size, icon_size))
    self.text = text

# A cell that houses a locked dream amber treasure chest
class DreamTreasureCell(IconCell):
  icon = Image.open("./assets/dreamtreasure.png")

  def __init__(self, x, y, text):
    super().__init__(x, y, self.icon, (icon_size, icon_size))
    self.text = text

# A cell that houses stairs that go up
class StairsUpCell(IconCell):
  icon = Image.open("./assets/stairsup.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (icon_size, icon_size))

# A cell that houses stairs that go down
class StairsDownCell(IconCell):
  icon = Image.open("./assets/stairsdown.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (icon_size, icon_size))

# A cell that houses a relay circle
class RelayCircleCell(IconCell):
  icon = Image.open("./assets/relay.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (icon_size, icon_size))

# A cell that houses a rock gate
class RockCell(IconCell):
  icon = Image.open("./assets/rock.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (icon_size * 1.6, icon_size * 1.6))

# A cell that houses a pushable swamp rock
class SwampRockCell(IconCell):
  icon = Image.open("./assets/swamprock.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (icon_size * 0.7, icon_size * 0.7))

# A cell that houses a 1F regular ice tile
class IceBlockCell(IconCell):
  icon = Image.open("./assets/ice.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (cell_size * 1.4, cell_size * 1.4))

# A cell that houses a 1F big ice tile
class BigIceBlockCell(IconCell):
  icon = Image.open("./assets/ice.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (cell_size * 2, cell_size * 2))

# A cell that houses a movable tile
class MovableTileCell(IconCell):
  icon = Image.open("./assets/movabletile.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (cell_size * 1.6, cell_size * 1.6))

# A cell that houses a green orb
class GreenOrbCell(IconCell):
  icon = Image.open("./assets/greenorb.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (cell_size * 2.5, cell_size * 2.5))

# A cell that houses a green orb
class BlueOrbCell(IconCell):
  icon = Image.open("./assets/blueorb.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (cell_size * 2.5, cell_size * 2.5))

# A cell that houses a green orb
class RedOrbCell(IconCell):
  icon = Image.open("./assets/redorb.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (cell_size * 2.5, cell_size * 2.5))

# A cell that houses a 3F green orb
class ArrowCell(IconCell):
  icon_up = Image.open("./assets/arrowup.png")
  icon_down = Image.open("./assets/arrowdown.png")
  icon_left = Image.open("./assets/arrowleft.png")
  icon_right = Image.open("./assets/arrowright.png")

  def __init__(self, x, y, direction):
    icon = None
    if direction.lower() == 'up':
      icon = self.icon_up
    elif direction.lower() == 'down':
      icon = self.icon_down
    elif direction.lower() == 'left':
      icon = self.icon_left
    elif direction.lower() == 'right':
      icon = self.icon_right
    super().__init__(x, y, icon, (cell_size * 2, cell_size * 2))

# A cell that houses a warp tile
class WarpCell(PathCell):
  icon = Image.open("./assets/warp.png")

  def __init__(self, x, y, dstx, dsty):
    super().__init__(
      x, y, self.icon, (cell_size * 2, cell_size * 2), dstx, dsty,
    )

# A cell that houses an invisible warp tile
class InvisibleWarpCell(PathCell):
  icon = Image.open("./assets/invisiblewarp.png")

  def __init__(self, x, y, dstx, dsty):
    super().__init__(
      x, y, self.icon, (cell_size * 2, cell_size * 2), dstx, dsty,
    )

# A floor that will be drawn in the map
class Floor:
  def __init__(self, stratum, floor, special_tiles, special_colors = {}, draw_walls = False):
    self.stratum = stratum
    self.floor = floor
    self.fileprefix = './data/'
    self.fileprefix += str(stratum) if stratum > 9 else ('0' + str(stratum))
    self.fileprefix += '0' + str(floor) + '_'
    self.special_tiles = special_tiles
    self.special_colors = special_colors
    self.draw_walls = draw_walls
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
        with open(self.fileprefix + "G.txt", 'r') as graphic_data:
          for row in range(grid_dim):
            self.grid.append([])
            y = (cell_size + grid_size) * row
            hidden_line = hidden_data.readline().split(',')[:-1]
            graphic_line = graphic_data.readline().split(',')[:-1]
            for col in range(grid_dim):
              self.grid[row].append(None)
              x = (cell_size + grid_size) * col
              # Check if cell is walkable (1 = visible, 2 = walkable)
              data = walkable_data.read(1)[0]
              walkable = data == 2
              visible = data >= 1
              # Check if cell is a hidden path (0 = not hidden)
              hidden = hidden_line[col] != '0'
              graphic = graphic_line[col]
              if walkable or hidden or (self.draw_walls and visible):
                # Make the cell and add it to the grid
                self.grid[row][col] = self.make_cell(row, col, x, y, hidden, graphic, walkable)
                # Update the boundaries for later cropping
                if col < minx:
                  minx = col
                if col > maxx:
                  maxx = col
                if row < miny:
                  miny = row
                if row > maxy:
                  maxy = row
    self.boundaries = (minx, maxx, miny, maxy)

  def make_cell(self, row, col, x, y, hidden, graphic, walkable = True):
    color_override = self.special_colors[graphic] if graphic in self.special_colors else None
    if color_override is None and not walkable:
      color_override = (0, 0, 0)
    # Check if this is a special cell by comparing row/col with x/y
    special = next(
      (tile for tile in self.special_tiles if tile.x == col and tile.y == row),
      None
    )
    # If it is special, set the proper x/y coords and return it
    if special is not None:
      special.x = x + grid_size
      special.y = y + grid_size
      special.hidden = hidden
      return special
    # Otherwise just make a simple cell
    return Cell(x + grid_size, y + grid_size, hidden, color_override)

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
    # Draw the icons
    for row in range(grid_dim):
      for col in range(grid_dim):
        if self.grid[row][col] is not None:
          self.grid[row][col].draw_icon(image)
    # Draw the paths
    if draw_paths:
      draw = ImageDraw.Draw(image)
      for row in range(grid_dim):
        for col in range(grid_dim):
          if self.grid[row][col] is not None:
            self.grid[row][col].draw_path(self.grid, draw)

  def draw_grid_row(self, y):
    for x in range(img_size):
      for g in range(grid_size):
        pixels[x, y + g] = grid_color

  def draw_grid_col(self, x, y):
    for c in range(cell_size):
      for g in range(grid_size):
        pixels[x + g, y + c] = grid_color

# These classes literally just hold the special tiles for each floor
class Oblivion1F(Floor):
  tiles = [
    BossCell(76, 58, "Lv1 Weakling Kedama"),
    BossCell(82, 43, "Lv3 Cirno"),
    BossCell(76, 82, "Lv7 Nightmare Avatar"),
    EventCell(76, 48, ""),
    EventCell(88, 67, ""),
    EventCell(114, 62, ""),
    EventCell(82, 45, ""),
    StairsUpCell(76, 80),
    WarpCell(72, 62, 70, 62),
    WarpCell(70, 62, 72, 62),
    WarpCell(77, 73, 79, 73),
    WarpCell(79, 73, 77, 73),
    WarpCell(82, 74, 82, 76),
    WarpCell(82, 76, 82, 74),
    WarpCell(107, 62, 109, 62),
    WarpCell(109, 62, 107, 62),
    TreasureCell(88, 70, ""),
    TreasureCell(109, 70, ""),
    TreasureCell(95, 71, ""),
    TreasureCell(95, 83, ""),
    TreasureCell(95, 87, ""),
    TreasureCell(95, 37, ""),
    TreasureCell(104, 43, ""),
    TreasureCell(110, 53, ""),
    TreasureCell(89, 56, ""),
    TreasureCell(109, 59, ""),
    TreasureCell(109, 65, ""),
    TreasureCell(88, 73, ""),
    TreasureCell(95, 63, ""),
    TreasureCell(57, 37, ""),
    TreasureCell(57, 41, ""),
    TreasureCell(76, 46, ""),
    TreasureCell(63, 56, ""),
    TreasureCell(33, 62, ""),
    TreasureCell(45, 62, ""),
    TreasureCell(56, 62, ""),
    TreasureCell(55, 69, ""),
    TreasureCell(73, 75, ""),
    TreasureCell(70, 78, ""),
    TreasureCell(57, 83, ""),
    TreasureCell(81, 83, ""),
    TreasureCell(57, 87, ""),
    LockedTreasureCell(76, 38, ""),
    BigIceBlockCell(80, 62),
    BigIceBlockCell(82, 48),
    BigIceBlockCell(95, 65),
    IceBlockCell(82, 49),
    IceBlockCell(85, 55),
    IceBlockCell(86, 73),
    IceBlockCell(95, 56),
  ]

  def __init__(self):
    super().__init__(1, 1, self.tiles)

class Oblivion2F(Floor):
  tiles = [
    BossCell(57, 86, ""),
    EventCell(52, 53, ""),
    StairsDownCell(49, 94),
    StairsUpCell(93, 50),
    RelayCircleCell(52, 91),
    RelayCircleCell(61, 82),
    InvisibleWarpCell(82, 72, 71, 71),
    InvisibleWarpCell(71, 73, 85, 72),
    TreasureCell(74, 83, ""),
    TreasureCell(67, 73, ""),
    TreasureCell(67, 71, ""),
    TreasureCell(76, 60, ""),
    TreasureCell(83, 60, ""),
    TreasureCell(77, 56, ""),
    TreasureCell(71, 48, ""),
    TreasureCell(49, 50, ""),
    TreasureCell(56, 57, ""),
    TreasureCell(47, 72, ""),
    TreasureCell(57, 74, ""),
    TreasureCell(65, 90, ""),
    TreasureCell(86, 82, ""),
    TreasureCell(92, 93, ""),
    TreasureCell(89, 90, ""),
    TreasureCell(95, 72, ""),
    TreasureCell(71, 72, ""),
    TreasureCell(90, 61, ""),
    TreasureCell(82, 53, ""),
    TreasureCell(71, 96, ""),
    LockedTreasureCell(66, 60, ""),
  ]

  def __init__(self):
    super().__init__(1, 2, self.tiles)

class Oblivion3F(Floor):
  tiles = [
    BossCell(73, 73, ""),
    EventCell(60, 60, ""),
    EventCell(98, 98, ""),
    StairsDownCell(68, 68),
    RelayCircleCell(65, 65),
    RockCell(69, 65),
    RockCell(71, 65),
    RockCell(65, 69),
    RockCell(65, 71),
    RockCell(72, 72),
    RockCell(56, 56),
    GreenOrbCell(96, 96),
    TreasureCell(70, 54, ""),
    TreasureCell(65, 35, ""),
    TreasureCell(54, 38, ""),
    TreasureCell(35, 43, ""),
    TreasureCell(43, 37, ""),
    TreasureCell(38, 54, ""),
    TreasureCell(35, 65, ""),
    TreasureCell(43, 57, ""),
    TreasureCell(54, 70, ""),
    TreasureCell(76, 54, ""),
    TreasureCell(100, 76, ""),
    TreasureCell(88, 55, ""),
    TreasureCell(95, 57, ""),
    TreasureCell(84, 70, ""),
    TreasureCell(94, 81, ""),
    TreasureCell(96, 90, ""),
    TreasureCell(76, 100, ""),
    TreasureCell(61, 91, ""),
    TreasureCell(57, 95, ""),
    TreasureCell(70, 84, ""),
    LockedTreasureCell(54, 76, ""),
    LockedTreasureCell(65, 43, ""),
  ]

  def __init__(self):
    super().__init__(1, 3, self.tiles)

class DreamPath1F(Floor):
  tiles = [
    BossCell(53, 53, ""),
    StairsUpCell(50, 50),
    RelayCircleCell(56, 56),
    WarpCell(56, 72, 72, 56),
    WarpCell(88, 72, 72, 88),
    WarpCell(72, 56, 56, 72),
    WarpCell(72, 88, 88, 72),
    TreasureCell(88, 56, ""),
    TreasureCell(90, 54, ""),
    TreasureCell(92, 72, ""),
    TreasureCell(88, 78, ""),
    TreasureCell(82, 72, ""),
    TreasureCell(72, 62, ""),
    TreasureCell(52, 73, ""),
    TreasureCell(72, 72, ""),
    TreasureCell(64, 80, ""),
    TreasureCell(58, 68, ""),
    TreasureCell(61, 87, ""),
    TreasureCell(91, 91, ""),
    TreasureCell(53, 91, ""),
    TreasureCell(58, 81, ""),
    LockedTreasureCell(66, 56, ""),
    LockedTreasureCell(78, 84, ""),
  ]

  def __init__(self):
    super().__init__(2, 1, self.tiles)

class DreamPath2F(Floor):
  tiles = [
    BossCell(83, 52, ""),
    EventCell(80, 52, ""),
    StairsDownCell(48, 48),
    RelayCircleCell(52, 52),
    RelayCircleCell(87, 52),
    RockCell(85, 52),
    WarpCell(109, 52, 52, 109),
    WarpCell(52, 109, 109, 52),
    TreasureCell(82, 82, ""),
    TreasureCell(92, 99, ""),
    TreasureCell(99, 92, ""),
    TreasureCell(96, 96, ""),
    TreasureCell(73, 60, ""),
    TreasureCell(74, 56, ""),
    TreasureCell(74, 48, ""),
    TreasureCell(69, 52, ""),
    TreasureCell(52, 69, ""),
    TreasureCell(72, 72, ""),
    TreasureCell(85, 61, ""),
    TreasureCell(52, 82, ""),
    TreasureCell(52, 116, ""),
    TreasureCell(116, 52, ""),
    LockedTreasureCell(45, 45, ""),
    LockedTreasureCell(92, 68, ""),
    ArrowCell(49, 83, "Up"),
    ArrowCell(49, 87, "Up"),
    ArrowCell(55, 83, "Down"),
    ArrowCell(55, 87, "Down"),
    ArrowCell(64, 85, "Left"),
    ArrowCell(72, 85, "Right"),
    ArrowCell(68, 89, "Up"),
    ArrowCell(68, 81, "Up"),
    ArrowCell(76, 85, "Left"),
    ArrowCell(63, 83, "Up"),
    ArrowCell(85, 76, "Down"),
    ArrowCell(89, 68, "Right"),
    ArrowCell(81, 68, "Right"),
    ArrowCell(76, 71, "Right"),
    ArrowCell(66, 71, "Left"),
    ArrowCell(71, 76, "Up"),
    ArrowCell(71, 66, "Down"),
    ArrowCell(62, 71, "Right"),
    ArrowCell(54, 71, "Right"),
    ArrowCell(50, 71, "Left"),
    ArrowCell(52, 76, "Up"),
    ArrowCell(48, 61, "Down"),
    ArrowCell(52, 61, "Up"),
    ArrowCell(56, 61, "Down"),
    ArrowCell(61, 48, "Right"),
    ArrowCell(61, 52, "Left"),
    ArrowCell(61, 56, "Right"),
    ArrowCell(71, 50, "Up"),
    ArrowCell(71, 54, "Down"),
    ArrowCell(71, 59, "Up"),
    ArrowCell(64, 62, "Up"),
    ArrowCell(62, 64, "Left"),
  ]

  def __init__(self):
    super().__init__(2, 2, self.tiles)

class Despair1F(Floor):
  tiles = [
    EventCell(75, 64, ""),
    EventCell(64, 75, ""),
    EventCell(90, 90, ""),
    WarpCell(75, 71, 75, 79),
    WarpCell(75, 79, 75, 71),
    WarpCell(75, 109, 41, 75),
    WarpCell(41, 75, 75, 109),
    WarpCell(71, 75, 79, 75),
    WarpCell(79, 75, 71, 75),
    WarpCell(109, 75, 77, 77),
    WarpCell(77, 77, 109, 75),
    WarpCell(75, 75, 67, 67),
    WarpCell(67, 67, 75, 75),
    WarpCell(64, 64, 83, 83),
    WarpCell(83, 83, 64, 64),
    TreasureCell(90, 75, ""),
    DreamTreasureCell(58, 64, ""),
    DreamTreasureCell(57, 62, ""),
    DreamTreasureCell(58, 61, ""),
    DreamTreasureCell(61, 58, ""),
    DreamTreasureCell(62, 57, ""),
    DreamTreasureCell(64, 58, ""),
    RockCell(59, 59),
    DreamTreasureCell(55, 61, ""),
    DreamTreasureCell(54, 59, ""),
    DreamTreasureCell(55, 58, ""),
    DreamTreasureCell(58, 55, ""),
    DreamTreasureCell(59, 54, ""),
    DreamTreasureCell(61, 55, ""),
    RockCell(56, 56),
    DreamTreasureCell(52, 58, ""),
    DreamTreasureCell(51, 56, ""),
    DreamTreasureCell(52, 55, ""),
    DreamTreasureCell(55, 52, ""),
    DreamTreasureCell(56, 51, ""),
    DreamTreasureCell(58, 52, ""),
    RockCell(53, 53),
  ]

  def __init__(self):
    super().__init__(3, 1, self.tiles)

class Anguish1F(Floor):
  tiles = [
    EventCell(70, 76, ""),
    EventCell(70, 65, ""),
    MiniBossCell(70, 64, ""),
    WarpCell(66, 55, 74, 55),
    WarpCell(74, 55, 66, 55),
    WarpCell(66, 57, 74, 57),
    WarpCell(74, 57, 66, 57),
    WarpCell(66, 83, 74, 83),
    WarpCell(74, 83, 66, 83),
    WarpCell(66, 85, 74, 85),
    WarpCell(74, 85, 66, 85),
    WarpCell(70, 97, 70, 46),
    WarpCell(70, 46, 70, 97),
    StairsUpCell(70, 60),
    LockedTreasureCell(63, 60, ""),
    TreasureCell(70, 35, ""),
    TreasureCell(84, 51, ""),
    TreasureCell(76, 52, ""),
    TreasureCell(79, 55, ""),
    TreasureCell(61, 57, ""),
    TreasureCell(49, 58, ""),
    TreasureCell(87, 59, ""),
    TreasureCell(77, 60, ""),
    TreasureCell(41, 70, ""),
    TreasureCell(44, 70, ""),
    TreasureCell(92, 70, ""),
    TreasureCell(65, 77, ""),
    TreasureCell(75, 77, ""),
    TreasureCell(66, 100, ""),
    TreasureCell(70, 105, ""),
  ]

  def __init__(self):
    super().__init__(4, 1, self.tiles, {"32": (55, 228, 255)})

class Anguish2F(Floor):
  tiles = [
    StairsDownCell(74, 88),
    RelayCircleCell(76, 90),
    ArrowCell(75, 92, "Up"),
    GreenOrbCell(75, 95),
    RockCell(75, 81),
    BossCell(75, 79, ""),
    RockCell(72, 75),
    EventCell(70, 75, ""),
    TreasureCell(67, 85, ""),
    TreasureCell(83, 85, ""),
    TreasureCell(48, 90, ""),
    TreasureCell(102, 90, ""),
    TreasureCell(98, 96, ""),
    TreasureCell(76, 100, ""),
    TreasureCell(54, 103, ""),
    TreasureCell(71, 107, ""),
    TreasureCell(96, 111, ""),
    TreasureCell(52, 118, ""),
    TreasureCell(67, 129, ""),
    TreasureCell(83, 129, ""),
    TreasureCell(41, 131, ""),
    TreasureCell(109, 131, ""),
    LockedTreasureCell(80, 75, ""),
    EventCell(75, 62, ""),
    RelayCircleCell(75, 61),
    RockCell(75, 56),
    RockCell(75, 54),
    StairsUpCell(75, 48),
    BlueOrbCell(37, 33),
    RedOrbCell(113, 33),
    LockedTreasureCell(43, 42, ""),
    TreasureCell(53, 63, ""),
    TreasureCell(53, 20, ""),
    TreasureCell(34, 55, ""),
    TreasureCell(43, 41, ""),
    TreasureCell(64, 25, ""),
    TreasureCell(86, 25, ""),
    TreasureCell(75, 44, ""),
    TreasureCell(75, 13, ""),
    TreasureCell(107, 41, ""),
    TreasureCell(107, 42, ""),
    TreasureCell(97, 55, ""),
    TreasureCell(116, 55, ""),
    TreasureCell(97, 19, ""),
    TreasureCell(97, 27, ""),
  ]

  def __init__(self):
    super().__init__(4, 2, self.tiles, {"32": (55, 228, 255)})

class Anguish3F(Floor):
  tiles = [
    StairsDownCell(83, 81),
    RelayCircleCell(83, 83),
    RockCell(83, 87),
    EventCell(86, 90, ""),
    MiniBossCell(87, 83, ""),
    WarpCell(90, 88, 56, 67),
    WarpCell(56, 67, 90, 88),
    ArrowCell(63, 67, "Right"),
    RelayCircleCell(57, 57),
    BossCell(52, 52, ""),
    WarpCell(70, 71, 72, 71),
    WarpCell(72, 71, 70, 71),
    WarpCell(71, 70, 71, 72),
    WarpCell(71, 72, 71, 70),
    WarpCell(78, 79, 80, 79),
    WarpCell(80, 79, 78, 79),
    WarpCell(79, 78, 79, 80),
    WarpCell(79, 80, 79, 78),
    WarpCell(79, 73, 77, 73),
    WarpCell(71, 77, 73, 77),
    LockedTreasureCell(92, 56, ""),
    LockedTreasureCell(64, 100, ""),
    TreasureCell(69, 85, ""),
    TreasureCell(74, 110, ""),
    TreasureCell(48, 110, ""),
    TreasureCell(65, 53, ""),
    TreasureCell(89, 29, ""),
    TreasureCell(89, 42, ""),
    TreasureCell(91, 39, ""),
    TreasureCell(89, 69, ""),
    TreasureCell(84, 73, ""),
    TreasureCell(89, 65, ""),
    TreasureCell(113, 53, ""),
    TreasureCell(66, 77, ""),
    TreasureCell(61, 84, ""),
    TreasureCell(37, 97, ""),
    TreasureCell(61, 121, ""),
    TreasureCell(85, 97, ""),
  ]

  def __init__(self):
    super().__init__(4, 3, self.tiles, {"32": (55, 228, 255)})

class Fragile1F(Floor):
  tiles = [
    SwampRockCell(42, 70),
    SwampRockCell(51, 81),
    SwampRockCell(52, 59),
    SwampRockCell(64, 70),
    SwampRockCell(75, 84),
    SwampRockCell(88, 52),
    SwampRockCell(88, 88),
    SwampRockCell(100, 70),
    RockCell(90, 70),
    EventCell(81, 70, ""),
    ArrowCell(48, 84, "Down"),
    ArrowCell(46, 84, "Up"),
    MiniBossCell(76, 70, ""),
    StairsUpCell(75, 61),
    LockedTreasureCell(82, 73, ""),
    TreasureCell(75, 47, ""),
    TreasureCell(93, 47, ""),
    TreasureCell(54, 48, ""),
    TreasureCell(108, 48, ""),
    TreasureCell(45, 51, ""),
    TreasureCell(36, 56, ""),
    TreasureCell(82, 67, ""),
    TreasureCell(29, 70, ""),
    TreasureCell(121, 70, ""),
    TreasureCell(36, 84, ""),
    TreasureCell(45, 89, ""),
    TreasureCell(54, 92, ""),
    TreasureCell(108, 92, ""),
    TreasureCell(93, 93, ""),
  ]

  def __init__(self):
    super().__init__(5, 1, self.tiles, {
      "8": (0, 0, 0),
      "9": (0, 0, 0),
      "10": (0, 0, 0),
      "11": (0, 0, 0),
      "12": (0, 0, 0),
      "13": (0, 0, 0),
      "14": (0, 0, 0),
      "15": (0, 0, 0),
    })

class Fragile2F(Floor):
  tiles = [
    StairsDownCell(38, 37),
    RelayCircleCell(40, 39),
    WarpCell(42, 44, 42, 42),
    WarpCell(42, 42, 42, 44),
    SwampRockCell(62, 70),
    SwampRockCell(71, 61),
    RelayCircleCell(73, 72),
    BossCell(76, 75, ""),
    TreasureCell(27, 26, ""),
    TreasureCell(67, 30, ""),
    TreasureCell(34, 33, ""),
    TreasureCell(63, 37, ""),
    TreasureCell(54, 43, ""),
    TreasureCell(40, 47, ""),
    TreasureCell(58, 57, ""),
    TreasureCell(31, 66, ""),
    TreasureCell(39, 66, ""),
  ]

  def __init__(self):
    super().__init__(5, 2, self.tiles, {
      "8": (0, 0, 0),
      "9": (0, 0, 0),
      "10": (0, 0, 0),
      "11": (0, 0, 0),
      "12": (0, 0, 0),
      "13": (0, 0, 0),
      "14": (0, 0, 0),
      "15": (0, 0, 0),
    })

class Fragile3F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(5, 3, self.tiles)

class Unforgiven1F(Floor):
  tiles = [
    MovableTileCell(63, 47),
    MovableTileCell(62, 51),
    MovableTileCell(47, 53),
    MovableTileCell(53, 53),
    MovableTileCell(64, 53),
    MovableTileCell(55, 56),
    MovableTileCell(70, 56),
    MovableTileCell(49, 60),
    MovableTileCell(89, 60),
    MovableTileCell(64, 61),
    MovableTileCell(46, 64),
    MovableTileCell(71, 64),
    MovableTileCell(85, 64),
    MovableTileCell(80, 67),
    MovableTileCell(91, 68),
    MovableTileCell(68, 76),
    MovableTileCell(77, 78),
    MovableTileCell(77, 79),
    MovableTileCell(63, 80),
    MovableTileCell(83, 80),
    MovableTileCell(75, 81),
    MovableTileCell(84, 82),
    MovableTileCell(41, 83),
    MovableTileCell(62, 83),
    MovableTileCell(62, 84),
    MovableTileCell(80, 87),
    MovableTileCell(53, 89),
    MovableTileCell(67, 89),
    MovableTileCell(59, 91),
    MovableTileCell(62, 95),
    MovableTileCell(59, 98),
    MovableTileCell(73, 100),
    MovableTileCell(71, 101),
    MovableTileCell(73, 101),
    MovableTileCell(64, 103),
    MovableTileCell(48, 106),
    MovableTileCell(74, 106),
    MovableTileCell(68, 109),
    MovableTileCell(67, 110),
    MovableTileCell(74, 110),
    MovableTileCell(71, 111),
    MiniBossCell(65, 91, ""),
    WarpCell(56, 48, 56, 50),
    WarpCell(59, 104, 59, 102),
    WarpCell(59, 102, 59, 104),
    StairsUpCell(63, 72),
    LockedTreasureCell(71, 117, ""),
    TreasureCell(63, 44, ""),
    TreasureCell(98, 50, ""),
    TreasureCell(51, 53, ""),
    TreasureCell(59, 56, ""),
    TreasureCell(77, 60, ""),
    TreasureCell(51, 71, ""),
    TreasureCell(95, 76, ""),
    TreasureCell(72, 83, ""),
    TreasureCell(65, 87, ""),
    TreasureCell(48, 89, ""),
    TreasureCell(75, 91, ""),
    TreasureCell(63, 100, ""),
    TreasureCell(37, 108, ""),
    TreasureCell(82, 119, ""),
  ]

  def __init__(self):
    super().__init__(6, 1, self.tiles, {
      "5": (0, 0, 0),
      "6": (127, 127, 127),
      "7": (127, 127, 127),
      "8": (127, 127, 127),
      "9": (127, 127, 127),
      "10": (127, 127, 127),
      "11": (127, 127, 127),
      "12": (127, 127, 127),
      "13": (127, 127, 127),
      "14": (127, 127, 127),
      "15": (127, 127, 127),
      "16": (127, 127, 127),
      "17": (127, 127, 127),
      "18": (127, 127, 127),
      "19": (127, 127, 127),
      "20": (127, 127, 127),
      "21": (127, 127, 127),
      "22": (127, 127, 127),
      "23": (127, 127, 127),
      "26": (0, 0, 0),
    }, True)

class Unforgiven2F(Floor):
  tiles = [
    MovableTileCell(56, 30),
    MovableTileCell(73, 30),
    MovableTileCell(82, 31),
    MovableTileCell(52, 33),
    MovableTileCell(73, 34),
    MovableTileCell(56, 38),
    MovableTileCell(81, 38),
    MovableTileCell(79, 40),
    MovableTileCell(43, 42),
    MovableTileCell(47, 42),
    MovableTileCell(40, 45),
    MovableTileCell(51, 47),
    MovableTileCell(40, 49),
    MovableTileCell(51, 51),
    MovableTileCell(45, 53),
    MovableTileCell(49, 53),
    MovableTileCell(31, 54),
    MovableTileCell(94, 55),
    MovableTileCell(98, 55),
    MovableTileCell(41, 57),
    MovableTileCell(55, 57),
    MovableTileCell(29, 58),
    MovableTileCell(95, 59),
    MovableTileCell(101, 59),
    MovableTileCell(92, 63),
    MovableTileCell(100, 63),
    MovableTileCell(29, 66),
    MovableTileCell(33, 66),
    MovableTileCell(96, 68),
    MovableTileCell(31, 70),
    MovableTileCell(105, 70),
    MovableTileCell(100, 71),
    MovableTileCell(98, 73),
    MovableTileCell(96, 74),
    MovableTileCell(91, 75),
    MovableTileCell(108, 75),
    MovableTileCell(103, 77),
    MovableTileCell(114, 77),
    MovableTileCell(79, 78),
    MovableTileCell(79, 79),
    MovableTileCell(92, 79),
    MovableTileCell(76, 81),
    MovableTileCell(77, 81),
    MovableTileCell(110, 82),
    MovableTileCell(61, 87),
    MovableTileCell(84, 88),
    MovableTileCell(86, 88),
    MovableTileCell(91, 88),
    MovableTileCell(68, 93),
    MovableTileCell(77, 94),
    MovableTileCell(64, 95),
    MovableTileCell(97, 95),
    MovableTileCell(66, 98),
    MovableTileCell(68, 98),
    MovableTileCell(78, 98),
    MovableTileCell(93, 99),
    MovableTileCell(102, 99),
    MovableTileCell(62, 101),
    MovableTileCell(78, 102),
    MovableTileCell(110, 102),
    MovableTileCell(97, 104),
    MovableTileCell(72, 105),
    MovableTileCell(90, 105),
    MovableTileCell(60, 110),
    MovableTileCell(74, 111),
    MovableTileCell(88, 112),
    MovableTileCell(84, 113),
    StairsDownCell(111, 113),
    RelayCircleCell(107, 109),
    RockCell(104, 104),
    EventCell(106, 105, ""),
    RelayCircleCell(73, 75),
    BossCell(70, 72, ""),
    WarpCell(102, 105, 102, 107),
    WarpCell(102, 107, 102, 105),
    LockedTreasureCell(90, 93, ""),
    TreasureCell(96, 49, ""),
    TreasureCell(111, 59, ""),
    TreasureCell(81, 62, ""),
    TreasureCell(111, 69, ""),
    TreasureCell(89, 75, ""),
    TreasureCell(77, 79, ""),
    TreasureCell(61, 84, ""),
    TreasureCell(106, 86, ""),
    TreasureCell(91, 92, ""),
    TreasureCell(73, 98, ""),
    TreasureCell(68, 108, ""),
    TreasureCell(67, 114, ""),
    TreasureCell(84, 115, ""),
    TreasureCell(67, 116, ""),
  ]

  def __init__(self):
    super().__init__(6, 2, self.tiles, {
      "5": (0, 0, 0),
      "6": (127, 127, 127),
      "7": (127, 127, 127),
      "8": (127, 127, 127),
      "9": (127, 127, 127),
      "10": (127, 127, 127),
      "11": (127, 127, 127),
      "12": (127, 127, 127),
      "13": (127, 127, 127),
      "14": (127, 127, 127),
      "15": (127, 127, 127),
      "16": (127, 127, 127),
      "17": (127, 127, 127),
      "18": (127, 127, 127),
      "19": (127, 127, 127),
      "20": (127, 127, 127),
      "21": (127, 127, 127),
      "22": (127, 127, 127),
      "23": (127, 127, 127),
      "26": (0, 0, 0),
    }, True)

class Unforgiven3F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(6, 3, self.tiles)

class Solitary1F(Floor):
  tiles = [
    RockCell(104, 107),
    EventCell(104, 109, ""),
    MiniBossCell(107, 104, ""),
    WarpCell(109, 104, 50, 50),
    WarpCell(50, 50, 109, 104),
    ArrowCell(52, 54, "Right"),
    ArrowCell(54, 52, "Down"),
    StairsUpCell(54, 54),
    LockedTreasureCell(65, 65, ""),
    TreasureCell(63, 46, ""),
    TreasureCell(107, 52, ""),
    TreasureCell(73, 56, ""),
    TreasureCell(46, 63, ""),
    TreasureCell(96, 70, ""),
    TreasureCell(74, 74, ""),
    TreasureCell(55, 77, ""),
    TreasureCell(96, 78, ""),
    TreasureCell(70, 96, ""),
    TreasureCell(78, 96, ""),
    TreasureCell(52, 107, ""),
  ]

  def __init__(self):
    super().__init__(7, 1, self.tiles, {"16": (55, 228, 255)})

class Solitary2F(Floor):
  tiles = [
    StairsDownCell(117, 117),
    RelayCircleCell(113, 113),
    RelayCircleCell(72, 72),
    BossCell(69, 69, ""),
    TreasureCell(79, 79, ""),
    TreasureCell(83, 83, ""),
    TreasureCell(107, 83, ""),
    TreasureCell(89, 89, ""),
    TreasureCell(119, 100, ""),
    TreasureCell(101, 101, ""),
    TreasureCell(83, 107, ""),
    TreasureCell(107, 107, ""),
    TreasureCell(100, 119, ""),
  ]

  def __init__(self):
    super().__init__(7, 2, self.tiles, {"16": (55, 228, 255)})

class Solitary3F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(7, 3, self.tiles, {"16": (55, 228, 255)})

class Utopia1F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(8, 1, self.tiles)

class Utopia2F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(8, 2, self.tiles)

class Utopia3F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(8, 3, self.tiles)

class GreatNightmare1F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(9, 1, self.tiles)

class GreatNightmare2F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(9, 2, self.tiles)

class GreatNightmare3F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(9, 3, self.tiles, {"61": (55, 228, 255)})

class GreatNightmare4F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(9, 4, self.tiles, {"61": (55, 228, 255)})

class Chaos1F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(10, 1, self.tiles, {"81": (55, 228, 255)})

class Chaos2F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(10, 2, self.tiles, {"81": (55, 228, 255)})

class Chaos3F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(10, 3, self.tiles, {"81": (55, 228, 255)})

class Chaos4F(Floor):
  tiles = [
  ]

  def __init__(self):
    super().__init__(10, 4, self.tiles, {"81": (55, 228, 255)})

# Make a 150x150 canvas so we can fill out the grid
map_img = Image.new("RGBA", (img_size, img_size), "black")
pixels = map_img.load()

# Actually draw the grid and cells
# floor = Oblivion1F()
# floor = Oblivion2F()
# floor = Oblivion3F()
# floor = DreamPath1F()
# floor = DreamPath2F()
# floor = Despair1F()
# floor = Anguish1F()
# floor = Anguish2F()
# floor = Anguish3F()
# floor = Fragile1F()
# floor = Fragile2F()
# floor = Fragile3F()
# floor = Unforgiven1F()
# floor = Unforgiven2F()
# floor = Unforgiven3F()
# floor = Solitary1F()
floor = Solitary2F()
# floor = Solitary3F()
# floor = Utopia1F()
# floor = Utopia2F()
# floor = Utopia3F()
# floor = GreatNightmare1F()
# floor = GreatNightmare2F()
# floor = GreatNightmare3F()
# floor = GreatNightmare4F()
# floor = Chaos1F()
# floor = Chaos2F()
# floor = Chaos3F()
# floor = Chaos4F()
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
alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
labels = [i for i in alphabet] + ["A" + i for i in alphabet]

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
