import math
from PIL import Image, ImageDraw

cell_size = 180 # How wide each grid cell is, each adition takes up half as much
cell_offset = cell_size // 2 # How each tile is offset to its neighbor
grid_dim = 150 # How many columns and rows to draw

img_size = cell_size * grid_dim

# A cell that is filled in in the grid, at position (X, Y)
class Cell:
  def __init__(self, x, y, stratum, tile, hidden, walkable):
    tilename = 'Grid' + ('0' if tile < 10 else '') + str(tile) + '.png'
    self.tile = Image.open('./assets/tiles/' + stratum + '/' + tilename)
    self.hidden = hidden
    self.walkable = walkable
    self.x = x
    self.y = y

  def draw(self, image):
    posx = (img_size // 2) + ((self.y - self.x) * cell_offset)
    posy = cell_offset + ((self.x + self.y) * cell_offset // 2)
    diffx = self.tile.size[0] - cell_size
    excessy = self.tile.size[1] - 200
    undery = cell_offset - self.tile.size[1]
    finalx = posx - cell_offset - (diffx // 2)
    finaly = posy - (cell_offset // 2)
    if undery > 0:
      finaly += int(undery * 1.5)
    # if excessy > 0:
    #   finaly -= excessy
    if not self.walkable:
      finaly -= 30
    image.paste(self.tile, (finalx, finaly), self.tile)

  def draw_icon(self, image):
    pass

# # A cell that houses an icon
# class IconCell(Cell):
#   def __init__(self, x, y, icon, size):
#     super().__init__(x, y, False)
#     self.icon = icon
#     self.icon.thumbnail(size)
#     self.shift_x = (self.icon.size[0] - (cell_size, cell_size)[0]) // 2
#     self.shift_y = (self.icon.size[1] - (cell_size, cell_size)[1]) // 2

#   def draw_icon(self, image):
#     image.paste(
#       self.icon,
#       (self.x - self.shift_x, self.y - self.shift_y),
#       self.icon,
#     )

# # A cell that houses a boss fight event
# class BossCell(IconCell):
#   icon = Image.open("./assets/boss.png")

#   def __init__(self, x, y, text):
#     super().__init__(x, y, self.icon, (icon_size, icon_size))
#     self.text = text

# # A cell that houses a dungeon event
# class EventCell(IconCell):
#   icon = Image.open("./assets/event.png")

#   def __init__(self, x, y, text):
#     super().__init__(x, y, self.icon, (icon_size, icon_size))
#     self.text = text

# # A cell that houses a regular treasure chest
# class TreasureCell(IconCell):
#   icon = Image.open("./assets/treasure.png")

#   def __init__(self, x, y, text):
#     super().__init__(x, y, self.icon, (icon_size, icon_size))
#     self.text = text

# # A cell that houses a locked treasure chest
# class LockedTreasureCell(IconCell):
#   icon = Image.open("./assets/lockedtreasure.png")

#   def __init__(self, x, y, text):
#     super().__init__(x, y, self.icon, (icon_size, icon_size))
#     self.text = text

# # A cell that houses stairs that go up
# class StairsUpCell(IconCell):
#   icon = Image.open("./assets/stairsup.png")

#   def __init__(self, x, y):
#     super().__init__(x, y, self.icon, (icon_size, icon_size))

# # A cell that houses stairs that go down
# class StairsDownCell(IconCell):
#   icon = Image.open("./assets/stairsup.png")

#   def __init__(self, x, y):
#     super().__init__(x, y, self.icon, (icon_size, icon_size))

# # A cell that houses a 1F regular ice tile
# class IceCell(IconCell):
#   icon = Image.open("./assets/ice.png")

#   def __init__(self, x, y):
#     super().__init__(x, y, self.icon, (cell_size * 1.4, cell_size * 1.4))

# # A cell that houses a 1F big ice tile
# class BigIceCell(IconCell):
#   icon = Image.open("./assets/ice.png")

#   def __init__(self, x, y):
#     super().__init__(x, y, self.icon, (cell_size * 2, cell_size * 2))

# A floor that will be drawn in the map
class Floor:
  def __init__(self, stratum, floor, special_tiles):
    self.stratum = str(stratum) if stratum > 9 else ('0' + str(stratum))
    self.floor = '0' + str(floor)
    self.fileprefix = self.stratum + self.floor + '_'
    self.special_tiles = special_tiles
    self.init_grid()

  def init_grid(self):
    self.grid = []
    with open(self.fileprefix + "OD.txt", "rb") as walkable_data:
      with open(self.fileprefix + "G.txt", "r") as tile_data:
        with open(self.fileprefix + "H.txt", 'r') as hidden_data:
          for row in range(grid_dim):
            self.grid.append([])
            tile_line = tile_data.readline().split(',')[:-1]
            hidden_line = hidden_data.readline().split(',')[:-1]
            for col in range(grid_dim):
              self.grid[row].append(None)
              # Check if cell is walkable (1 = visible, 2 = walkable)
              walkable = walkable_data.read(1)[0] == 2
              # Check if cell is renderable (0 = not renderable)
              shown = tile_line[col] != '0'
              # # Check if cell is a hidden path (0 = not hidden)
              # hidden = hidden_line[col] != '0'
              if shown:
                self.grid[row][col] = self.make_cell(
                  row, col, self.stratum, tile_line[col], walkable
                )

  def make_cell(self, x, y, stratum, tile, walkable):
    # special = next(
    #   (tile for tile in self.special_tiles if tile.x == col and tile.y == row),
    #   None
    # )
    # if special is not None:
    #   special.x = x + grid_size
    #   special.y = y + grid_size
    #   return special
    return Cell(x, y, stratum, int(tile), False, walkable)

  def draw(self, image, pixels):
    # Draw the cells from top to bottom, left to right
    for row in range(grid_dim):
      for col in range(grid_dim):
        # Draw the cell, if available
        if self.grid[row][col] is not None:
          self.grid[row][col].draw(image)
    # # Draw the icons
    # for row in range(grid_dim):
    #   for col in range(grid_dim):
    #     if self.grid[row][col] is not None:
    #       self.grid[row][col].draw_icon(image)

class Oblivion1F(Floor):
  tiles = [
    # BossCell(76, 58, "Lv1 Weakling Kedama"),
    # BossCell(82, 43, "Lv3 Cirno"),
    # BossCell(76, 82, "Lv7 Nightmare Avatar"),
    # EventCell(76, 48, ""),
    # EventCell(88, 67, ""),
    # EventCell(114, 62, ""),
    # EventCell(82, 45, ""),
    # TreasureCell(88, 70, ""),
    # TreasureCell(109, 70, ""),
    # TreasureCell(95, 71, ""),
    # TreasureCell(95, 83, ""),
    # TreasureCell(95, 87, ""),
    # TreasureCell(95, 37, ""),
    # TreasureCell(104, 43, ""),
    # TreasureCell(110, 53, ""),
    # TreasureCell(89, 56, ""),
    # TreasureCell(109, 59, ""),
    # TreasureCell(109, 65, ""),
    # TreasureCell(88, 73, ""),
    # TreasureCell(95, 63, ""),
    # TreasureCell(57, 37, ""),
    # TreasureCell(57, 41, ""),
    # TreasureCell(76, 46, ""),
    # TreasureCell(63, 56, ""),
    # TreasureCell(33, 62, ""),
    # TreasureCell(45, 62, ""),
    # TreasureCell(56, 62, ""),
    # TreasureCell(55, 69, ""),
    # TreasureCell(73, 75, ""),
    # TreasureCell(70, 78, ""),
    # TreasureCell(57, 83, ""),
    # TreasureCell(81, 83, ""),
    # TreasureCell(57, 87, ""),
    # LockedTreasureCell(76, 38, ""),
    # StairsUpCell(76, 80),
    # WarpCell(72, 62, 70, 62),
    # WarpCell(70, 62, 72, 62),
    # WarpCell(77, 73, 79, 73),
    # WarpCell(79, 73, 77, 73),
    # WarpCell(82, 74, 82, 76),
    # WarpCell(82, 76, 82, 74),
    # WarpCell(107, 62, 109, 62),
    # WarpCell(109, 62, 107, 62),
    # BigIceCell(80, 62),
    # BigIceCell(82, 48),
    # BigIceCell(95, 65),
    # IceCell(82, 49),
    # IceCell(85, 55),
    # IceCell(86, 73),
    # IceCell(95, 56),
  ]

  def __init__(self):
    super().__init__(1, 1, self.tiles)

img = Image.new("RGBA", (img_size, img_size // 2), "black")
pixels = img.load()

floor = Oblivion1F()
floor.draw(img, pixels)
img.show()
# img.save("out_v.png")
