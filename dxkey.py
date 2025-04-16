# This script will generate the DXExtract key for a given password

password = "HyperGigaAnalSmasher" # Yes this is password 3peso chose

pbytes = [ord(x) for x in password[:12]]
kbytes = pbytes[::]
kbytes[0] = 255 - pbytes[0]
kbytes[1] = (pbytes[1] >> 4) | ((pbytes[1] << 4) % 256)
kbytes[2] = pbytes[2] ^ 0x8a
kbytes[3] = 255 - ((pbytes[3] >> 4) | ((pbytes[3] << 4) % 256))
kbytes[4] = 255 - pbytes[4]
kbytes[5] = pbytes[5] ^ 0xac
kbytes[6] = 255 - pbytes[6]
kbytes[7] = 255 - ((pbytes[7] >> 3) | ((pbytes[7] << 5) % 256))
kbytes[8] = (pbytes[8] >> 5) | ((pbytes[8] << 3) % 256)
kbytes[9] = pbytes[9] ^ 0x7f
kbytes[10] = ((pbytes[10] >> 4) | ((pbytes[10] << 4) % 256)) ^ 0xd6
kbytes[11] = pbytes[11] ^ 0xcc

print(password)
print(kbytes)
print([hex(x)[2:].upper().zfill(2) for x in kbytes])
print("0x" + ''.join([hex(x)[2:].upper().zfill(2) for x in kbytes]))
