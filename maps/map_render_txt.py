with open("data/0101_OD.txt", "rb") as fi:
  with open("out_OD.txt", 'w') as fo:
    for i in range(150):
      for j in range(150):
        s = fi.read(1)
        fo.write('#' if s[0] == 2 else ' ')
      fo.write('\n')

with open("data/0101_B.txt", 'r') as fi:
  with open("out_B.txt", 'w') as fo:
    for i in range(150):
      line = fi.readline().split(',')[:-1]
      for j in range(150):
        fo.write(line[j] if line[j] != '0' else ' ')
      fo.write('\n')

with open("data/0101_G.txt", 'r') as fi:
  with open("out_G.txt", 'w') as fo:
    for i in range(150):
      line = fi.readline().split(',')[:-1]
      for j in range(150):
        fo.write(hex(int(line[j]))[2:] if line[j] != '0' else ' ')
      fo.write('\n')

with open("data/0101_H.txt", 'r') as fi:
  with open("out_H.txt", 'w') as fo:
    for i in range(150):
      line = fi.readline().split(',')[:-1]
      for j in range(150):
        fo.write(line[j] if line[j] != '0' else ' ')
      fo.write('\n')

with open("data/0101_M.txt", 'r') as fi:
  with open("out_M.txt", 'w') as fo:
    for i in range(150):
      line = fi.readline().split(',')[:-1]
      for j in range(150):
        fo.write(line[j] if line[j] != '0' else ' ')
      fo.write('\n')
