from datetime import datetime, date


class TimeUtils:
    """
    This class provides utility methods for working with dates and times.
    """
    
    @staticmethod
    def get_todays_date() -> date:
        """Get the current date."""
        return datetime.now().date()
    
    @staticmethod
    def get_todays_date_str() -> str:
        """Get the current date in the format YYYYMMDD."""
        return TimeUtils.get_todays_date().strftime("%Y%m%d")
