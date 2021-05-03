import threading
import time
import traceback
from datetime import datetime, timezone
from typing import List
from unittest.mock import Mock
import pytest
from src.barkylib.domain.models import Equipment
from src.barkylib.services import unit_of_work

pytestmark = pytest.mark.usefixtures("mappers")
        
def insert_equipment(session, manufacturer: str, model: str, install_location: str, need_by_date: str, lead_time: str=None, vendor: str=None, po: str=None, ):
    session.execute(
        """
        INSERT INTO equipment (manufacturer, model, install_location, need_by_date, lead_time, vendor, po) 
        VALUES (:manufacturer, :model, :install_location, :need_by_date, :lead_time, :vendor, :po)
        """,
        dict(
            manufacturer = manufacturer,
            model = model,
            install_location = install_location,
            need_by_date = need_by_date,
            lead_time = lead_time,
            vendor = vendor,
            po = po,
        ),
    )

def test_can_retreive_equipment(sqlite_session_factory):
    session = sqlite_session_factory()
    nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)
    insert_equipment(session, f"Test_Manufacturer", f"Test_Model", f"Test_Location", nu.isoformat(), f"Test_Days", f"Test_Vendor", f"Test_PO")
    session.commit()

    equipment: Equipment = None

    uow = unit_of_work.SqlAlchemyUnitOfWork(sqlite_session_factory)
    with uow:
        equipment = uow.equipment.get_by_manufacturer(f"Test_Manufacturer")
        assert equipment.manufacturer == f"Test_Manufacturer"
        # uow.commit()
