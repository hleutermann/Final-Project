from abc import ABC
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

from .models import Equipment

class Event(ABC):
    pass


@dataclass
class EquipmentAdded(Event):
    id: int
    manufacturer: str
    model: str
    install_location: str
    need_by_date: datetime
    lead_time: Optional[int] = 0
    vendor: Optional[str] = None
    po: Optional[str] = None


@dataclass
class EquipmentEdited(Event):
    id: int
    manufacturer: str
    model: str
    install_location: str
    need_by_date: datetime
    lead_time: Optional[int] = 0
    vendor: Optional[str] = None
    po: Optional[str] = None


@dataclass
class EquipmentListed(Event):
    equipments: list[Equipment]


@dataclass
class EquipmentDeleted(Event):
    equipments: Equipment