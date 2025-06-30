# -*- coding: utf-8 -*-

import os
import sys
import subprocess
from pathlib import Path
from typing import Optional, Dict, List, Union
from datetime import datetime

def print_error(message: str) -> None:
    """打印错误信息"""
    print(f"错误: {message}", file=sys.stderr)

def print_warning(message: str) -> None:
    """打印警告信息"""
    print(f"警告: {message}", file=sys.stderr)

def print_info(message: str) -> None:
    """打印信息"""
    print(f"信息: {message}")

def setup_logging() -> None:
    """配置日志系统"""
    # 由于移除了loguru，此函数现在只是一个占位符
    pass

def get_disk_model() -> str:
    """获取当前系统的硬盘型号"""
    try:
        result = subprocess.run(
            ["lsblk", "-dno", "MODEL", "/dev/sda"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except subprocess.SubprocessError as e:
        print_error(f"获取硬盘型号失败: {e}")
        return "Unknown"

def is_ubuntu() -> bool:
    """检查当前系统是否为Ubuntu"""
    try:
        with open("/etc/os-release") as f:
            content = f.read().lower()
            return "id=ubuntu" in content or "id_like=ubuntu" in content
    except Exception as e:
        print_error(f"检查操作系统失败: {e}")
        return False

def get_dir_size_gb(path: Union[str, Path]) -> float:
    """
    计算目录大小（GB）
    
    Args:
        path: 目录路径
        
    Returns:
        float: 目录大小（GB）
    """
    total = 0
    try:
        for dirpath, _, filenames in os.walk(str(path)):
            for f in filenames:
                fp = os.path.join(dirpath, f)
                try:
                    total += os.path.getsize(fp)
                except (OSError, FileNotFoundError) as e:
                    print_warning(f"无法获取文件大小 {fp}: {e}")
    except Exception as e:
        print_error(f"计算目录大小失败 {path}: {e}")
    
    return total / (1024 ** 3)  # 转换为GB

def get_disk_free_gb(path: Union[str, Path]) -> float:
    """
    获取指定路径所在磁盘的剩余空间（GB）
    
    Args:
        path: 路径
        
    Returns:
        float: 剩余空间（GB）
    """
    try:
        if hasattr(os, 'statvfs'):  # Unix/Linux系统
            statvfs = os.statvfs(str(path))
            free_gb = statvfs.f_frsize * statvfs.f_bavail / (1024 ** 3)
            return free_gb
        else:  # Windows系统
            import ctypes
            free_bytes = ctypes.c_ulonglong(0)
            ctypes.windll.kernel32.GetDiskFreeSpaceExW(
                str(path),
                None,
                None,
                ctypes.pointer(free_bytes)
            )
            return free_bytes.value / (1024 ** 3)
    except Exception as e:
        print_error(f"获取磁盘剩余空间失败 {path}: {e}")
        return 0.0

def format_duration(seconds: float) -> str:
    """
    格式化持续时间
    
    Args:
        seconds: 秒数
        
    Returns:
        str: 格式化后的时间字符串
    """
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    secs = seconds % 60
    return f"{hours}小时 {minutes}分钟 {secs:.2f}秒"

def verify_path_exists(path: Union[str, Path], create: bool = False) -> bool:
    """
    验证路径是否存在，可选择创建
    
    Args:
        path: 要验证的路径
        create: 如果不存在是否创建
        
    Returns:
        bool: 路径是否存在或创建成功
    """
    path = Path(path)
    if path.exists():
        return True
    
    if create:
        try:
            path.mkdir(parents=True, exist_ok=True)
            print_info(f"已创建目录: {path}")
            return True
        except Exception as e:
            print_error(f"创建目录失败 {path}: {e}")
            return False
    
    return False

def calculate_checksum(file_path: Union[str, Path]) -> Optional[str]:
    """
    计算文件的MD5校验和
    
    Args:
        file_path: 文件路径
        
    Returns:
        Optional[str]: MD5校验和，失败返回None
    """
    try:
        result = subprocess.run(
            ["md5sum", str(file_path)],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            check=True
        )
        return result.stdout.split()[0]
    except subprocess.SubprocessError as e:
        print_error(f"计算文件校验和失败 {file_path}: {e}")
        return None

def check_root_privileges() -> bool:
    """
    检查是否具有root权限
    
    Returns:
        bool: 是否具有root权限
    """
    if sys.platform.startswith('win'):
        print_error("此程序只能在Ubuntu系统上运行")
        return False
    try:
        return os.geteuid() == 0
    except AttributeError:
        print_error("无法检查root权限")
        return False
