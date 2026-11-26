# KHSahibi VDownloader

A modern Android app built with Python/KivyMD for downloading video, audio, and images from any website.

## Features

- **Multi-platform support**: Download from YouTube, TikTok, Instagram, Twitter/X, Facebook, and 1000+ sites using yt-dlp
- **Media types**: Download video, audio, and images
- **Format selection**: Choose quality and format before downloading
- **Download management**: View history, cancel ongoing downloads, open downloaded files
- **Material Design UI**: Beautiful dark/light theme with Material You dynamic colors
- **Clipboard integration**: Paste URL from clipboard automatically
- **Download history**: Track all downloads, view progress, and manage files

## Screens

1. **Main** - URL input, quick action buttons, download progress list
2. **Settings** - Appearance, download preferences, network settings
3. **History** - View and manage past downloads

## Installation

### From Source

```bash
# Install dependencies
pip install -r requirements.txt

# Run the app
python main.py
```

### Buildozer (Android APK)

1. Install buildozer: `pip install buildozer`
2. Configure your Android development environment
3. Build: `buildozer android debug apk`
4. Install the APK on your device

## Usage

1. Paste any video/audio/image URL in the input field
2. Tap "Analyze & Download" to see available formats
3. Select your preferred quality and format
4. Wait for download to complete
5. View downloaded files in the History screen

## Supported Sites

Supports over 1000 websites including:
- YouTube, YouTube Music
- TikTok, Instagram, Twitter/X, Facebook
- Vimeo, Dailymotion, Twitch
- SoundCloud, Spotify (audio extraction)
- And many more via yt-dlp

## License

MIT License - feel free to modify and distribute