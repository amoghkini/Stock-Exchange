import os
import sys
import platform


class OSUtils:
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
