from abc import ABC, abstractmethod
from tsk_utils import get_fs_type

SECTOR_SIZE_PREFIX = "Sector Size: "
CLUSTER_SIZE_PREFIX = "Cluster Size: "
VOLUME_SERIAL_NUMBER_PREFIX = "Volume Serial Number: "
FIRST_CLUSTER_OF_MFT_PREFIX = "First Cluster of MFT: "
FIRST_CLUSTER_OF_MFT_MIRROR_PREFIX = "First Cluster of MFT Mirror: "
SIZE_OF_MFT_ENTRIES_PREFIX = "Size of MFT Entries: "
VOLUME_ID_PREFIX = "Volume ID: "
SECTORS_BEFORE_FILE_SYSTEM_PREFIX = "Sectors before file system: "
TOTAL_RANGE_PREFIX = "Total Range: "

class FileSystem(ABC):
    def __init__(self, dd_image_path):
        super().__init__()
        self.dd_image_path = dd_image_path

    @abstractmethod
    def is_valid(self):
        pass

    @abstractmethod
    def parse(self, fsstat_output):
        pass

class NTFS(FileSystem):
    def __init__(self, dd_image_path):
        super().__init__(dd_image_path)
        self.type, output = get_fs_type(self.dd_image_path)
        self.sector_size = None
        self.cluster_size = None
        self.volume_serial_number = None
        self.first_cluster_of_mft = None
        self.first_cluster_of_mft_mirror = None
        self.size_of_mft_entries = None
        self.parse(output)

    def parse(self, fsstat_output):
        for line in fsstat_output: 
            if line.startswith(SECTOR_SIZE_PREFIX):
                self.sector_size = int(line[len(SECTOR_SIZE_PREFIX):])
            if line.startswith(CLUSTER_SIZE_PREFIX):
                self.cluster_size = int(line[len(CLUSTER_SIZE_PREFIX):])
            if line.startswith(VOLUME_SERIAL_NUMBER_PREFIX):
                self.volume_serial_number = int(line[len(VOLUME_SERIAL_NUMBER_PREFIX):])
            if line.startswith(FIRST_CLUSTER_OF_MFT_PREFIX):
                self.first_cluster_of_mft = int(line[len(FIRST_CLUSTER_OF_MFT_PREFIX):])
            if line.startswith(FIRST_CLUSTER_OF_MFT_MIRROR_PREFIX):
                self.first_cluster_of_mft_mirror = int(line[len(FIRST_CLUSTER_OF_MFT_MIRROR_PREFIX):])
            if line.startswith(SIZE_OF_MFT_ENTRIES_PREFIX):
                self.size_of_mft_entries = int(line[len(SIZE_OF_MFT_ENTRIES_PREFIX):])


class FAT16(FileSystem):
    def __init__(self, dd_image_path):
        super().__init__(dd_image_path)
        self.type, output = get_fs_type(self.dd_image_path)
        self.sector_size = None
        self.cluster_size = None
        self.volume_id = None
        self.sectors_before_file_system = None
        self.total_range = None
        self.parse(output)

    def parse(self, fsstat_output):
        for line in fsstat_output: 
            if line.startswith(SECTOR_SIZE_PREFIX):
                self.sector_size = int(line[len(SECTOR_SIZE_PREFIX):])
            if line.startswith(CLUSTER_SIZE_PREFIX):
                self.cluster_size = int(line[len(CLUSTER_SIZE_PREFIX):])
            if line.startswith(VOLUME_ID_PREFIX):
                self.volume_id = int(line[len(VOLUME_ID_PREFIX):])
            if line.startswith(SECTORS_BEFORE_FILE_SYSTEM_PREFIX):
                self.sectors_before_file_system = int(line[len(SECTORS_BEFORE_FILE_SYSTEM_PREFIX):])
            if line.startswith(TOTAL_RANGE_PREFIX):
                self.total_range = int(line[len(TOTAL_RANGE_PREFIX):])

class FAT32(FileSystem):
    def __init__(self, dd_image_path):
        super().__init__(dd_image_path)
        self.type, output = get_fs_type(self.dd_image_path)
        self.sector_size = None
        self.cluster_size = None
        self.volume_id = None
        self.sectors_before_file_system = None
        self.total_range = None
        self.parse(output)

    def parse(self, fsstat_output):
        for line in fsstat_output: 
            if line.startswith(SECTOR_SIZE_PREFIX):
                self.sector_size = int(line[len(SECTOR_SIZE_PREFIX):])
            if line.startswith(CLUSTER_SIZE_PREFIX):
                self.cluster_size = int(line[len(CLUSTER_SIZE_PREFIX):])
            if line.startswith(VOLUME_ID_PREFIX):
                self.volume_id = int(line[len(VOLUME_ID_PREFIX):])
            if line.startswith(SECTORS_BEFORE_FILE_SYSTEM_PREFIX):
                self.sectors_before_file_system = int(line[len(SECTORS_BEFORE_FILE_SYSTEM_PREFIX):])
            if line.startswith(TOTAL_RANGE_PREFIX):
                self.total_range = int(line[len(TOTAL_RANGE_PREFIX):])


def ntfs_parse(ntfs):
    # TODO: parse NTFS filesystem! Argument will be passed in as a string

    # PERSON 2
    pass

def fat_parse(fat):
    # TODO: parse FAT filesystem! Argument will be passed in as a string
    
    # PERSON 2
    pass