import os

target = ""
compare = ""

dirs = []
for f in os.listdir('.'):
  if '.' not in f:
    dirs.append(f)

if target == "":
  target = dirs[-2]
if compare == "":
  compare = dirs[-1]

print_target = False
print_compare = False
print_flag_diff = True
print_data_diff = True

ignore_data = [
  [0x4, 0xc3],
  [0x190, 0x1ef],
  [0x1f4, 0x203],
  [0x844, 0xac3],
  [0x1114, 0x15c3],
  [0x4d64, 0x4e77],
  [0x5260, 0x526f],
]

def flag_to_int(flag):
  return flag[3] + (flag[2] * 256) + (flag[1] * 65536) + (flag[0] * 16777216)

def read_flags(filename, will_print):
  flags = []
  with open(filename + "/EVF01.ngd", "rb") as f:
    for i in range(30000):
      flag = flag_to_int(f.read(4))
      if flag > 0 and will_print:
        print("FLAG", i + 1, "SET TO", flag)
      flags.append(flag)
  return flags

def read_gamedata(filename):
  data = []
  with open(filename + "/PGD01.ngd", "rb") as f:
    for i in range(30008):
      data.append(f.read(1)[0])
  return data

target_flags = read_flags(target, print_target)
compare_flags = read_flags(compare, print_compare)

for i in range(30000):
  if target_flags[i] != compare_flags[i] and print_flag_diff:
    print("DIFF AT FLAG", i + 1, "WAS", target_flags[i], "IS", compare_flags[i])

target_data = read_gamedata(target)
compare_data = read_gamedata(compare)

for i in range(30008):
  skip = False
  for ignore in ignore_data:
    if i >= ignore[0] and i <= ignore[1]:
      skip = True
  if skip: continue
  if target_data[i] != compare_data[i] and print_data_diff:
    print("DATA AT", hex(i), "WAS", target_data[i], "IS", compare_data[i])
