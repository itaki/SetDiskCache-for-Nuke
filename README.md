A class to manage and set cache directories for applications like Nuke,
    prioritizing local and writable volumes over network-mounted ones.

    Features:
        - Checks for preferred volumes and ensures they are suitable for caching.
        - Detects if a volume is network-mounted by parsing mount information.
        - Verifies write permissions on the target cache directory.
        - Falls back to the user's home directory if no suitable volume is found.
        - Supports OS-specific handling for macOS, Linux, and Windows (currently only macOS is implemented).

    Attributes:
        preferred_volumes (List[str]): List of preferred volume names to check. It will default 
        to the first available volume that passes the checks so list them in order of preference.
            e.g. PREFERRED_CACHE_DISKS = ['ReallyFastM2', 'LocalSSD', 'SlowRAID']
        cache_dir (str): Relative path for the cache directory on the drive. It will be created if it doesn't exist.
            e.g. CACHE_DIR = 'NukeCache' or CACHE_DIR = '.NukeCache' or CACHE_DIR = '_caches/nuke'
        cache_path (Optional[str]): The resolved cache path after checks.

    Notes: 
        This has been tested extensively on macOS, but only basic checks have been implemented for Linux and Windows.
        Please feel free to update the code to support more platforms or improve the existing checks.
        Start a pull request here : https://github.com/itaki/SetDiskCache-for-Nuke
