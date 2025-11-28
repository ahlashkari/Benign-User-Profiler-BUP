#!/usr/bin/env python3

from .base_browser import BaseBrowserModule
from .soundcloud import SoundcloudModule
from .image_download import ImageDownloadModule
from .youtube import YoutubeModule
from .web_browse import WebBrowseModule
from .custom_network_service import CustomServiceModule
from .firefox_search import FirefoxSearchModule

def get_module(module_type, headless=False):
    modules = {
        "soundcloud": SoundcloudModule,
        "download": ImageDownloadModule,
        "youtube": YoutubeModule,
        "web": WebBrowseModule,
        "custom_service": CustomServiceModule,
        "firefox_search": FirefoxSearchModule
    }
    
    if module_type.lower() in modules:
        return modules[module_type.lower()](headless=headless)
    return WebBrowseModule(headless=headless)