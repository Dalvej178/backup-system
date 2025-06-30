# -*- coding: utf-8 -*-

"""
核心功能模块
包含备份、恢复和工具函数
"""

from .backup import BackupManager
from .restore import RestoreManager
from .utils import (
    setup_logging,
    is_ubuntu,
    get_disk_model,
    get_dir_size_gb,
    get_disk_free_gb,
    verify_path_exists,
    calculate_checksum,
    format_duration,
    check_root_privileges
)

__all__ = [
    'BackupManager',
    'RestoreManager',
    'setup_logging',
    'is_ubuntu',
    'get_disk_model',
    'get_dir_size_gb',
    'get_disk_free_gb',
    'verify_path_exists',
    'calculate_checksum',
    'format_duration',
    'check_root_privileges'
]
