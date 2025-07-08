import logging
import socket


class NetworkUtils:
    """
    This class provides utility methods for working with networking.
    """
    
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
