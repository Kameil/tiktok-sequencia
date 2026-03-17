"""
Chrome flags configuration by operating system
"""

def get_linux_flags():
    """Return Linux-specific Chrome flags"""
    return [
        "--disable-dev-shm-usage",
        "--disable-gpu",
        "--use-gl=swiftshader",
        "--disable-setuid-sandbox",
        "--ozone-platform=x11",
        "--no-sandbox",
        "--disable-infobars",
        "--start-maximized",
        "--disable-extensions"
    ]

def get_windows_flags():
    """Return Windows-specific Chrome flags"""
    return [
        "--no-sandbox",
        "--disable-infobars",
        "--start-maximized",
        "--disable-extensions",
        "--disable-gpu",
        "--disable-dev-shm-usage"
    ]

def get_macos_flags():
    """Return macOS-specific Chrome flags"""
    return [
        "--no-sandbox",
        "--disable-infobars",
        "--start-maximized",
        "--disable-extensions",
        "--disable-gpu"
    ]

def get_default_flags():
    """Return default Chrome flags for unknown OS"""
    return [
        "--no-sandbox",
        "--disable-infobars",
        "--start-maximized",
        "--disable-extensions"
    ]

def get_flags_by_os(os_name):
    """
    Get Chrome flags based on operating system
    
    Args:
        os_name (str): Operating system name (Linux, Windows, Darwin)
    
    Returns:
        list: List of Chrome flags
    """
    flags_map = {
        "Linux": get_linux_flags,
        "Windows": get_windows_flags,
        "Darwin": get_macos_flags
    }
    
    flag_function = flags_map.get(os_name, get_default_flags)
    return flag_function()