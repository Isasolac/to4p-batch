from enum import Enum

class SupportedTypes(Enum):
    NTFS = 1
    FAT16 = 2
    FAT32 = 3
    UNSUPPORTED = 4