from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime
from typing import List, Optional


"""
Pure domain equipment:
id INTEGER PRIMARY KEY AUTOINCREMENT,
manufacturer TEXT NOT NULL,
model TEXT NOT NULL,
install location TEXT NOT NULL,
need by date TEXT,
lead time INTERGER,
vendor TEXT
po TEXT
"""

class Equipment:

    def __init__(self, id: int, manufacturer: str, model: str, install_location: str, need_by_date: datetime, lead_time: int, vendor: str, po: str):
        self.id = id
        self.manufacturer = manufacturer
        self.model = model
        self.install_location = install_location
        self.need_by_date = need_by_date
        self.lead_time = lead_time
        self.vendor = vendor
        self.po = po
        self.events = []
