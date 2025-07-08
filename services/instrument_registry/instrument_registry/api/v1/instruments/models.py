from sqlalchemy import Column, String, Boolean, Date
from instrument_registry.database.base import BaseModel
from instrument_registry.config.config_manager import ConfigManager


class Instrument(BaseModel):
    __tablename__ = "instruments"
    __table_args__ = (
        {"postgresql_partition_by": "date"} if ConfigManager.get_config().ENABLE_PARTITIONING else {}
    )

    name = Column(String, nullable=False)
    trade_date = Column(Date, nullable=False)
    is_active = Column(Boolean, nullable=False, default=True)
    
    def __repr__(self) -> str:
        return f"<Instrument name={self.name} trade_date={self.trade_date} is_active={self.is_active}>"

    def __str__(self) -> str:
        return self.__repr__()

    def to_dict(self) -> dict[str, str]:
        return self.__dict__
