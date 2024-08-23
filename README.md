# SetDiskCache for Nuke

A class to manage and set cache directories for applications like Nuke, prioritizing local and writable volumes over network-mounted ones.

## Features
- **Volume Checking**: Scans a list of preferred volumes and ensures they are suitable for caching.
- **Network Detection**: Detects if a volume is network-mounted by parsing mount information.
- **Write Permission Verification**: Verifies write permissions on the target cache directory.
- **Fallback Mechanism**: Falls back to the user's home directory if no suitable volume is found.
- **Cross-Platform Support**: Supports OS-specific handling for macOS, Linux, and Windows (currently only macOS is fully implemented).

## Attributes
- **preferred_volumes (List[str])**: List of preferred volume names to check. It will default to the first available volume that passes the checks, so list them in order of preference.
  - Example: `PREFERRED_CACHE_DISKS = ['ReallyFastM2', 'LocalSSD', 'SlowRAID']`
  
- **cache_dir (str)**: Relative path for the cache directory on the drive. It will be created if it doesn't exist.
  - Example: `CACHE_DIR = 'NukeCache'` or `CACHE_DIR = '.NukeCache'` or `CACHE_DIR = '_caches/nuke'`
  
- **cache_path (Optional[str])**: The resolved cache path after checks.

## Installation

1. **Copy the Script**: Place the script in your `.nuke` folder or wherever you keep your scripts.

2. **Add to init.py or menu.py**:
   - Add the following code to your `init.py` file if you want it to always run (both command line and GUI versions of Nuke). This is recommended.
   - Alternatively, add it to your `menu.py` file if you only want to run it when you run the GUI version.

```python
import set_cache_disk  # Import the script
PREFERRED_CACHE_DISKS = ['FastM2', 'SlowerSSD', 'Raid', 'ExampleDisk']  # Your disks or volumes in order of preference
CACHE_DIR = '_caches/nuke'  # The cache directory
set_cache_disk.DiskCache(PREFERRED_CACHE_DISKS, CACHE_DIR)  # Run the script
```

## Notes
This script has been tested extensively on macOS.

It has not been sufficantly tested on Linux and Windows, but may work. Please feel free to contribute! 
Start a pull request here: https://github.com/itaki/SetDiskCache-for-Nuke
