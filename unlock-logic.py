target_dir = "unlock-logic" # The dir that contains the save file
main = []
subs = [
  1, 2, 3, 5, 6, 9, 13, 14, 17, 18, 21, 25, 26, 29, 30, 35, 39, 43, 47, 61, 62, 63, # Cirno
  22, 23, 24, 33, 44, 45, 49, 60, 64, 65, 66, 68, 75, 76, # Nightmare
  7, 78, 86, # Ran
  15, 27, 50, 57, 67, 69, 70, 71, 83, 87, 91, 95, # Horde
  10, 16, 19, 20, 28, 53, 54, 80, 88, # Sumireko Protector
  56, 72, # Reset
  11, 40, 41, 42, 73, 74, 77, 79, 85, 89, 90, 99, 101, 103, 111, # Marisa
  84, 106, 138, # Marisa with miniboss
  81, 94, 98, 108, 117, # Reimu
  110, # Reimu with miniboss
  51, 58, 59, 82, 100, 115, 116, # Midbosses-Fragile
  4, 37, 46, 52, 92, 124, 133, # Midbosses-Fragile with miniboss
  12, 31, 37, 102, 104, 113, 118, 123, 125, # Midbosses-Unforgiven
  8, 127, # Midbosses-Unforgiven with miniboss
  34, 36, 38, 55, 93, 96, 97, 109, 112, 114, 119, 128, 129, # Midbosses-Solitary
  107, 137, # Midbosses-Solitary with miniboss
]
mats = [
  1, 6, 14, 23, 33, 39, 41, 45, 59, # Cirno
  29, 57, 61, # Nightmare
  25, 37, 49, 62, # Horde
  11, 12, # Sumireko Protector
  30, 63, 71, # Reset
  2, 15, 19, 21, 27, 34, 35, 40, 42, 43, 47, 58, 64, # Marisa
  24, 65, # Marisa with miniboss
  26, 55, 60, # Reimu
  7, 31, # Midbosses-Fragile
  3, 17, 50, # Midbosses-Fragile with miniboss
  18, 38, 48, 51, 66, # Midbosses-Unforgiven
  16, 32, 56, # Midbosses-Unforgiven with miniboss
  8, 20, 44, 46, 67, # Midbosses-Solitary
  4, 28, 52, 72, 80, # Midbosses-Solitary with miniboss
  74, 75, # Despair and Hope farming
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
    if i in main:
      f.write(bytearray([1]))
    else:
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
    if i in main:
      f.write(bytearray([0, 0, 1, 0xf4]))
    else:
      f.write(bytearray(data[(i+1000)*4:(i+1000)*4+4]))
