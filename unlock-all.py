target_dir = "unlock-target" # The dir that contains the save file
max_upgrade_main = False # Whether characters will have main equip at +5
max_upgrade_sub = False # Whether sub equips will be at +10
lots_money = False # WANNA DOUBLE YOUR COINS?

# Fully unlock map data
for i in range(1, 11):
  for j in range(1, 6):
    x = ("" if i > 9 else "0") + str(i)
    y = "0" + str(j)
    fname = x + y + "_OD.txt"
    with open(target_dir + '/' + fname, 'wb') as f:
      for xp in range(150):
        for yp in range(150):
          f.write(bytearray([2]))

# Characters to level 100, unlock all skills, upgrade main equip
for i in range(1, 49):
  x = ("0" if i > 9 else "00") + str(i)
  fname = "C" + x + ".ngd"
  data = None
  with open(target_dir + '/' + fname, 'rb') as f:
    data = list(f.read())
  data[0x0:0x4] = [0, 0, 0, 100]
  data[0x4:0x8] = [0, 0, 0, 100]
  data[0xbc:0x23c] = [0, 0, 0, 1]*96
  if max_upgrade_main:
    data[0x878:0x87c] = [0, 0, 0, 5]
  with open(target_dir + '/' + fname, 'wb') as f:
    f.write(bytearray(data))

# Unlock all items
with open(target_dir + "/EEF01.ngd", 'wb') as f:
  f.write(bytearray([0]))
  for i in range(1200):
    f.write(bytearray([1]))

# Max upgrade subequips
if max_upgrade_sub:
  with open(target_dir + "/EEH01.ngd", 'wb') as f:
    f.write(bytearray([0, 0, 0, 0]))
    for i in range(500):
      f.write(bytearray([0, 0, 0, 10]))

# 255 copies of every item
with open(target_dir + "/EEN01.ngd", 'wb') as f:
  f.write(bytearray([0, 0, 0, 0]))
  for i in range(1200):
    f.write(bytearray([0, 0, 0, 255]))

# Unlock all characters, get lots of money
data = None
with open(target_dir + "/PGD01.ngd", 'rb') as f:
  data = list(f.read())
data[0x4:0xc4] = [0, 0, 0, 1]*48
if lots_money:
  data[0x1d4] = 255
  data[0x1dc] = 255
with open(target_dir + "/PGD01.ngd", 'wb') as f:
  f.write(bytearray(data))
