#!/usr/bin/env python3
"""Swap patched classes2.dex into the original APK, preserving every other
entry byte-for-byte with its original compression method."""
import zipfile, shutil, os

SRC_ORIG = "/home/z/my-project/work/app.apk"
NEW_DEX = "/home/z/my-project/work/dexout/classes2.dex"
OUT = "/home/z/my-project/work/patched_unaligned.apk"

zin = zipfile.ZipFile(SRC_ORIG, "r")
zout = zipfile.ZipFile(OUT, "w")

new_dex_bytes = open(NEW_DEX, "rb").read()

replaced = 0
for info in zin.infolist():
    data = zin.read(info.filename)
    if info.filename == "classes2.dex":
        data = new_dex_bytes
        replaced += 1
    zi = zipfile.ZipInfo(info.filename, date_time=info.date_time)
    zi.compress_type = info.compress_type  # preserve STORED/DEFLATED
    zi.external_attr = info.external_attr
    zi.internal_attr = info.internal_attr
    zi.create_system = info.create_system
    zi.comment = info.comment
    # deflate with max compression like original (which used DEFLATED level ~9)
    if zi.compress_type == zipfile.ZIP_DEFLATED:
        zout.writestr(zi, data, compress_type=zipfile.ZIP_DEFLATED, compresslevel=9)
    else:
        zout.writestr(zi, data, compress_type=zi.compress_type)
zout.close()
zin.close()

print("entries processed, replaced dex count:", replaced)
print("size:", os.path.getsize(OUT))

# verify: all entries identical except classes2.dex
za = zipfile.ZipFile(SRC_ORIG)
zb = zipfile.ZipFile(OUT)
na, nb = set(za.namelist()), set(zb.namelist())
assert na == nb, f"entry mismatch: {na ^ nb}"
diffs = [n for n in za.namelist() if za.read(n) != zb.read(n)]
print("differing entries (should be only classes2.dex):", diffs)
assert diffs == ["classes2.dex"]
# compress types preserved?
for info in za.infolist():
    ib = zb.getinfo(info.filename)
    assert ib.compress_type == info.compress_type, info.filename
print("compress types preserved: OK")
