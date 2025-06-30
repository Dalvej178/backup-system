# -*- coding: utf-8 -*-

import os
from pathlib import Path

# Version information
VERSION = "2.0.0"

# Disk model configurations
SOURCE_DISK_MODEL = "Samsung SSD 860 EVO 500GB"  # A机器硬盘型号

# Target machine configurations
RESTORE_PATHS = {
    "WDC WD10EZEX-00BBHA0": {  # B电脑
        "firefox_dst": "/home/amd369/snap/firefox/common/.mozilla/firefox/a1x4t0kj.default-release",
        "vbox_restore_dir": "/home/amd369/VirtualBox VMs",
        "ubuntu_restore_dir": "/home/amd369/ubuntu20240415"
    },
    "XCERIA SATA": {  # C电脑
        "firefox_dst": "/home/amd369/snap/firefox/common/.mozilla/firefox/tn5em7w4.default",
        "vbox_restore_dir": "/home/amd369/VirtualBox VMs",
        "ubuntu_restore_dir": "/home/amd369/ubuntu20240415"
    }
}

# Source paths (A机器)
SOURCE_PATHS = {
    "firefox_src": "/home/amd369/snap/firefox/common/.mozilla/firefox/9o7ba9cd.default",
    "vbox_src": "/home/amd369/VirtualBox VMs",
    "ubuntu_src": "/home/amd369/ubuntu20240415"
}

# Backup settings
USB_MOUNT = "/media/amd369/KIOXIA480G"
BACKUP_ROOT = os.path.join(USB_MOUNT, "backup")
BACKUP_DIR = os.path.join(BACKUP_ROOT, "backup_2025-06-28")  # 指定要使用的备份目录，可以是已存在的目录
MIN_FREE_SPACE_GB = 2  # 最小剩余空间要求（GB）

# Backup retention settings
MAX_BACKUPS = 5  # 保留的最大备份数量
MIN_BACKUP_INTERVAL_DAYS = 1  # 最小备份间隔（天）

# Logging settings
LOG_DIR = os.path.join(Path(__file__).parent.parent, "logs")
LOG_FORMAT = "{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
LOG_ROTATION = "1 week"  # 日志保留时间

# RSync settings
RSYNC_OPTIONS = {
    "archive": True,          # -a, 归档模式
    "verbose": True,          # -v, 详细输出
    "compress": True,         # -z, 传输时压缩
    "delete": True,          # --delete, 删除目标端不存在的文件
    "progress": True,        # --info=progress2, 显示进度
    "exclude": ["lock"]      # --exclude=lock, 排除文件
}

# Verification settings
VERIFY_CHECKSUM = True  # 是否验证备份文件校验和
VERIFY_SAMPLE_SIZE = 10  # 随机验证文件数量（每个目录）
