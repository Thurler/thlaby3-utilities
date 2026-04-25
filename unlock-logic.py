target_dir = "unlock-logic" # The dir that contains the save file
subs = [
  1, 2, 3, 5, 6, 9, 13, 14, 17, 18, 21, 25, 26, 29, 30, 35, 39, 43, 47, 61, 62, 63, # Cirno
  22, 23, 24, 33, 44, 45, 49, 60, 64, 65, 66, 68, 75, 76, # Nightmare
  7, 78, 86, # Ran
  15, 27, 50, 57, 67, 69, 70, 71, 83, 87, 91, 95, # Horde
  10, 16, 19, 20, 28, 53, 54, 80, 88, # Sumireko Protector
  56, 72 # Reset
]
mats = [
  1, 6, 14, 23, 33, 39, 41, 45, 59, # Cirno
  29, 57, 61, # Nightmare
  25, 37, 49, 62, # Horde
  11, 12, # Sumireko Protector
  30, 63, 71 # Reset
]
breaks = [1, 2, 3, 4, 5, 6, 7, 8] # Cirno
specs = [
  1, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16 # Cirno
]

# Unlock required items
with open(target_dir + "/EEF01.ngd", 'rb') as fr:
  data = fr.read()
with open(target_dir + "/EEF01.ngd", 'wb') as f:
  for i in range(500):
    if i in subs:
      f.write(bytearray([1]))
    else:
      f.write(bytearray([data[i]]))
  for i in range(200):
    if i in mats:
      f.write(bytearray([1]))
    else:
      f.write(bytearray([data[i+500]]))
  for i in range(100):
    if i in breaks:
      f.write(bytearray([1]))
    else:
      f.write(bytearray([data[i+700]]))
  for i in range(200):
    if i in specs:
      f.write(bytearray([1]))
    else:
      f.write(bytearray([data[i+800]]))
  for i in range(201):
      f.write(bytearray([data[i+1000]]))

# 500 copies of every item
with open(target_dir + "/EEN01.ngd", 'rb') as fr:
  data = fr.read()
with open(target_dir + "/EEN01.ngd", 'wb') as f:
  for i in range(500):
    if i in subs:
      f.write(bytearray([0, 0, 1, 0xf4]))
    else:
      f.write(bytearray(data[i*4:i*4+4]))
  for i in range(200):
    if i in mats:
      if i == 71:
        f.write(bytearray([0, 0, 3, 0xe8]))
      else:
        f.write(bytearray([0, 0, 1, 0xf4]))
    else:
      f.write(bytearray(data[(i+500)*4:(i+500)*4+4]))
  for i in range(100):
    if i in breaks:
      f.write(bytearray([0, 0, 1, 0xf4]))
    else:
      f.write(bytearray(data[(i+700)*4:(i+700)*4+4]))
  for i in range(200):
    if i in specs:
      f.write(bytearray([0, 0, 1, 0xf4]))
    else:
      f.write(bytearray(data[(i+800)*4:(i+800)*4+4]))
  for i in range(201):
      f.write(bytearray(data[(i+1000)*4:(i+1000)*4+4]))
