[app]

# ---------- App info ----------
title = Sahibi Budget App
package.name = sahibibudget
package.domain = sahibi.budget
version = 1.0.0

# ---------- Source ----------
source.dir = .
source.include_exts = py,kv,png,jpg,jpeg,atlas,txt,xml,json,ttf

# ---------- Requirements ----------
# Python is pinned to 3.11 (python-for-android master now builds 3.14, which breaks Kivy 2.3.0)
requirements = python3==3.11.5,hostpython3==3.11.5,kivy==2.3.0,kivymd==1.2.0,pillow,certifi,yt-dlp

# ---------- Display ----------
orientation = portrait
fullscreen = 0

# ---------- Android ----------
android.permissions = INTERNET,ACCESS_NETWORK_STATE,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE,FOREGROUND_SERVICE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.build_tools_version = 33.0.1
android.archs = arm64-v8a
android.private_storage = True
android.accept_sdk_license = True

# ---------- python-for-android ----------
p4a.branch = v2024.01.21

[buildozer]
log_level = 2
warn_on_root = 1
