# -*- coding: utf-8 -*-

import os
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Tuple

from config.settings import (
    BACKUP_ROOT,
    #BACKUP_PREFIX,
    MIN_FREE_SPACE_GB,
    RESTORE_PATHS,
    RSYNC_OPTIONS,
    VERIFY_CHECKSUM
)
from .utils import (
    get_dir_size_gb,
    get_disk_free_gb,
    verify_path_exists,
    calculate_checksum,
    format_duration,
    print_info,
    print_error
)

class RestoreManager:
    def __init__(self, disk_model: str):
        """
        初始化恢复管理器
        
        Args:
            disk_model: 目标机器的硬盘型号
        """
        self.disk_model = disk_model
        self.restore_paths = RESTORE_PATHS.get(disk_model)
        if not self.restore_paths:
            raise ValueError(f"未找到硬盘型号 {disk_model} 的恢复路径配置")
            
    def _get_latest_backup(self) -> Optional[Path]:
        """
        获取最新的备份目录
        
        Returns:
            Optional[Path]: 最新备份目录的路径，如果没有找到则返回None
        """
        if not os.path.isdir(BACKUP_ROOT):
            print_error(f"备份根目录不存在: {BACKUP_ROOT}")
            return None
            
        backup_dirs = [
            d for d in Path(BACKUP_ROOT).iterdir()
            if d.is_dir() and d.name.startswith(BACKUP_PREFIX)
        ]
        
        if not backup_dirs:
            print_error("未找到任何备份目录")
            return None
            
        # 按日期排序，返回最新的
        return sorted(backup_dirs, key=lambda x: x.name)[-1]
    
    def _verify_restore(self, src_path: Path, dst_path: Path) -> bool:
        """
        验证恢复的完整性
        
        Args:
            src_path: 源路径（备份目录）
            dst_path: 目标路径（恢复位置）
            
        Returns:
            bool: 验证是否通过
        """
        if not VERIFY_CHECKSUM:
            return True
            
        src_checksum = calculate_checksum(src_path)
        dst_checksum = calculate_checksum(dst_path)
        
        if src_checksum != dst_checksum:
            print_error(f"恢复验证失败: {dst_path}")
            print_error(f"源校验和: {src_checksum}")
            print_error(f"目标校验和: {dst_checksum}")
            return False
            
        return True
    
    def _check_space_requirements(self, backup_dir: Path) -> Tuple[bool, float, float]:
        """
        检查目标磁盘空间是否足够
        
        Args:
            backup_dir: 备份目录路径
            
        Returns:
            Tuple[bool, float, float]: (是否满足要求, 需要的空间, 可用空间)
        """
        # 计算所需空间
        total_size = sum(
            get_dir_size_gb(os.path.join(backup_dir, os.path.basename(path)))
            for path in self.restore_paths.values()
        )
        
        # 检查目标磁盘剩余空间
        available_space = get_disk_free_gb("/")
        
        print_info(f"恢复所需空间: {total_size:.2f} GB")
        print_info(f"目标磁盘可用空间: {available_space:.2f} GB")
        
        return (available_space >= total_size + MIN_FREE_SPACE_GB,
                total_size,
                available_space)
    
    def perform_restore(self) -> bool:
        """
        执行恢复操作
        
        Returns:
            bool: 恢复是否成功
        """
        start_time = time.time()
        print_info(f"开始恢复 - {datetime.now()}")
        
        # 获取最新备份
        backup_dir = self._get_latest_backup()
        if not backup_dir:
            return False
            
        print_info(f"使用备份目录: {backup_dir}")
        
        # 检查空间要求
        space_ok, total_size, available_space = self._check_space_requirements(backup_dir)
        if not space_ok:
            print_error(
                f"目标磁盘空间不足。需要: {total_size + MIN_FREE_SPACE_GB:.2f} GB, "
                f"可用: {available_space:.2f} GB"
            )
            return False
        
        # 执行恢复
        success = True
        for name, dst_path in self.restore_paths.items():
            src_path = os.path.join(backup_dir, os.path.basename(dst_path))
            if not os.path.exists(src_path):
                print_error(f"备份源路径不存在: {src_path}")
                success = False
                continue
                
            print_info(f"恢复 {name}: {src_path} -> {dst_path}")
            
            # 确保目标目录存在
            if not verify_path_exists(os.path.dirname(dst_path), create=True):
                success = False
                continue
                
            try:
                import subprocess
                # 构建rsync命令
                cmd = ["rsync", "-avz", "--delete"]
                if RSYNC_OPTIONS["progress"]:
                    cmd.append("--info=progress2")
                cmd.extend([str(src_path) + "/", str(dst_path) + "/"])
                
                # 执行rsync
                subprocess.run(cmd, check=True)
                
                # 验证恢复
                if not self._verify_restore(Path(src_path), Path(dst_path)):
                    print_error(f"恢复验证失败: {name}")
                    success = False
                    
            except subprocess.SubprocessError as e:
                print_error(f"恢复失败 {name}: {e}")
                success = False
        
        if success:
            end_time = time.time()
            duration = format_duration(end_time - start_time)
            print_info(f"恢复完成 - 耗时: {duration}")
        
        return success
