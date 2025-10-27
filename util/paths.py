"""
路径管理工具 - 统一管理项目中的所有路径
"""

from pathlib import Path
from typing import Union


def get_project_root() -> Path:
    """
    获取项目根目录路径
    
    Returns:
        Path: 项目根目录的绝对路径
    """
    # 从当前文件位置往上查找，直到找到包含main.py的目录
    current_path = Path(__file__).resolve()
    
    # 向上查找直到找到项目根目录（包含main.py的目录）
    for parent in current_path.parents:
        if (parent / "main.py").exists():
            return parent
    
    # 如果没找到，返回当前文件的父目录的父目录（util的父目录）
    return current_path.parent


def get_config_dir() -> Path:
    """获取配置目录路径"""
    return get_project_root() / "config"


def get_data_dir() -> Path:
    """获取数据目录路径"""
    return get_project_root() / "data"


def get_temp_dir() -> Path:
    """获取临时文件目录路径"""
    return get_project_root() / "temp"


def get_templates_dir() -> Path:
    """获取模板目录路径"""
    return get_project_root() / "templates"


def get_static_dir() -> Path:
    """获取静态文件目录路径"""
    return get_project_root() / "static"


def get_app_dir() -> Path:
    """获取应用代码目录路径"""
    return get_project_root() / "app"


def get_tool_dir() -> Path:
    """获取工具目录路径"""
    return get_project_root() / "tool"


def get_docker_dir() -> Path:
    """获取Docker配置目录路径"""
    return get_project_root() / "docker"


def get_users_config_file() -> Path:
    """获取用户配置文件路径"""
    return get_config_dir() / "users.json"


def ensure_dir_exists(path: Union[str, Path]) -> Path:
    """
    确保目录存在，如果不存在则创建
    
    Args:
        path: 目录路径
        
    Returns:
        Path: 目录路径对象
    """
    path_obj = Path(path)
    path_obj.mkdir(parents=True, exist_ok=True)
    return path_obj


def get_relative_path(file_path: Union[str, Path], base_path: Union[str, Path] = None) -> str:
    """
    获取相对于基准路径的相对路径
    
    Args:
        file_path: 文件路径
        base_path: 基准路径，默认为项目根目录
        
    Returns:
        str: 相对路径字符串
    """
    if base_path is None:
        base_path = get_project_root()
    
    file_path = Path(file_path)
    base_path = Path(base_path)
    
    try:
        return str(file_path.relative_to(base_path)).replace('\\', '/')
    except ValueError:
        # 如果无法计算相对路径，返回绝对路径
        return str(file_path).replace('\\', '/')


# 常用路径常量
PROJECT_ROOT = get_project_root()
CONFIG_DIR = get_config_dir()
DATA_DIR = get_data_dir()
TEMP_DIR = get_temp_dir()
TEMPLATES_DIR = get_templates_dir()
STATIC_DIR = get_static_dir()
APP_DIR = get_app_dir()
TOOL_DIR = get_tool_dir()
DOCKER_DIR = get_docker_dir()
USERS_CONFIG_FILE = get_users_config_file()