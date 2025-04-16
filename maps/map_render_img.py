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
  def __init__(self, x, y, hidden):
    self.hidden = hidden
    self.x = x
    self.y = y

  def draw(self, pixels):
    # Use a grey shade when path is hidden
    color = (127, 127, 127) if self.hidden else (255, 255, 255)
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
    super().__init__(x, y, self.icon, (icon_size, icon_size))

# A cell that houses a 1F regular ice tile
class IceCell(IconCell):
  icon = Image.open("./assets/ice.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (cell_size * 1.4, cell_size * 1.4))

# A cell that houses a 1F big ice tile
class BigIceCell(IconCell):
  icon = Image.open("./assets/ice.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (cell_size * 2, cell_size * 2))

# A cell that houses a 3F green orb
class OblivionOrbCell(IconCell):
  icon = Image.open("./assets/oblivionorb.png")

  def __init__(self, x, y):
    super().__init__(x, y, self.icon, (cell_size, cell_size))

# A cell that houses a 3F green orb
class DreamArrowCell(IconCell):
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
  def __init__(self, stratum, floor, special_tiles):
    self.stratum = stratum
    self.floor = floor
    self.fileprefix = './data/'
    self.fileprefix += str(stratum) if stratum > 9 else ('0' + str(stratum))
    self.fileprefix += '0' + str(floor) + '_'
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
        for row in range(grid_dim):
          self.grid.append([])
          y = (cell_size + grid_size) * row
          hidden_line = hidden_data.readline().split(',')[:-1]
          for col in range(grid_dim):
            self.grid[row].append(None)
            x = (cell_size + grid_size) * col
            # Check if cell is walkable (1 = visible, 2 = walkable)
            walkable = walkable_data.read(1)[0] == 2
            # Check if cell is a hidden path (0 = not hidden)
            hidden = hidden_line[col] != '0'
            if walkable or hidden:
              # Make the cell and add it to the grid
              self.grid[row][col] = self.make_cell(row, col, x, y, hidden)
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

  def make_cell(self, row, col, x, y, hidden):
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
    return Cell(x + grid_size, y + grid_size, hidden)

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
    BigIceCell(80, 62),
    BigIceCell(82, 48),
    BigIceCell(95, 65),
    IceCell(82, 49),
    IceCell(85, 55),
    IceCell(86, 73),
    IceCell(95, 56),
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
    EventCell(58, 60, ""),
    EventCell(98, 98, ""),
    StairsDownCell(68, 68),
    RelayCircleCell(65, 65),
    RockCell(69, 65),
    RockCell(71, 65),
    RockCell(65, 69),
    RockCell(65, 71),
    RockCell(72, 72),
    RockCell(56, 56),
    OblivionOrbCell(96, 96),
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
    DreamArrowCell(49, 83, "Up"),
    DreamArrowCell(49, 87, "Up"),
    DreamArrowCell(55, 83, "Down"),
    DreamArrowCell(55, 87, "Down"),
    DreamArrowCell(64, 85, "Left"),
    DreamArrowCell(72, 85, "Right"),
    DreamArrowCell(68, 89, "Up"),
    DreamArrowCell(68, 81, "Up"),
    DreamArrowCell(76, 85, "Left"),
    DreamArrowCell(63, 83, "Up"),
    DreamArrowCell(85, 76, "Down"),
    DreamArrowCell(89, 68, "Right"),
    DreamArrowCell(81, 68, "Right"),
    DreamArrowCell(76, 71, "Right"),
    DreamArrowCell(66, 71, "Left"),
    DreamArrowCell(71, 76, "Up"),
    DreamArrowCell(71, 66, "Down"),
    DreamArrowCell(62, 71, "Right"),
    DreamArrowCell(54, 71, "Right"),
    DreamArrowCell(50, 71, "Left"),
    DreamArrowCell(52, 76, "Up"),
    DreamArrowCell(48, 61, "Down"),
    DreamArrowCell(52, 61, "Up"),
    DreamArrowCell(56, 61, "Down"),
    DreamArrowCell(61, 48, "Right"),
    DreamArrowCell(61, 52, "Left"),
    DreamArrowCell(61, 56, "Right"),
    DreamArrowCell(71, 50, "Up"),
    DreamArrowCell(71, 54, "Down"),
    DreamArrowCell(71, 59, "Up"),
    DreamArrowCell(64, 62, "Up"),
    DreamArrowCell(62, 64, "Left"),
  ]

  def __init__(self):
    super().__init__(2, 2, self.tiles)

# Make a 150x150 canvas so we can fill out the grid
map_img = Image.new("RGBA", (img_size, img_size), "black")
pixels = map_img.load()

# Actually draw the grid and cells
# floor = Oblivion1F()
# floor = Oblivion2F()
# floor = Oblivion3F()
# floor = DreamPath1F()
floor = DreamPath2F()
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
