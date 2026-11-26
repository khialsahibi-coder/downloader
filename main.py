#!/usr/bin/env python
"""
KHSahibi VDownloader - Modern Android Video/Audio/Image Downloader
Built with KivyMD for beautiful Material Design UI
"""

import os
import sys
import threading
import json
import re
from pathlib import Path
from datetime import datetime
from typing import Optional, Dict, List, Any

# Kivy imports
import kivy
kivy.require('2.3.0')

from kivy.lang import Builder
from kivy.clock import Clock, mainthread
from kivy.properties import StringProperty, ListProperty, NumericProperty, BooleanProperty, ObjectProperty
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.metrics import dp, sp
from kivy.utils import platform
from kivy.logger import Logger

# KivyMD imports
from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDButton, MDButtonText, MDIconButton, MDFabButton
from kivymd.uix.textfield import MDTextField, MDTextFieldHintText, MDTextFieldHelperText, MDTextFieldMaxLengthText
from kivymd.uix.label import MDLabel, MDIcon
from kivymd.uix.card import MDCard
from kivymd.uix.list import MDListItem, MDListItemHeadlineText, MDListItemSupportingText, MDListItemLeadingIcon, MDListItemTrailingIcon
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogSupportingText, MDDialogButtonContainer
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.bottomsheet import MDBottomSheet, MDBottomSheetDragHandle, MDBottomSheetContent
from kivymd.uix.chip import MDChip, MDChipText
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.toolbar import MDTopAppBar, MDTopAppBarTitle, MDTopAppBarLeadingButtonContainer, MDTopAppBarTrailingButtonContainer
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.divider import MDDivider
from kivymd.uix.relativelayout import MDRelativeLayout
from kivymd.icon_definitions import md_icons

# Python standard library
import yt_dlp
import requests

# ============================================================================
# KV Language UI Definition
# ============================================================================

KV = '''
#:import md_icons kivymd.icon_definitions.md_icons
#:import Clipboard kivy.core.clipboard.Clipboard

<DownloadItem@MDCard>:
    orientation: "vertical"
    size_hint_y: None
    height: dp(120)
    padding: dp(12)
    spacing: dp(8)
    elevation: 1
    radius: [dp(16),]
    md_bg_color: app.theme_cls.surfaceContainerLowColor

    MDBoxLayout:
        orientation: "horizontal"
        spacing: dp(12)

        MDBoxLayout:
            orientation: "vertical"
            size_hint_x: 0.6
            spacing: dp(2)

            MDLabel:
                id: title_label
                text: "Loading..."
                font_style: "titleSmall"
                bold: True
                shorten: True
                shorten_from: "right"

            MDLabel:
                id: url_label
                text: "https://example.com/video"
                font_style: "labelSmall"
                theme_text_color: "Hint"
                shorten: True
                shorten_from: "right"

            MDLabel:
                id: meta_label
                text: "Video • 1080p • 45.2 MB"
                font_style: "labelSmall"
                theme_text_color: "Hint"

        MDBoxLayout:
            orientation: "vertical"
            size_hint_x: 0.4
            spacing: dp(4)
            padding: [0, dp(4), 0, 0]

            MDProgressBar:
                id: progress_bar
                value: 0
                type: "determinate"
                color: app.theme_cls.primaryColor
                size_hint_y: None
                height: dp(6)
                radius: [dp(3),]

            MDLabel:
                id: status_label
                text: "Pending"
                font_style: "labelSmall"
                theme_text_color: "Hint"
                halign: "right"

            MDBoxLayout:
                orientation: "horizontal"
                spacing: dp(8)
                size_hint_y: None
                height: dp(36)
                padding: [0, dp(4), 0, 0]

                MDIconButton:
                    id: pause_btn
                    icon: "pause"
                    theme_icon_color: "Custom"
                    icon_color: app.theme_cls.onSurfaceVariantColor
                    on_release: root.pause_download()
                    disabled: True

                MDIconButton:
                    id: cancel_btn
                    icon: "close"
                    theme_icon_color: "Custom"
                    icon_color: app.theme_cls.onSurfaceVariantColor
                    on_release: root.cancel_download()

                MDIconButton:
                    id: open_btn
                    icon: "folder-open"
                    theme_icon_color: "Custom"
                    icon_color: app.theme_cls.primaryColor
                    on_release: root.open_file()
                    disabled: True

<FormatChip@MDChip>:
    checkable: True
    type: "filter"
    on_active: root.on_chip_active(self, self.active)

<MainScreen>:
    md_bg_color: app.theme_cls.surfaceColor

    MDBoxLayout:
        orientation: "vertical"

        # Top App Bar
        MDTopAppBar:
            id: top_bar
            type: "small"
            elevation: 0
            md_bg_color: app.theme_cls.surfaceColor

            MDTopAppBarLeadingButtonContainer:
                MDIconButton:
                    icon: "menu"
                    on_release: app.open_drawer()

            MDTopAppBarTitle:
                text: "KHSahibi VDownloader"
                font_style: "titleMedium"

            MDTopAppBarTrailingButtonContainer:
                MDIconButton:
                    icon: "theme-light-dark"
                    on_release: app.toggle_theme()
                MDIconButton:
                    icon: "cog"
                    on_release: app.open_settings()

        # Main Content
        MDScrollView:
            MDBoxLayout:
                id: main_content
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(16)
                adaptive_height: True

                # URL Input Card
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)
                    elevation: 0
                    radius: [dp(20),]
                    md_bg_color: app.theme_cls.surfaceContainerHighColor

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(12)
                        adaptive_height: True

                        MDTextField:
                            id: url_field
                            hint_text: "Paste video, audio, or image URL here..."
                            helper_text: "Supports YouTube, TikTok, Instagram, Twitter, Facebook, and 1000+ sites"
                            helper_text_mode: "on_focus"
                            mode: "outlined"
                            size_hint_x: 0.85
                            max_text_length: 2048

                            MDTextFieldHintText:
                                text: "Paste URL or tap paste button"

                            MDTextFieldHelperText:
                                text: "Supports YouTube, TikTok, Instagram, Twitter, Facebook, and 1000+ sites"
                                mode: "on_focus"

                        MDIconButton:
                            id: paste_btn
                            icon: "content-paste"
                            theme_icon_color: "Custom"
                            icon_color: app.theme_cls.primaryColor
                            on_release: app.paste_from_clipboard()
                            size_hint: None, None
                            size: dp(48), dp(48)

                    # Quick action chips
                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(8)
                        adaptive_height: True

                        MDLabel:
                            text: "Quick Actions:"
                            font_style: "labelSmall"
                            theme_text_color: "Hint"
                            size_hint_x: None
                            width: dp(100)
                            valign: "center"

                        MDIconButton:
                            icon: "camera"
                            theme_icon_color: "Custom"
                            icon_color: app.theme_cls.primaryColor
                            on_release: app.quick_download("image")
                            size_hint: None, None
                            size: dp(40), dp(40)
                            md_bg_color: app.theme_cls.primaryContainerColor
                            radius: [dp(20),]

                        MDIconButton:
                            icon: "music"
                            theme_icon_color: "Custom"
                            icon_color: app.theme_cls.primaryColor
                            on_release: app.quick_download("audio")
                            size_hint: None, None
                            size: dp(40), dp(40)
                            md_bg_color: app.theme_cls.primaryContainerColor
                            radius: [dp(20),]

                        MDIconButton:
                            icon: "video"
                            theme_icon_color: "Custom"
                            icon_color: app.theme_cls.primaryColor
                            on_release: app.quick_download("video")
                            size_hint: None, None
                            size: dp(40), dp(40)
                            md_bg_color: app.theme_cls.primaryContainerColor
                            radius: [dp(20),]

                # Download Button
                MDButton:
                    id: download_btn
                    style: "filled"
                    theme_width: "Custom"
                    size_hint_x: 1
                    height: dp(56)
                    on_release: app.start_download()
                    md_bg_color: app.theme_cls.primaryColor
                    disabled: True

                    MDButtonText:
                        id: download_btn_text
                        text: "Analyze & Download"
                        font_style: "titleSmall"

                # Divider
                MDDivider:

                # Downloads List Header
                MDBoxLayout:
                    orientation: "horizontal"
                    spacing: dp(8)
                    adaptive_height: True
                    padding: [dp(4), dp(8), dp(4), dp(4)]

                    MDLabel:
                        text: "Downloads"
                        font_style: "titleMedium"
                        bold: True

                    MDLabel:
                        id: download_count
                        text: "(0)"
                        font_style: "titleMedium"
                        theme_text_color: "Hint"

                # Downloads List
                MDBoxLayout:
                    id: downloads_list
                    orientation: "vertical"
                    spacing: dp(12)
                    adaptive_height: True
                    size_hint_y: None
                    height: self.minimum_height

                # Empty State
                MDBoxLayout:
                    id: empty_state
                    orientation: "vertical"
                    spacing: dp(16)
                    padding: dp(32)
                    adaptive_height: True
                    size_hint_x: 1

                    MDIcon:
                        icon: "download-circle"
                        font_size: dp(64)
                        theme_icon_color: "Hint"
                        halign: "center"

                    MDLabel:
                        text: "No downloads yet"
                        font_style: "headlineSmall"
                        halign: "center"
                        theme_text_color: "Hint"

                    MDLabel:
                        text: "Paste a URL above to start downloading videos, audio, or images from any website"
                        font_style: "bodyMedium"
                        halign: "center"
                        theme_text_color: "Hint"
                        padding: [dp(24), 0, dp(24), 0]

<FormatBottomSheet>:
    orientation: "vertical"
    spacing: dp(16)
    padding: dp(16)
    adaptive_height: True

    MDBottomSheetDragHandle:
        id: drag_handle

    MDBottomSheetContent:
        orientation: "vertical"
        spacing: dp(16)
        adaptive_height: True

        MDLabel:
            text: "Select Format & Quality"
            font_style: "titleLarge"
            bold: True

        MDDivider:

        MDLabel:
            text: "Video Formats"
            font_style: "titleSmall"
            bold: True

        MDBoxLayout:
            id: video_formats_container
            orientation: "vertical"
            spacing: dp(8)
            adaptive_height: True

        MDDivider:

        MDLabel:
            text: "Audio Formats"
            font_style: "titleSmall"
            bold: True

        MDBoxLayout:
            id: audio_formats_container
            orientation: "vertical"
            spacing: dp(8)
            adaptive_height: True

        MDDivider:

        MDLabel:
            text: "Image Formats"
            font_style: "titleSmall"
            bold: True

        MDBoxLayout:
            id: image_formats_container
            orientation: "vertical"
            spacing: dp(8)
            adaptive_height: True

        MDBoxLayout:
            orientation: "horizontal"
            spacing: dp(12)
            padding: [0, dp(16), 0, 0]

            MDButton:
                style: "text"
                on_release: root.dismiss()

                MDButtonText:
                    text: "Cancel"

            MDButton:
                style: "filled"
                on_release: root.confirm_selection()

                MDButtonText:
                    text: "Download"

<SettingsScreen>:
    md_bg_color: app.theme_cls.surfaceColor

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            type: "small"
            elevation: 0
            md_bg_color: app.theme_cls.surfaceColor

            MDTopAppBarLeadingButtonContainer:
                MDIconButton:
                    icon: "arrow-left"
                    on_release: app.switch_screen("main")

            MDTopAppBarTitle:
                text: "Settings"

        MDScrollView:
            MDBoxLayout:
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(24)
                adaptive_height: True

                # Appearance Section
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)
                    elevation: 0
                    radius: [dp(16),]
                    md_bg_color: app.theme_cls.surfaceContainerHighColor

                    MDLabel:
                        text: "Appearance"
                        font_style: "titleMedium"
                        bold: True

                    MDDivider:

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(12)
                        adaptive_height: True

                        MDLabel:
                            text: "Dark Mode"
                            font_style: "bodyLarge"
                            size_hint_x: 0.7

                        MDIconButton:
                            id: theme_toggle
                            icon: "theme-light-dark"
                            theme_icon_color: "Custom"
                            icon_color: app.theme_cls.primaryColor
                            on_release: app.toggle_theme()

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(12)
                        adaptive_height: True

                        MDLabel:
                            text: "Dynamic Colors (Material You)"
                            font_style: "bodyLarge"
                            size_hint_x: 0.7

                        MDCheckbox:
                            id: dynamic_colors
                            active: True
                            on_active: app.set_dynamic_colors(self.active)

                # Downloads Section
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)
                    elevation: 0
                    radius: [dp(16),]
                    md_bg_color: app.theme_cls.surfaceContainerHighColor

                    MDLabel:
                        text: "Downloads"
                        font_style: "titleMedium"
                        bold: True

                    MDDivider:

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(12)
                        adaptive_height: True

                        MDLabel:
                            text: "Download Folder"
                            font_style: "bodyLarge"
                            size_hint_x: 0.7

                        MDLabel:
                            id: download_path_label
                            text: "/storage/emulated/0/Download/KHSahibi"
                            font_style: "bodyMedium"
                            theme_text_color: "Hint"
                            size_hint_x: 0.3
                            halign: "right"

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(12)
                        adaptive_height: True

                        MDLabel:
                            text: "Auto-detect Format"
                            font_style: "bodyLarge"
                            size_hint_x: 0.7

                        MDCheckbox:
                            id: auto_format
                            active: True

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(12)
                        adaptive_height: True

                        MDLabel:
                            text: "Download Thumbnails"
                            font_style: "bodyLarge"
                            size_hint_x: 0.7

                        MDCheckbox:
                            id: download_thumbs
                            active: True

                # Network Section
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)
                    elevation: 0
                    radius: [dp(16),]
                    md_bg_color: app.theme_cls.surfaceContainerHighColor

                    MDLabel:
                        text: "Network"
                        font_style: "titleMedium"
                        bold: True

                    MDDivider:

                    MDBoxLayout:
                        orientation: "horizontal"
                        spacing: dp(12)
                        adaptive_height: True

                        MDLabel:
                            text: "Max Concurrent Downloads"
                            font_style: "bodyLarge"
                            size_hint_x: 0.7

                        MDLabel:
                            id: concurrent_label
                            text: "3"
                            font_style: "bodyMedium"
                            theme_text_color: "Hint"
                            size_hint_x: 0.3
                            halign: "right"

                    MDProgressBar:
                        id: concurrent_slider
                        value: 3
                        min: 1
                        max: 5
                        on_touch_up: app.set_concurrent_downloads(int(self.value))

                # About Section
                MDCard:
                    orientation: "vertical"
                    padding: dp(16)
                    spacing: dp(12)
                    elevation: 0
                    radius: [dp(16),]
                    md_bg_color: app.theme_cls.surfaceContainerHighColor

                    MDLabel:
                        text: "About"
                        font_style: "titleMedium"
                        bold: True

                    MDDivider:

                    MDBoxLayout:
                        orientation: "vertical"
                        spacing: dp(8)
                        adaptive_height: True

                        MDLabel:
                            text: "KHSahibi VDownloader v1.0.0"
                            font_style: "bodyLarge"
                            halign: "center"

                        MDLabel:
                            text: "Built with KivyMD & yt-dlp"
                            font_style: "bodyMedium"
                            theme_text_color: "Hint"
                            halign: "center"

                        MDLabel:
                            text: "Download videos, audio & images from any site"
                            font_style: "bodySmall"
                            theme_text_color: "Hint"
                            halign: "center"

<HistoryScreen>:
    md_bg_color: app.theme_cls.surfaceColor

    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            type: "small"
            elevation: 0
            md_bg_color: app.theme_cls.surfaceColor

            MDTopAppBarLeadingButtonContainer:
                MDIconButton:
                    icon: "arrow-left"
                    on_release: app.switch_screen("main")

            MDTopAppBarTitle:
                text: "Download History"

            MDTopAppBarTrailingButtonContainer:
                MDIconButton:
                    icon: "delete-sweep"
                    on_release: app.clear_history()

        MDScrollView:
            MDBoxLayout:
                id: history_list
                orientation: "vertical"
                padding: dp(16)
                spacing: dp(12)
                adaptive_height: True

<DrawerContent>:
    orientation: "vertical"
    spacing: dp(8)
    padding: dp(16)
    adaptive_height: True

    MDBoxLayout:
        orientation: "horizontal"
        spacing: dp(16)
        adaptive_height: True
        padding: [0, dp(16), 0, dp(24)]

        MDIcon:
            icon: "download-circle"
            font_size: dp(48)
            theme_icon_color: "Custom"
            icon_color: app.theme_cls.primaryColor

        MDBoxLayout:
            orientation: "vertical"
            spacing: dp(4)

            MDLabel:
                text: "KHSahibi VDownloader"
                font_style: "titleLarge"
                bold: True

            MDLabel:
                text: "v1.0.0"
                font_style: "bodyMedium"
                theme_text_color: "Hint"

    MDDivider:

    MDListItem:
        on_release: app.switch_screen("main")

        MDListItemLeadingIcon:
            icon: "home"

        MDListItemHeadlineText:
            text: "Home"

    MDListItem:
        on_release: app.switch_screen("history")

        MDListItemLeadingIcon:
            icon: "history"

        MDListItemHeadlineText:
            text: "History"

    MDListItem:
        on_release: app.switch_screen("settings")

        MDListItemLeadingIcon:
            icon: "cog"

        MDListItemHeadlineText:
            text: "Settings"

    MDDivider:

    MDListItem:
        on_release: app.open_github()

        MDListItemLeadingIcon:
            icon: "github"

        MDListItemHeadlineText:
            text: "GitHub"

        MDListItemSupportingText:
            text: "View source code"

<RootWidget>:
    MDBoxLayout:
        orientation: "horizontal"

        # Navigation Drawer
        MDNavigationDrawer:
            id: nav_drawer
            radius: [0, dp(28), dp(28), 0]

            DrawerContent:
                id: drawer_content

        # Main Content
        MDScreenManager:
            id: screen_manager

            MainScreen:
                name: "main"
                id: main_screen

            SettingsScreen:
                name: "settings"
                id: settings_screen

            HistoryScreen:
                name: "history"
                id: history_screen
'''

# ============================================================================
# Data Models
# ============================================================================

class DownloadTask:
    """Represents a download task with all its metadata"""
    def __init__(self, url: str, task_id: str = None):
        self.task_id = task_id or f"task_{datetime.now().timestamp()}"
        self.url = url
        self.title = "Analyzing..."
        self.status = "analyzing"  # analyzing, queued, downloading, paused, completed, failed
        self.progress = 0
        self.format_id = None
        self.format_note = ""
        self.filesize = 0
        self.filepath = ""
        self.thumbnail = ""
        self.media_type = "video"  # video, audio, image
        self.error = ""
        self.start_time = datetime.now()
        self.end_time = None
        self.speed = ""
        self.eta = ""

    def to_dict(self) -> Dict:
        return {
            "task_id": self.task_id,
            "url": self.url,
            "title": self.title,
            "status": self.status,
            "progress": self.progress,
            "format_id": self.format_id,
            "format_note": self.format_note,
            "filesize": self.filesize,
            "filepath": self.filepath,
            "thumbnail": self.thumbnail,
            "media_type": self.media_type,
            "error": self.error,
            "start_time": self.start_time.isoformat(),
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "speed": self.speed,
            "eta": self.eta,
        }

    @classmethod
    def from_dict(cls, data: Dict) -> 'DownloadTask':
        task = cls(data["url"], data["task_id"])
        task.title = data.get("title", "Unknown")
        task.status = data.get("status", "analyzing")
        task.progress = data.get("progress", 0)
        task.format_id = data.get("format_id")
        task.format_note = data.get("format_note", "")
        task.filesize = data.get("filesize", 0)
        task.filepath = data.get("filepath", "")
        task.thumbnail = data.get("thumbnail", "")
        task.media_type = data.get("media_type", "video")
        task.error = data.get("error", "")
        task.start_time = datetime.fromisoformat(data["start_time"]) if data.get("start_time") else datetime.now()
        task.end_time = datetime.fromisoformat(data["end_time"]) if data.get("end_time") else None
        task.speed = data.get("speed", "")
        task.eta = data.get("eta", "")
        return task


# ============================================================================
# Screens
# ============================================================================

class MainScreen(MDScreen):
    """Main download screen"""
    pass


class SettingsScreen(MDScreen):
    """Settings screen"""
    pass


class HistoryScreen(MDScreen):
    """Download history screen"""
    pass


class FormatBottomSheet(MDBottomSheet):
    """Bottom sheet for format selection"""

    def __init__(self, formats: Dict, callback, **kwargs):
        super().__init__(**kwargs)
        self.formats = formats
        self.callback = callback
        self.selected_format = None
        self.chip_widgets = []

    def on_open(self):
        self.populate_formats()

    def populate_formats(self):
        """Populate format chips for video, audio, and image"""
        app = MDApp.get_running_app()

        # Video formats
        video_container = self.ids.video_formats_container
        video_container.clear_widgets()

        video_formats = self.formats.get("video", [])
        for fmt in video_formats[:8]:  # Limit to 8 options
            chip = MDChip(
                MDChipText(text=f"{fmt['note']} • {fmt.get('ext', 'mp4')} • {self.format_size(fmt.get('filesize', 0))}"),
                id=f"video_{fmt['format_id']}",
                on_active=lambda chip, active, f=fmt: self.on_format_selected(chip, active, f, "video"),
            )
            self.chip_widgets.append(chip)
            video_container.add_widget(chip)

        # Audio formats
        audio_container = self.ids.audio_formats_container
        audio_container.clear_widgets()

        audio_formats = self.formats.get("audio", [])
        for fmt in audio_formats[:5]:
            chip = MDChip(
                MDChipText(text=f"{fmt['note']} • {fmt.get('ext', 'm4a')} • {self.format_size(fmt.get('filesize', 0))}"),
                id=f"audio_{fmt['format_id']}",
                on_active=lambda chip, active, f=fmt: self.on_format_selected(chip, active, f, "audio"),
            )
            self.chip_widgets.append(chip)
            audio_container.add_widget(chip)

        # Image formats
        image_container = self.ids.image_formats_container
        image_container.clear_widgets()

        image_formats = self.formats.get("image", [])
        for fmt in image_formats[:5]:
            chip = MDChip(
                MDChipText(text=f"{fmt['note']} • {fmt.get('ext', 'jpg')}"),
                id=f"image_{fmt['format_id']}",
                on_active=lambda chip, active, f=fmt: self.on_format_selected(chip, active, f, "image"),
            )
            self.chip_widgets.append(chip)
            image_container.add_widget(chip)

    def format_size(self, size: int) -> str:
        """Format file size"""
        if not size or size == 0:
            return "Unknown size"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def on_format_selected(self, chip, active, fmt, media_type):
        """Handle format chip selection"""
        if active:
            # Deselect other chips of same media type
            for c in self.chip_widgets:
                if c != chip and c.id.startswith(f"{media_type}_"):
                    c.active = False
            self.selected_format = fmt

    def confirm_selection(self):
        """Confirm format selection and start download"""
        if self.selected_format and self.callback:
            self.callback(self.selected_format)
        self.dismiss()


# ============================================================================
# Main App
# ============================================================================

class KHSahibiVDownloader(MDApp):
    """Main application class"""

    # Properties
    current_url = StringProperty("")
    download_tasks = ListProperty([])
    active_downloads = NumericProperty(0)
    max_concurrent = NumericProperty(3)
    is_dark_theme = BooleanProperty(False)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_dir = self.get_download_dir()
        self.history_file = os.path.join(self.download_dir, "history.json")
        self.load_history()
        self.format_bottom_sheet = None
        self.pending_task = None
        self.pending_formats = None

    def get_download_dir(self) -> str:
        """Get the download directory path"""
        if platform == "android":
            from android.storage import primary_external_storage_path
            base = primary_external_storage_path()
            download_dir = os.path.join(base, "Download", "KHSahibi")
        else:
            download_dir = os.path.join(Path.home(), "Downloads", "KHSahibi")

        os.makedirs(download_dir, exist_ok=True)
        return download_dir

    def build(self):
        """Build the app"""
        self.theme_cls.theme_style = "Dark" if self.is_dark_theme else "Light"
        self.theme_cls.primary_palette = "Blue"
        self.theme_cls.material_style = "M3"

        # Load KV
        self.root = Builder.load_string(KV)
        return self.root

    def on_start(self):
        """App started"""
        self.update_download_count()
        self.check_clipboard_on_start()

    def check_clipboard_on_start(self):
        """Check clipboard for URL on start"""
        try:
            from kivy.core.clipboard import Clipboard
            text = Clipboard.paste()
            if text and self.is_valid_url(text):
                self.root.ids.main_screen.ids.url_field.text = text
                self.on_url_change(text)
        except:
            pass

    def is_valid_url(self, text: str) -> bool:
        """Check if text is a valid URL"""
        url_pattern = re.compile(
            r'^https?://'  # http:// or https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # domain
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # or ip
            r'(?::\d+)?'  # optional port
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        return bool(url_pattern.match(text.strip()))

    def on_url_change(self, text: str):
        """Handle URL field change"""
        self.current_url = text.strip()
        download_btn = self.root.ids.main_screen.ids.download_btn
        download_btn.disabled = not self.is_valid_url(self.current_url)

    def paste_from_clipboard(self):
        """Paste URL from clipboard"""
        try:
            from kivy.core.clipboard import Clipboard
            text = Clipboard.paste()
            if text and self.is_valid_url(text):
                self.root.ids.main_screen.ids.url_field.text = text
                self.on_url_change(text)
                self.show_snackbar("URL pasted from clipboard")
            else:
                self.show_snackbar("No valid URL in clipboard")
        except Exception as e:
            self.show_snackbar(f"Failed to paste: {e}")

    def quick_download(self, media_type: str):
        """Quick download with preset media type"""
        if not self.current_url or not self.is_valid_url(self.current_url):
            self.show_snackbar("Please enter a valid URL first")
            return

        self.pending_task = DownloadTask(self.current_url)
        self.pending_task.media_type = media_type
        self.analyze_url(self.pending_task, media_type)

    def start_download(self):
        """Start download process"""
        if not self.current_url or not self.is_valid_url(self.current_url):
            self.show_snackbar("Please enter a valid URL")
            return

        # Check concurrent downloads
        if self.active_downloads >= self.max_concurrent:
            self.show_snackbar(f"Max {self.max_concurrent} concurrent downloads. Wait for one to finish.")
            return

        # Create task
        task = DownloadTask(self.current_url)
        self.add_download_task(task)

        # Analyze URL first
        self.analyze_url(task)

        # Clear URL field
        self.root.ids.main_screen.ids.url_field.text = ""
        self.current_url = ""
        self.root.ids.main_screen.ids.download_btn.disabled = True

    def analyze_url(self, task: DownloadTask, media_type: str = None):
        """Analyze URL to get available formats"""
        task.status = "analyzing"
        self.update_task_ui(task)

        def analyze_thread():
            try:
                ydl_opts = {
                    'quiet': True,
                    'no_warnings': True,
                    'extract_flat': False,
                }

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(task.url, download=False)

                    # Update task info
                    task.title = info.get('title', 'Unknown Title')
                    task.thumbnail = info.get('thumbnail', '')

                    # Determine media type
                    if media_type:
                        task.media_type = media_type
                    else:
                        # Auto-detect
                        if info.get('is_live'):
                            task.media_type = "video"
                        elif info.get('duration') and info.get('duration') < 60:
                            task.media_type = "video"
                        else:
                            task.media_type = "video"

                    # Extract formats
                    formats = self.extract_formats(info)
                    self.pending_formats = formats

                    # Show format selection on main thread
                    Clock.schedule_once(lambda dt: self.show_format_selection(task, formats), 0)

            except Exception as e:
                Logger.error(f"Analysis error: {e}")
                Clock.schedule_once(lambda dt: self.on_analysis_failed(task, str(e)), 0)

        threading.Thread(target=analyze_thread, daemon=True).start()

    def extract_formats(self, info: Dict) -> Dict:
        """Extract and categorize formats from yt-dlp info"""
        formats = {"video": [], "audio": [], "image": []}

        for fmt in info.get('formats', []):
            format_id = fmt.get('format_id', '')
            ext = fmt.get('ext', '')
            vcodec = fmt.get('vcodec', 'none')
            acodec = fmt.get('acodec', 'none')
            filesize = fmt.get('filesize') or fmt.get('filesize_approx', 0)

            note = fmt.get('format_note', '')
            if not note:
                height = fmt.get('height')
                if height:
                    note = f"{height}p"
                elif fmt.get('abr'):
                    note = f"{fmt.get('abr')}kbps"
                else:
                    note = format_id

            format_info = {
                'format_id': format_id,
                'ext': ext,
                'note': note,
                'filesize': filesize,
                'vcodec': vcodec,
                'acodec': acodec,
                'height': fmt.get('height'),
                'width': fmt.get('width'),
                'fps': fmt.get('fps'),
                'abr': fmt.get('abr'),
                'tbr': fmt.get('tbr'),
            }

            # Categorize
            if vcodec != 'none' and acodec != 'none':
                formats["video"].append(format_info)
            elif vcodec != 'none':
                formats["video"].append(format_info)
            elif acodec != 'none':
                formats["audio"].append(format_info)

        # Add best options
        # Best video
        video_formats = [f for f in formats["video"] if f.get('height')]
        if video_formats:
            best_video = max(video_formats, key=lambda x: x.get('height', 0))
            formats["video"].insert(0, {**best_video, 'note': f"Best • {best_video['note']}"})

        # Best audio
        audio_formats = [f for f in formats["audio"] if f.get('abr')]
        if audio_formats:
            best_audio = max(audio_formats, key=lambda x: x.get('abr', 0))
            formats["audio"].insert(0, {**best_audio, 'note': f"Best • {best_audio['note']}"})

        # Sort video by height descending
        formats["video"].sort(key=lambda x: x.get('height', 0), reverse=True)
        # Sort audio by bitrate descending
        formats["audio"].sort(key=lambda x: x.get('abr', 0), reverse=True)

        return formats

    def show_format_selection(self, task: DownloadTask, formats: Dict):
        """Show format selection bottom sheet"""
        # Auto-select based on media type if only one option
        if task.media_type == "audio" and formats["audio"]:
            self.on_format_selected(task, formats["audio"][0])
        elif task.media_type == "image" and formats["image"]:
            self.on_format_selected(task, formats["image"][0])
        else:
            self.format_bottom_sheet = FormatBottomSheet(
                formats=formats,
                callback=lambda fmt: self.on_format_selected(task, fmt)
            )
            self.format_bottom_sheet.open()

    def on_format_selected(self, task: DownloadTask, fmt: Dict):
        """Handle format selection"""
        task.format_id = fmt['format_id']
        task.format_note = fmt['note']
        task.filesize = fmt.get('filesize', 0)

        if self.format_bottom_sheet:
            self.format_bottom_sheet.dismiss()
            self.format_bottom_sheet = None

        # Start actual download
        self.start_actual_download(task)

    def on_analysis_failed(self, task: DownloadTask, error: str):
        """Handle analysis failure"""
        task.status = "failed"
        task.error = error
        self.update_task_ui(task)
        self.show_snackbar(f"Analysis failed: {error}")

    def start_actual_download(self, task: DownloadTask):
        """Start the actual download with yt-dlp"""
        task.status = "downloading"
        self.active_downloads += 1
        self.update_task_ui(task)

        def download_thread():
            try:
                # Build ydl options
                ydl_opts = {
                    'format': task.format_id,
                    'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
                    'quiet': True,
                    'no_warnings': True,
                    'progress_hooks': [lambda d: self.progress_hook(task, d)],
                }

                # Add thumbnail download if video
                if task.media_type == "video":
                    ydl_opts['writethumbnail'] = True
                    ydl_opts['postprocessors'] = [{
                        'key': 'EmbedThumbnail',
                        'already_have_thumbnail': False,
                    }]

                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([task.url])

                # Find downloaded file
                task.filepath = self.find_downloaded_file(task.title)
                task.status = "completed"
                task.end_time = datetime.now()
                task.progress = 100

                Clock.schedule_once(lambda dt: self.on_download_complete(task), 0)

            except Exception as e:
                Logger.error(f"Download error: {e}")
                Clock.schedule_once(lambda dt: self.on_download_failed(task, str(e)), 0)
            finally:
                self.active_downloads -= 1

        threading.Thread(target=download_thread, daemon=True).start()

    def progress_hook(self, task: DownloadTask, d: Dict):
        """Progress hook for yt-dlp"""
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)

            if total > 0:
                task.progress = int((downloaded / total) * 100)

            task.speed = d.get('_speed_str', '')
            task.eta = d.get('_eta_str', '')

            Clock.schedule_once(lambda dt: self.update_task_ui(task), 0)

    def find_downloaded_file(self, title: str) -> str:
        """Find the downloaded file"""
        try:
            files = list(Path(self.download_dir).glob(f"{title}.*"))
            if files:
                return str(max(files, key=lambda f: f.stat().st_mtime))
        except:
            pass
        return ""

    def on_download_complete(self, task: DownloadTask):
        """Handle download completion"""
        self.update_task_ui(task)
        self.save_history()
        self.show_snackbar(f"Downloaded: {task.title}")

    def on_download_failed(self, task: DownloadTask, error: str):
        """Handle download failure"""
        task.status = "failed"
        task.error = error
        self.update_task_ui(task)
        self.show_snackbar(f"Download failed: {error}")

    def add_download_task(self, task: DownloadTask):
        """Add a download task to the list"""
        self.download_tasks.append(task.to_dict())
        self.create_task_widget(task)
        self.update_download_count()
        self.hide_empty_state()

    def create_task_widget(self, task: DownloadTask):
        """Create UI widget for download task"""
        from kivy.factory import Factory

        downloads_list = self.root.ids.main_screen.ids.downloads_list

        # Create card widget
        card = MDCard(
            orientation="vertical",
            size_hint_y=None,
            height=dp(120),
            padding=dp(12),
            spacing=dp(8),
            elevation=1,
            radius=[dp(16),],
            md_bg_color=self.theme_cls.surfaceContainerLowColor,
        )

        # Store task reference
        card.task = task
        card.task_id = task.task_id

        # Layout
        main_layout = MDBoxLayout(orientation="horizontal", spacing=dp(12))

        # Left side - info
        left_layout = MDBoxLayout(orientation="vertical", size_hint_x=0.6, spacing=dp(2))

        title_label = MDLabel(
            id="title_label",
            text=task.title,
            font_style="titleSmall",
            bold=True,
            shorten=True,
            shorten_from="right",
        )

        url_label = MDLabel(
            id="url_label",
            text=task.url[:50] + "..." if len(task.url) > 50 else task.url,
            font_style="labelSmall",
            theme_text_color="Hint",
            shorten=True,
            shorten_from="right",
        )

        meta_text = f"{task.media_type.capitalize()} • {task.format_note}"
        if task.filesize > 0:
            meta_text += f" • {self.format_size(task.filesize)}"

        meta_label = MDLabel(
            id="meta_label",
            text=meta_text,
            font_style="labelSmall",
            theme_text_color="Hint",
        )

        left_layout.add_widget(title_label)
        left_layout.add_widget(url_label)
        left_layout.add_widget(meta_label)

        # Right side - progress and controls
        right_layout = MDBoxLayout(orientation="vertical", size_hint_x=0.4, spacing=dp(4), padding=[0, dp(4), 0, 0])

        progress_bar = MDProgressBar(
            id="progress_bar",
            value=task.progress,
            type="determinate",
            color=self.theme_cls.primaryColor,
            size_hint_y=None,
            height=dp(6),
            radius=[dp(3),],
        )

        status_label = MDLabel(
            id="status_label",
            text=task.status.capitalize(),
            font_style="labelSmall",
            theme_text_color="Hint",
            halign="right",
        )

        btn_layout = MDBoxLayout(orientation="horizontal", spacing=dp(8), size_hint_y=None, height=dp(36), padding=[0, dp(4), 0, 0])

        pause_btn = MDIconButton(
            id="pause_btn",
            icon="pause",
            theme_icon_color="Custom",
            icon_color=self.theme_cls.onSurfaceVariantColor,
            disabled=True,
        )

        cancel_btn = MDIconButton(
            id="cancel_btn",
            icon="close",
            theme_icon_color="Custom",
            icon_color=self.theme_cls.onSurfaceVariantColor,
            on_release=lambda x, t=task: self.cancel_download(t),
        )

        open_btn = MDIconButton(
            id="open_btn",
            icon="folder-open",
            theme_icon_color="Custom",
            icon_color=self.theme_cls.primaryColor,
            on_release=lambda x, t=task: self.open_file(t),
            disabled=True,
        )

        btn_layout.add_widget(pause_btn)
        btn_layout.add_widget(cancel_btn)
        btn_layout.add_widget(open_btn)

        right_layout.add_widget(progress_bar)
        right_layout.add_widget(status_label)
        right_layout.add_widget(btn_layout)

        main_layout.add_widget(left_layout)
        main_layout.add_widget(right_layout)

        card.add_widget(main_layout)

        # Store widget references
        card.title_label = title_label
        card.url_label = url_label
        card.meta_label = meta_label
        card.progress_bar = progress_bar
        card.status_label = status_label
        card.pause_btn = pause_btn
        card.cancel_btn = cancel_btn
        card.open_btn = open_btn

        # Insert at top
        downloads_list.add_widget(card, index=0)

    def update_task_ui(self, task: DownloadTask):
        """Update task UI widget"""
        downloads_list = self.root.ids.main_screen.ids.downloads_list

        for child in downloads_list.children:
            if hasattr(child, 'task_id') and child.task_id == task.task_id:
                child.progress_bar.value = task.progress
                child.status_label.text = f"{task.status.capitalize()} {task.speed} {task.eta}".strip()

                if task.status == "completed":
                    child.open_btn.disabled = False
                    child.cancel_btn.disabled = True
                    child.pause_btn.disabled = True
                elif task.status == "failed":
                    child.cancel_btn.disabled = True
                    child.pause_btn.disabled = True
                elif task.status == "downloading":
                    child.cancel_btn.disabled = False
                    child.pause_btn.disabled = True  # TODO: implement pause

                break

    def cancel_download(self, task: DownloadTask):
        """Cancel a download"""
        task.status = "cancelled"
        self.update_task_ui(task)
        self.show_snackbar("Download cancelled")

    def open_file(self, task: DownloadTask):
        """Open downloaded file"""
        if task.filepath and os.path.exists(task.filepath):
            try:
                if platform == "android":
                    from android.content import Intent
                    from android.net import Uri
                    from android import mimetype
                    from jnius import autoclass

                    PythonActivity = autoclass('org.kivy.android.PythonActivity')
                    Intent = autoclass('android.content.Intent')
                    Uri = autoclass('android.net.Uri')
                    File = autoclass('java.io.File')

                    file = File(task.filepath)
                    uri = Uri.fromFile(file)

                    intent = Intent(Intent.ACTION_VIEW)
                    mime = mimetype.guess_type(task.filepath)[0] or "*/*"
                    intent.setDataAndType(uri, mime)
                    intent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION)

                    currentActivity = PythonActivity.mActivity
                    currentActivity.startActivity(intent)
                else:
                    import subprocess
                    subprocess.run(["xdg-open", task.filepath])

                self.show_snackbar("Opening file...")
            except Exception as e:
                self.show_snackbar(f"Could not open file: {e}")
        else:
            self.show_snackbar("File not found")

    def update_download_count(self):
        """Update download count label"""
        count = len(self.download_tasks)
        self.root.ids.main_screen.ids.download_count.text = f"({count})"

    def hide_empty_state(self):
        """Hide empty state when there are downloads"""
        empty_state = self.root.ids.main_screen.ids.empty_state
        empty_state.opacity = 0
        empty_state.height = 0
        empty_state.size_hint_y = None

    def show_empty_state(self):
        """Show empty state"""
        empty_state = self.root.ids.main_screen.ids.empty_state
        empty_state.opacity = 1
        empty_state.height = dp(300)
        empty_state.size_hint_y = None

    def format_size(self, size: int) -> str:
        """Format file size"""
        if not size or size == 0:
            return "Unknown"
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size < 1024:
                return f"{size:.1f} {unit}"
            size /= 1024
        return f"{size:.1f} TB"

    def load_history(self):
        """Load download history"""
        try:
            if os.path.exists(self.history_file):
                with open(self.history_file, 'r') as f:
                    data = json.load(f)
                    self.download_tasks = data.get('tasks', [])
                    # Recreate widgets
                    for task_data in self.download_tasks:
                        task = DownloadTask.from_dict(task_data)
                        self.create_task_widget(task)
                    self.update_download_count()
                    if self.download_tasks:
                        self.hide_empty_state()
        except Exception as e:
            Logger.error(f"Failed to load history: {e}")

    def save_history(self):
        """Save download history"""
        try:
            data = {
                'tasks': self.download_tasks,
                'updated': datetime.now().isoformat()
            }
            with open(self.history_file, 'w') as f:
                json.dump(data, f, indent=2)
        except Exception as e:
            Logger.error(f"Failed to save history: {e}")

    def clear_history(self):
        """Clear download history"""
        self.download_tasks = []
        self.download_dir = self.get_download_dir()
        self.history_file = os.path.join(self.download_dir, "history.json")

        downloads_list = self.root.ids.main_screen.ids.downloads_list
        downloads_list.clear_widgets()

        self.update_download_count()
        self.save_history()
        self.show_empty_state()
        self.show_snackbar("History cleared")

    def toggle_theme(self):
        """Toggle dark/light theme"""
        self.is_dark_theme = not self.is_dark_theme
        self.theme_cls.theme_style = "Dark" if self.is_dark_theme else "Light"
        self.save_theme_preference()

    def save_theme_preference(self):
        """Save theme preference"""
        try:
            pref_file = os.path.join(self.download_dir, "preferences.json")
            with open(pref_file, 'w') as f:
                json.dump({'dark_theme': self.is_dark_theme}, f)
        except:
            pass

    def set_dynamic_colors(self, active: bool):
        """Set dynamic colors (Material You)"""
        # TODO: Implement Material You dynamic colors
        pass

    def set_concurrent_downloads(self, value: int):
        """Set max concurrent downloads"""
        self.max_concurrent = value
        self.root.ids.settings_screen.ids.concurrent_label.text = str(value)

    def open_drawer(self):
        """Open navigation drawer"""
        self.root.ids.nav_drawer.set_state("open")

    def open_settings(self):
        """Open settings screen"""
        self.switch_screen("settings")

    def switch_screen(self, screen_name: str):
        """Switch to a screen"""
        self.root.ids.screen_manager.current = screen_name
        if screen_name != "main":
            self.root.ids.nav_drawer.set_state("close")

    def open_github(self):
        """Open GitHub repo"""
        import webbrowser
        webbrowser.open("https://github.com/khsahibi/vdownloader")

    def show_snackbar(self, text: str):
        """Show a snackbar message"""
        MDSnackbar(
            MDSnackbarText(text=text),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.8,
        ).open()


# ============================================================================
# Entry Point
# ============================================================================

if __name__ == '__main__':
    KHSahibiVDownloader().run()