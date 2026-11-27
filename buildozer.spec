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
requirements = python3==3.11.5,hostpython3==3.11.5,kivy=2.3.0,kivymd,p4a.branch=v2024.01.21,materialyoucolor,asynckivy,asyncgui,yt-dlp,requests,certifi,urllib3,idna,charset-normalizer,ffmpeg

# Android settings
android.api = 36
android.minapi = 24
android.ndk = 25b
android.ndk_api = 27
android.archs = arm64-v8a

# Keeps first builds smaller
android.accept_sdk_license = True
android.allow_backup = True

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,FOREGROUND_SERVICE,FOREGROUND_SERVICE_MEDIA_PROJECTION,POST_NOTIFICATIONS,READ_MEDIA_VIDEO,READ_MEDIA_IMAGES,READ_MEDIA_AUDIO

# Features
android.features = android.hardware.touchscreen

# Orientation
orientation = portrait

# Kivy settings
kivy_garden_requirements =

# Python-for-Android
p4a.branch = v2024.01.21
p4a.bootstrap = sdl2

# Log level
log_level = 2

# Warn on root
warn_on_root = 1

# Buildozer version
buildozer.spec_version = 1.0

[buildozer]
warn_on_root = 0
