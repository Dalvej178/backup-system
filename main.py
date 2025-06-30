# -*- coding: utf-8 -*-

import sys
import argparse

from config.settings import VERSION
from core.utils import (
    setup_logging,
    is_ubuntu,
    get_disk_model,
    check_root_privileges,
    print_info,
    print_error
)
from core.backup import BackupManager
from core.restore import RestoreManager

def parse_args() -> argparse.Namespace:
    """解析命令行参数"""
    parser = argparse.ArgumentParser(
        description="Ubuntu系统备份还原工具",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument(
        "-b", "--backup",
        action="store_true",
        help="执行备份操作"
    )
    group.add_argument(
        "-r", "--restore",
        action="store_true",
        help="执行恢复操作"
    )
    
    parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"备份系统 v{VERSION}"
    )
    
    return parser.parse_args()

def main() -> int:
    """
    主程序入口
    
    Returns:
        int: 退出码（0表示成功，非0表示失败）
    """
    # 检查root权限
    if not check_root_privileges():
        print("请使用sudo或root权限运行本程序")
        return 1
    
    # 检查操作系统
    if not is_ubuntu():
        print("当前操作系统不是Ubuntu，程序退出")
        return 1
    
    # 设置日志（现在是空操作）
    setup_logging()
    print_info(f"备份系统 v{VERSION} 启动")
    
    # 解析命令行参数
    args = parse_args()
    
    try:
        # 获取硬盘型号
        disk_model = get_disk_model()
        print_info(f"检测到硬盘型号: {disk_model}")
        
        if args.backup:
            # 执行备份
            manager = BackupManager()
            success = manager.perform_backup()
        else:
            # 执行恢复
            manager = RestoreManager(disk_model)
            success = manager.perform_restore()
        
        return 0 if success else 1
        
    except Exception as e:
        print_error(f"发生错误: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
