# -*- coding: utf-8 -*-

import os
import time
import json
import random
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple

from config.settings import (
    SOURCE_PATHS,
    BACKUP_DIR,
    MIN_FREE_SPACE_GB,
    RSYNC_OPTIONS,
    VERIFY_CHECKSUM,
    VERIFY_SAMPLE_SIZE
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

class BackupManager:
    def __init__(self):
        """初始化备份管理器"""
        self.backup_dir = BACKUP_DIR
        self.history_file = os.path.join(self.backup_dir, "backup_history.json")
        
        if os.path.exists(self.backup_dir):
            print_info(f"使用现有备份目录: {self.backup_dir}")
            # 显示上次备份时间
            last_backup_time = self._get_last_backup_time()
            if last_backup_time:
                print_info(f"上次备份时间: {last_backup_time}")
        else:
            print_info(f"将创建新的备份目录: {self.backup_dir}")

    def _load_backup_history(self) -> Dict:
        """加载备份历史记录"""
        if os.path.exists(self.history_file):
            try:
                with open(self.history_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print_error(f"读取备份历史记录失败: {e}")
        return {"backups": []}

    def _save_backup_history(self, history: Dict) -> None:
        """保存备份历史记录"""
        try:
            # 确保备份目录存在
            os.makedirs(self.backup_dir, exist_ok=True)
            with open(self.history_file, 'w', encoding='utf-8') as f:
                json.dump(history, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print_error(f"保存备份历史记录失败: {e}")

    def _get_last_backup_time(self) -> Optional[str]:
        """获取最后一次备份时间"""
        history = self._load_backup_history()
        if history["backups"]:
            return history["backups"][-1]["backup_time"]
        return None

    def _update_backup_history(self, success: bool, total_size: float, duration: str) -> None:
        """更新备份历史记录"""
        history = self._load_backup_history()
        backup_info = {
            "backup_time": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            "success": success,
            "total_size_gb": round(total_size, 2),
            "duration": duration,
            "source_paths": SOURCE_PATHS
        }
        history["backups"].append(backup_info)
        self._save_backup_history(history)
        
    def _build_rsync_command(self, src: str, dst: str) -> List[str]:
        """
        构建rsync命令
        
        Args:
            src: 源路径
            dst: 目标路径
            
        Returns:
            List[str]: rsync命令及其参数列表
        """
        cmd = ["rsync"]
        
        if RSYNC_OPTIONS["archive"]:
            cmd.append("-a")
        if RSYNC_OPTIONS["verbose"]:
            cmd.append("-v")
        if RSYNC_OPTIONS["compress"]:
            cmd.append("-z")
        if RSYNC_OPTIONS["delete"]:
            cmd.append("--delete")
        if RSYNC_OPTIONS["progress"]:
            cmd.append("--info=progress2")
            
        for item in RSYNC_OPTIONS.get("exclude", []):
            cmd.extend(["--exclude", item])
            
        # 确保源路径以/结尾，这样rsync会复制目录内容而不是目录本身
        src = str(src).rstrip("/") + "/"
        cmd.extend([src, str(dst)])
        
        return cmd
    
    def _verify_backup(self, src_path: str, dst_path: str) -> bool:
        """
        验证备份的完整性
        
        Args:
            src_path: 源路径
            dst_path: 目标路径
            
        Returns:
            bool: 验证是否通过
        """
        if not VERIFY_CHECKSUM:
            return True
            
        src = Path(src_path)
        dst = Path(dst_path)
        
        # 获取所有文件列表
        src_files = [f for f in src.rglob("*") if f.is_file()]
        
        # 如果文件太多，随机抽样验证
        if len(src_files) > VERIFY_SAMPLE_SIZE:
            src_files = random.sample(src_files, VERIFY_SAMPLE_SIZE)
        
        for src_file in src_files:
            # 计算目标文件的相对路径
            rel_path = src_file.relative_to(src)
            dst_file = dst / rel_path
            
            if not dst_file.exists():
                print_error(f"目标文件不存在: {dst_file}")
                return False
            
            src_checksum = calculate_checksum(src_file)
            dst_checksum = calculate_checksum(dst_file)
            
            if src_checksum != dst_checksum:
                print_error(f"文件校验和不匹配: {rel_path}")
                return False
        
        return True
    
    def _check_space_requirements(self) -> Tuple[bool, float, float]:
        """
        检查空间要求
        
        Returns:
            Tuple[bool, float, float]: (是否满足要求, 需要的空间, 可用空间)
        """
        total_size = sum(get_dir_size_gb(path) for path in SOURCE_PATHS.values())
        available_space = get_disk_free_gb(self.backup_dir)
        
        print_info(f"需要备份的总空间: {total_size:.2f} GB")
        print_info(f"可用空间: {available_space:.2f} GB")
        
        return (available_space >= total_size + MIN_FREE_SPACE_GB,
                total_size,
                available_space)
    
    def perform_backup(self) -> bool:
        """
        执行备份操作
        
        Returns:
            bool: 备份是否成功
        """
        start_time = time.time()
        print_info(f"开始备份 - {datetime.now()}")
        
        # 检查空间要求
        space_ok, total_size, available_space = self._check_space_requirements()
        if not space_ok:
            print_error(
                f"空间不足。需要: {total_size + MIN_FREE_SPACE_GB:.2f} GB, "
                f"可用: {available_space:.2f} GB"
            )
            return False
        
        # 确保备份目录存在
        if not verify_path_exists(self.backup_dir, create=True):
            return False
        
        # 执行备份
        success = True
        for name, src_path in SOURCE_PATHS.items():
            if not os.path.exists(src_path):
                print_error(f"源路径不存在: {src_path}")
                success = False
                continue
                
            dst_path = os.path.join(self.backup_dir, os.path.basename(src_path))
            print_info(f"备份 {name}: {src_path} -> {dst_path}")
            
            try:
                import subprocess
                cmd = self._build_rsync_command(src_path, dst_path)
                subprocess.run(cmd, check=True)
                
                # 验证备份
                if not self._verify_backup(src_path, dst_path):
                    print_error(f"备份验证失败: {name}")
                    success = False
                    
            except subprocess.SubprocessError as e:
                print_error(f"备份失败 {name}: {e}")
                success = False
        
        end_time = time.time()
        duration = format_duration(end_time - start_time)
        
        if success:
            print_info(f"备份完成 - 耗时: {duration}")
        
        # 更新备份历史记录
        self._update_backup_history(success, total_size, duration)
        
        return success
