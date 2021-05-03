"""
Note: this is significantly refactored to use the Imperative (a.k.a. Classical) Mappings (https://docs.sqlalchemy.org/en/14/orm/mapping_styles.html#imperative-a-k-a-classical-mappings)
That would have been common in 1.3.x and earlier.
"""
import logging
from typing import Text
from sqlalchemy import (
    Table,
    MetaData,
    Column,
    Integer,
    String,
    DateTime,
    Text,
    event,
)

from sqlalchemy.orm import registry, mapper, relationship

from src.barkylib.domain.models import Equipment

mapper_registry = registry()
Base = mapper_registry.generate_base()

logger = logging.getLogger(__name__)
metadata = MetaData()

"""
Pure domain equipment:
id INTEGER PRIMARY KEY AUTOINCREMENT,
manufacturer TEXT NOT NULL,
model TEXT NOT NULL,
install location TEXT NOT NULL,
need by date TEXT,
lead time INTERGER,
vendor TEXT
"""

equipments = Table(
    "equipment",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True, unique=True),
    Column("manufacturer", String(255)),
    Column("model", String(255)),
    Column("install_location", Text),
    Column("need_by_date", Text),
    Column("lead_time", Text),
    Column("vendor", Text),
    Column("po", Text),
)

def start_mappers():
    
    logger.info("starting mappers")
    # mapper_registry.map_imperatively(Bookmark, bookmarks)
    mapper(Equipment, equipments)

