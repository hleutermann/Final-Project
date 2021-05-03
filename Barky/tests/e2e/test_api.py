import pytest
import requests
from datetime import datetime, timezone

from src.barkylib.api.flaskapi import get_equipment_by_manufacturer

from .api_client import post_to_add_equipment, get_equipment_by_manufacturer
import pytest


@pytest.mark.usefixtures("restart_api")
def test_path_correct_returns_202_and_equipment_added():

    nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

    manufacturer = f"Test_Manufacturer"
    model = f"Test_Model"
    install_location = f"Test_Location"
    need_by_date = nu.isoformat()
    lead_time = f"Test_Days"
    vendor = f"Test_Vendor"
    po = f"Test_PO"

    post_to_add_equipment(manufacturer, model, install_location, need_by_date, lead_time, vendor)
    r = get_equipment_by_manufacturer(manufacturer)
    assert r.ok
    assert r.json() == [
        {
            "manufacturer": manufacturer,
            "model": model,
            "install_location": install_location,
        },
    ]



@pytest.mark.usefixtures("restart_api")
def test_incorrect_path_returns_400_and_error_message():

    nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

    manufacturer = f"Test_Manufacturer"
    model = f"Test_Model"
    install_location = f"Test_Location"
    need_by_date = nu.isoformat()
    lead_time = f"Test_Days"
    vendor = f"Test_Vendor"
    po = f"Test_PO"
    r = post_to_add_equipment(manufacturer, model, install_location, need_by_date, lead_time, vendor, po)
    assert r.status_code == 400
    assert r.json()["message"] == f"Invalid manufacturer {manufacturer}"

    r = get_equipment_by_manufacturer(manufacturer)
    assert r.status_code == 404
