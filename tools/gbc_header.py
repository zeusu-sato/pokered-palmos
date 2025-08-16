#!/usr/bin/env python3
import sys, pathlib

def read_u8(b, off): return b[off]
def read_u16be(b, off): return (b[off] << 8) | b[off+1]

CART_TYPE = {
  0x00:"ROM ONLY", 0x01:"MBC1", 0x02:"MBC1+RAM", 0x03:"MBC1+RAM+BATTERY",
  0x05:"MBC2", 0x06:"MBC2+BATTERY", 0x08:"ROM+RAM", 0x09:"ROM+RAM+BATTERY",
  0x0B:"MMM01", 0x0C:"MMM01+RAM", 0x0D:"MMM01+RAM+BATTERY",
  0x0F:"MBC3+TIMER+BATTERY", 0x10:"MBC3+TIMER+RAM+BATTERY",
  0x11:"MBC3", 0x12:"MBC3+RAM", 0x13:"MBC3+RAM+BATTERY",
  0x19:"MBC5", 0x1A:"MBC5+RAM", 0x1B:"MBC5+RAM+BATTERY",
  0x1C:"MBC5+RUMBLE", 0x1D:"MBC5+RUMBLE+RAM", 0x1E:"MBC5+RUMBLE+RAM+BATTERY",
  0x20:"MBC6", 0x22:"MBC7+SENSOR+RUMBLE+RAM+BATTERY",
  0xFC:"POCKET CAMERA", 0xFD:"BANDAI TAMA5", 0xFE:"HuC3", 0xFF:"HuC1+RAM+BATTERY",
}
ROM_SIZE = {
  0x00:("32 KiB",2), 0x01:("64 KiB",4), 0x02:("128 KiB",8), 0x03:("256 KiB",16),
  0x04:("512 KiB",32), 0x05:("1 MiB",64), 0x06:("2 MiB",128), 0x07:("4 MiB",256),
  0x08:("8 MiB",512), 0x52:("1.1 MiB",72), 0x53:("1.2 MiB",80), 0x54:("1.5 MiB",96),
}
RAM_SIZE = {
  0x00:"None", 0x01:"2 KiB", 0x02:"8 KiB", 0x03:"32 KiB (4×8KiB)", 0x04:"128 KiB (16×8KiB)", 0x05:"64 KiB (8×8KiB)"
}

def header_checksum(b):
  x = 0
  for i in range(0x0134, 0x014D):
    x = (x - b[i] - 1) & 0xFF
  return x

def global_checksum(b):
  total = sum(b[:0x014E]) + sum(b[0x0150:])
  return total & 0xFFFF

def main():
  if len(sys.argv) < 2:
    print("Usage: gbc_header.py <rom.gbc>", file=sys.stderr); sys.exit(2)
  p = pathlib.Path(sys.argv[1])
  data = p.read_bytes()
  if len(data) < 0x150:
    print("ROM too small.", file=sys.stderr); sys.exit(1)

  title_raw = data[0x0134:0x0143]  # simple view
  title = title_raw.rstrip(b"\x00").decode("ascii", "ignore")

  cgb = read_u8(data, 0x0143)
  new_lic = data[0x0144:0x0146].decode("ascii", "ignore")
  sgb = read_u8(data, 0x0146)
  cart = read_u8(data, 0x0147)
  romc = read_u8(data, 0x0148)
  ramc = read_u8(data, 0x0149)
  dest = read_u8(data, 0x014A)
  old_lic = read_u8(data, 0x014B)
  ver = read_u8(data, 0x014C)
  head_chk = read_u8(data, 0x014D)
  glob_chk = read_u16be(data, 0x014E)

  head_calc = header_checksum(data)
  glob_calc = global_checksum(data)

  print(f"File           : {p.name} ({len(data)/1024/1024:.2f} MiB)")
  print(f"Title          : {title}")
  print(f"CGB Flag       : 0x{cgb:02X} ({'CGB-only' if cgb==0xC0 else 'CGB support' if cgb&0x80 else 'DMG compatible'})")
  print(f"SGB Flag       : 0x{sgb:02X} ({'SGB functions' if sgb==0x03 else 'No SGB'})")
  print(f"Cartridge Type : 0x{cart:02X} ({CART_TYPE.get(cart,'Unknown')})")
  rom_txt, banks = ROM_SIZE.get(romc, (f'Unknown code 0x{romc:02X}', None))
  print(f"ROM Size       : {rom_txt}{'' if banks is None else f' ({banks} banks)'}")
  print(f"RAM Size       : {RAM_SIZE.get(ramc, f'Unknown code 0x{ramc:02X}')}")
  print(f"Destination    : 0x{dest:02X} ({'Japanese' if dest==0x00 else 'Non-Japanese'})")
  print(f"New Licensee   : '{new_lic}'  Old: 0x{old_lic:02X}")
  print(f"ROM Version    : {ver}")
  print(f"Header Chksum  : 0x{head_chk:02X} (calc 0x{head_calc:02X})  -> {'OK' if head_chk==head_calc else 'MISMATCH'}")
  print(f"Global Chksum  : 0x{glob_chk:04X} (calc 0x{glob_calc:04X}) -> {'OK' if glob_chk==glob_calc else 'MISMATCH'}")

if __name__ == "__main__":
  main()
