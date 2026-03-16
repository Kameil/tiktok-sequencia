"""
Chrome executable paths by operating system
"""

import os
from platform import system

def get_linux_paths():
    """Return Linux Chrome paths"""
    return {
        # Official Chrome/Chromium
        "standard": "/sbin/google-chrome-stable",
        "alternative1": "/usr/bin/google-chrome-stable",
        "alternative2": "/usr/bin/google-chrome",
        "alternative3": "/usr/bin/google-chrome-unstable",
        "alternative4": "/usr/bin/google-chrome-beta",
        
        # Chromium
        "chromium": "/usr/bin/chromium",
        "chromium_browser": "/usr/bin/chromium-browser",
        "chromium_alt": "/usr/lib/chromium/chrome",
        "chromium_alt2": "/usr/lib/chromium-browser/chromium-browser",
        
        # Snap packages
        "snap_chrome": "/snap/bin/chromium",
        "snap_chrome_alt": "/snap/bin/google-chrome",
        "snap_chrome_stable": "/snap/bin/google-chrome-stable",
        
        # Flatpak
        "flatpak_chrome": "/var/lib/flatpak/exports/bin/com.google.Chrome",
        "flatpak_chromium": "/var/lib/flatpak/exports/bin/org.chromium.Chromium",
        "flatpak_user_chrome": os.path.expanduser("~/.local/share/flatpak/exports/bin/com.google.Chrome"),
        "flatpak_user_chromium": os.path.expanduser("~/.local/share/flatpak/exports/bin/org.chromium.Chromium"),
        
        # AppImage
        "appimage_chrome": os.path.expanduser("~/Applications/google-chrome.AppImage"),
        "appimage_chromium": os.path.expanduser("~/Applications/chromium.AppImage"),
        
        # NixOS
        "nixos_chrome": "/run/current-system/sw/bin/google-chrome-stable",
        "nixos_chromium": "/run/current-system/sw/bin/chromium",
        "nix_user_chrome": os.path.expanduser("~/.nix-profile/bin/google-chrome-stable"),
        
        # Arch Linux
        "arch_chrome": "/usr/bin/google-chrome",
        "arch_chromium": "/usr/bin/chromium",
        
        # Fedora/RHEL
        "fedora_chrome": "/usr/bin/google-chrome",
        "fedora_chromium": "/usr/bin/chromium",
        "fedora_chrome_alt": "/usr/bin/google-chrome-stable",

        # Local Binaries
        "local_bin": "/usr/local/bin/google-chrome",
        "local_bin_chromium": "/usr/local/bin/chromium",
        "opt_chrome": "/opt/google/chrome/chrome",
        "opt_chromium": "/opt/chromium/chrome",
        
        # Home directory
        "home_chrome": os.path.expanduser("~/bin/google-chrome"),
        "home_chromium": os.path.expanduser("~/bin/chromium"),
        "home_local_chrome": os.path.expanduser("~/.local/bin/google-chrome"),
        "home_local_chromium": os.path.expanduser("~/.local/bin/chromium"),
    }

def get_windows_paths():
    """Return Windows Chrome paths"""
    return {
        "windows_chrome": "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
        "windows_chrome_x86": "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
        "windows_chromium": "C:\\Program Files\\Chromium\\Application\\chrome.exe",
        "windows_local": os.path.expanduser("~\\AppData\\Local\\Google\\Chrome\\Application\\chrome.exe"),
        "windows_local_chromium": os.path.expanduser("~\\AppData\\Local\\Chromium\\Application\\chrome.exe"),
    }

def get_macos_paths():
    """Return macOS Chrome paths"""
    return {
        "mac_chrome": "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
        "mac_chromium": "/Applications/Chromium.app/Contents/MacOS/Chromium",
    }

def get_paths_by_os():
    """
    Get Chrome paths based on current operating system
    
    Returns:
        dict: Dictionary of Chrome paths for current OS
    """
    system_name = system()
    
    paths_map = {
        "Linux": get_linux_paths,
        "Windows": get_windows_paths,
        "Darwin": get_macos_paths
    }
    
    paths_function = paths_map.get(system_name, lambda: {})
    return paths_function()