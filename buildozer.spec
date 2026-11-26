[app]

# Application name
title = KHSahibi VDownloader

# Package name
package.name = khsahibivdownloader

# Package domain
package.domain = khsahibi.vdownloader

# Source directory
source.dir = .

# Source files to include
source.include_exts = py,kv,png,jpg,atlas,txt,xml,json,ttf

# Version
version = 1.0.0

# Requirements
requirements = python3,kivy==2.3.0,kivymd==2.0.1,yt-dlp,requests,certifi,urllib3,idna,charset-normalizer

# Android settings
android.api = 36
android.minapi = 24
android.ndk = 25b
android.ndk_api = 27
android.archs = arm64-v8a, armeabi-v7a

# Keeps first builds smaller
android.accept_sdk_license = True
android.allow_backup = True

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,FOREGROUND_SERVICE_MEDIA_PROJECTION,POST_NOTIFICATIONS,READ_MEDIA_VIDEO,READ_MEDIA_IMAGES,READ_MEDIA_AUDIO

# Features
android.features = android.hardware.touchscreen

# Presplash
android.presplash = presplash.png

# Icon / presplash are optional - comment out if the files are missing,
# buildozer errors out when a listed asset does not exist.
# android.presplash = assets/presplash.png
# android.icon = assets/icon.png

# Orientation
orientation = portrait

# Kivy settings
kivy_garden_requirements =

# Python-for-Android
p4a.branch = master
p4a.bootstrap = sdl2

# Log level
log_level = 2

# Warn on root
warn_on_root = 1

# Buildozer version
buildozer.spec_version = 1.0

[buildozer]
warn_on_root = 0
