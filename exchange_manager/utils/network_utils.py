import os
import logging
import socket
import platform
import sys


class SystemUtils:
    
    @staticmethod
    def get_local_ip() -> str:
        """Get the local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            
            ip = s.getsockname()[0]
            s.close()
            return ip
        except Exception as e:
            logging.error(f"Error getting local IP: {e}")
            return "127.0.0.1"
    
    @staticmethod
    def get_local_hostname() -> str:
        """Get the local hostname"""
        try:
            return socket.gethostname()
        except Exception as e:
            logging.error(f"Error getting local hostname: {e}")
            return "localhost"
    
    @staticmethod
    def is_windows() -> bool:
        return (
            os.name == "nt"
            and sys.platform == "win32"
            and platform.system() == "Windows"
        )  # noqa E501  # noqa E501
    
    @staticmethod
    def is_linux() -> bool:
        return (
            os.name == "posix"
            and platform.system() == "Linux"
            and sys.platform in {"linux", "linux2"}
        )  # noqa: E501

    @staticmethod
    def is_mac() -> bool:
        return (
            os.name == "posix"
            and sys.platform == "darwin"
            and platform.system() == "Darwin"
        )  # noqa E501  # noqa E501
