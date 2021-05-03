"""
This module utilizes the command pattern - https://en.wikipedia.org/wiki/Command_pattern - to 
specify and implement the business logic layer
"""
import sys
from abc import ABC
from datetime import datetime
from dataclasses import dataclass
from typing import Optional

import requests


class Command(ABC):
    pass


@dataclass
class AddEquipmentCommand(Command):
    """
    This command is a dataclass that encapsulates a bookmark
    This uses type hints: https://docs.python.org/3/library/typing.html
    """
    id: int
    manufacturer: str
    model: str
    install_location: str
    need_by_date: str
    # data["need_by_date"] = datetime.utcnow().isoformat()
    lead_time: Optional[int] = 0
    vendor: Optional[str] = None
    po: Optional[str] = None


@dataclass
class ListEquipmentCommand(Command):
    order_by: str
    order: str


@dataclass
class DeleteEquipmentCommand(Command):
    id: int


@dataclass
class EditEquipmentCommand(Command):
    id: int
    manufacturer: str
    model: str
    install_location: str
    need_by_date: str
    # data["need_by_date"] = datetime.utcnow().isoformat()
    lead_time: Optional[int] = 0
    vendor: Optional[str] = None
    po: Optional[str] = None
