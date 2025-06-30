# -*- coding: utf-8 -*-

"""
配置模块
包含所有配置项和设置
"""

from .settings import (
    VERSION,
    SOURCE_DISK_MODEL,
    RESTORE_PATHS,
    SOURCE_PATHS,
    USB_MOUNT,
    BACKUP_ROOT,
    #BACKUP_PREFIX,
    MIN_FREE_SPACE_GB,
    MAX_BACKUPS,
    MIN_BACKUP_INTERVAL_DAYS,
    LOG_DIR,
    LOG_FORMAT,
    LOG_ROTATION,
    RSYNC_OPTIONS,
    VERIFY_CHECKSUM,
    VERIFY_SAMPLE_SIZE
)

__all__ = [
    'VERSION',
    'SOURCE_DISK_MODEL',
    'RESTORE_PATHS',
    'SOURCE_PATHS',
    'USB_MOUNT',
    'BACKUP_ROOT',
    #'BACKUP_PREFIX',
    'MIN_FREE_SPACE_GB',
    'MAX_BACKUPS',
    'MIN_BACKUP_INTERVAL_DAYS',
    'LOG_DIR',
    'LOG_FORMAT',
    'LOG_ROTATION',
    'RSYNC_OPTIONS',
    'VERIFY_CHECKSUM',
    'VERIFY_SAMPLE_SIZE'
]
