#!/usr/bin/env python3
"""Remove social networks/channels + about-us/copyright sections from
SettingsAndAboutScreenKt.smali of DrMobile (پزشک گوشی) APK."""
import sys

PATH = "/home/z/my-project/work/decoded/smali_classes2/com/example/ui/screens/SettingsAndAboutScreenKt.smali"

def esc(s: str) -> str:
    out = []
    for ch in s:
        if 0x20 <= ord(ch) < 0x7F:
            out.append(ch)
        else:
            out.append("\\u%04x" % ord(ch))
    return "".join(out)

with open(PATH, encoding="utf-8") as f:
    lines = f.readlines()

# ---- Edit 1: delete the 6 unwanted LazyColumn items (lines 3387..3476, 1-based) ----
start, end = 3387, 3476  # inclusive
assert lines[start - 1].strip() == ".line 140", f"line 3387 unexpected: {lines[start-1]!r}"
assert ".line 275" in lines[end + 1 - 1], f"line 3477 unexpected: {lines[end]!r}"
assert lines[end - 1].strip() == "", f"line 3476 unexpected: {lines[end-1]!r}"
del lines[start - 1 : end]

# ---- Edit 2: retitle the screen (old title/subtitle mention removed sections) ----
txt = "".join(lines)
old_title = '"\\u0627\\u0637\\u0644\\u0627\\u0639\\u0627\\u062a \\u0648 \\u062f\\u0631\\u0628\\u0627\\u0631\\u0647 \\u0645\\u0627"'
new_title = '"' + esc("اطلاعات و امکانات") + '"'
old_sub = '"\\u0627\\u0645\\u06a9\\u0627\\u0646\\u0627\\u062a\\u060c \\u0634\\u0628\\u06a9\\u0647\\u200c\\u0647\\u0627\\u06cc \\u0627\\u062c\\u062a\\u0645\\u0627\\u0639\\u06cc \\u0648 \\u06a9\\u067e\\u06cc\\u200c\\u0631\\u0627\\u06cc\\u062a"'
new_sub = '"' + esc("امکانات، امتیازدهی و سایر برنامه‌ها") + '"'
assert txt.count(old_title) == 1, f"title occurrences: {txt.count(old_title)}"
assert txt.count(old_sub) == 1, f"subtitle occurrences: {txt.count(old_sub)}"
txt = txt.replace(old_title, new_title).replace(old_sub, new_sub)

with open(PATH, "w", encoding="utf-8") as f:
    f.write(txt)

# ---- sanity checks ----
final = txt.splitlines()
kept_items = sum(1 for l in final if "item$default" in l)
print("item$default calls now in file:", kept_items)
removed_markers = ["-2030248531", "-1495900887", "ExternalSyntheticLambda10;", "ExternalSyntheticLambda12;",
                   "ExternalSyntheticLambda13;", "ExternalSyntheticLambda14;"]
for marker in removed_markers:
    n = sum(1 for l in final if marker in l and "invoke" in l)
    print(f"  refs to {marker}: {n} (expect 0)")
print("new title present:", new_title in txt, "| new subtitle present:", new_sub in txt)
print("OK")
