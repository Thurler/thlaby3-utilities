alphabet = ' 123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
#           00000000001111111111222222222233333333334444444444555555555566
#           01234567890123456789012345678901234567890123456789012345678901

with open("data/0601_OD.txt", "rb") as fi:
  with open("out_OD.txt", 'w') as fo:
    for i in range(150):
      for j in range(150):
        s = fi.read(1)
        fo.write(alphabet[s[0]])
      fo.write('\n')

with open("data/0601_B.txt", 'r') as fi:
  with open("out_B.txt", 'w') as fo:
    for i in range(150):
      line = fi.readline().split(',')[:-1]
      for j in range(150):
        if int(line[j]) >= 0:
          fo.write(alphabet[int(line[j])])
      fo.write('\n')

with open("data/0601_G.txt", 'r') as fi:
  with open("out_G.txt", 'w') as fo:
    for i in range(150):
      line = fi.readline().split(',')[:-1]
      for j in range(150):
        if int(line[j]) >= 0:
          fo.write(alphabet[int(line[j])])
      fo.write('\n')

with open("data/0601_H.txt", 'r') as fi:
  with open("out_H.txt", 'w') as fo:
    for i in range(150):
      line = fi.readline().split(',')[:-1]
      for j in range(150):
        if int(line[j]) >= 0:
          fo.write(alphabet[int(line[j])])
      fo.write('\n')

with open("data/0601_M.txt", 'r') as fi:
  with open("out_M.txt", 'w') as fo:
    for i in range(150):
      line = fi.readline().split(',')[:-1]
      for j in range(150):
        if int(line[j]) >= 0:
          fo.write(alphabet[int(line[j])])
      fo.write('\n')
