import set_cache_disk
PREFERRED_CACHE_DISKS = ['FastM2','SlowerSSD','Raid','ExampleDisk']
CACHE_DIR = '_caches/nuke'
set_cache_disk.SetDiskCache(PREFERRED_CACHE_DISKS,CACHE_DIR)