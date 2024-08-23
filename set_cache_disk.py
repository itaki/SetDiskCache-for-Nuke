import os
import platform
import subprocess
import logging
from typing import List, Optional

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class SetDiskCache:
    """
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
    """
    def __init__(self, preferred_volumes: List[str], cache_dir: str):
        self.preferred_volumes = preferred_volumes
        self.cache_dir = cache_dir
        self.cache_path: Optional[str] = None
        logging.debug(f"DiskCache initialized with preferred_volumes: {self.preferred_volumes} and cache_dir: '{self.cache_dir}'")
        self._handle_os_specific_cache_location()

    def _handle_os_specific_cache_location(self) -> None:
        current_os = platform.system()
        logging.debug(f"Detected operating system: {current_os}")

        if current_os == 'Darwin':
            self._set_cache_location_macos()
        elif current_os == 'Linux':
            self._set_cache_location_linux()
        elif current_os == 'Windows':
            self._set_cache_location_windows()
        else:
            logging.warning(f"Unsupported operating system: {current_os}. Skipping cache setup.")

    def _set_cache_location_macos(self) -> None:
        self.cache_path = self._find_suitable_cache_path_macos()

        if self.cache_path:
            os.environ['NUKE_TEMP_DIR'] = self.cache_path
            os.environ['NUKE_DISK_CACHE'] = self.cache_path
            logging.info(f"Cache directories set: NUKE_TEMP_DIR and NUKE_DISK_CACHE -> {self.cache_path}")
        else:
            logging.error("Failed to set cache directories. No suitable path found.")

    def _set_cache_location_linux(self) -> None:
        self.cache_path = self._find_suitable_cache_path_linux()

        if self.cache_path:
            os.environ['NUKE_TEMP_DIR'] = self.cache_path
            os.environ['NUKE_DISK_CACHE'] = self.cache_path
            logging.info(f"Cache directories set: NUKE_TEMP_DIR and NUKE_DISK_CACHE -> {self.cache_path}")
        else:
            logging.error("Failed to set cache directories. No suitable path found.")

    def _set_cache_location_windows(self) -> None:
        self.cache_path = self._find_suitable_cache_path_windows()

        if self.cache_path:
            os.environ['NUKE_TEMP_DIR'] = self.cache_path
            os.environ['NUKE_DISK_CACHE'] = self.cache_path
            logging.info(f"Cache directories set: NUKE_TEMP_DIR and NUKE_DISK_CACHE -> {self.cache_path}")
        else:
            logging.error("Failed to set cache directories. No suitable path found.")

    def _find_suitable_cache_path_macos(self) -> Optional[str]:
        for volume in self.preferred_volumes:
            volume_path = os.path.join('/Volumes', volume)
            if not os.path.ismount(volume_path):
                logging.warning(f"Volume '{volume}' is not mounted.")
                continue

            if self._is_network_drive(volume_path):
                logging.warning(f"Volume '{volume}' is a network drive. Skipping.")
                continue

            cache_path = os.path.join(volume_path, self.cache_dir)
            if self._ensure_directory(cache_path) and self._is_writable(cache_path):
                return cache_path

        home_cache_path = os.path.join(os.path.expanduser('~'), self.cache_dir)
        if self._ensure_directory(home_cache_path) and self._is_writable(home_cache_path):
            return home_cache_path

        return None

    def _find_suitable_cache_path_linux(self) -> Optional[str]:
        for volume in self.preferred_volumes:
            volume_path = os.path.join('/mnt', volume)  # Common mount point in Linux
            if not os.path.ismount(volume_path):
                logging.warning(f"Volume '{volume}' is not mounted.")
                continue

            if self._is_network_drive(volume_path):
                logging.warning(f"Volume '{volume}' is a network drive. Skipping.")
                continue

            cache_path = os.path.join(volume_path, self.cache_dir)
            if self._ensure_directory(cache_path) and self._is_writable(cache_path):
                return cache_path

        home_cache_path = os.path.join(os.path.expanduser('~'), self.cache_dir)
        if self._ensure_directory(home_cache_path) and self._is_writable(home_cache_path):
            return home_cache_path

        return None

    def _find_suitable_cache_path_windows(self) -> Optional[str]:
        for volume in self.preferred_volumes:
            volume_path = f"{volume}:\\"  # Windows uses drive letters
            if not os.path.isdir(volume_path):
                logging.warning(f"Volume '{volume}' is not accessible.")
                continue

            cache_path = os.path.join(volume_path, self.cache_dir)
            if self._ensure_directory(cache_path) and self._is_writable(cache_path):
                return cache_path

        home_cache_path = os.path.join(os.path.expanduser('~'), self.cache_dir)
        if self._ensure_directory(home_cache_path) and self._is_writable(home_cache_path):
            return home_cache_path

        return None

    def _is_network_drive(self, volume_path: str) -> bool:
        current_os = platform.system()

        if current_os == 'Darwin' or current_os == 'Linux':
            try:
                mount_output = subprocess.check_output(['mount'], text=True)
                for line in mount_output.splitlines():
                    if volume_path in line:
                        network_filesystems = ['smbfs', 'nfs', 'afp', 'cifs', 'webdav']
                        return any(fs_type in line for fs_type in network_filesystems)
                return False
            except subprocess.CalledProcessError as e:
                logging.error(f"Error executing mount command: {e}")
                return False

        elif current_os == 'Windows':
            try:
                output = subprocess.check_output(['net', 'use'], text=True)
                return volume_path.lower() in output.lower()
            except subprocess.CalledProcessError as e:
                logging.error(f"Error executing net use command: {e}")
                return False

        return False

    def _ensure_directory(self, path: str) -> bool:
        if os.path.isdir(path):
            return True

        try:
            os.makedirs(path, exist_ok=True)
            logging.info(f"Directory '{path}' created successfully.")
            return True
        except OSError as e:
            logging.error(f"Failed to create directory '{path}': {e}")
            return False

    def _is_writable(self, path: str) -> bool:
        test_file = os.path.join(path, '.write_test')
        try:
            with open(test_file, 'w') as f:
                f.write('test')
            os.remove(test_file)
            return True
        except IOError as e:
            logging.warning(f"Directory '{path}' is not writable: {e}")
            return False
