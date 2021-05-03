'''

This set of tests verifies that the input equipment line item has all required fields


'''

from datetime import date, datetime, timedelta
import random

from src.barkylib.domain import events
from src.barkylib.domain.models import Equipment

ok_urls = ["http://", "https://"]

# test that equipment key is unique
def test_equipment_id_is_unique():
    pass

# this test verifies that the equipment manufacturer is populated
def test_new_equipment_manufacturer_is_populated():
    # arrange
    need_by_date: datetime = datetime.now()
    equipment_manufacturer = "Test_Manufacturer"

    # act
    equipment_item = Equipment(0, equipment_manufacturer, "Test_Model", "Test_Install_Location", need_by_date, None, None, None)

    # assert
    assert equipment_item.manufacturer == equipment_manufacturer

# this test will verify that the model is populated
def test_new_equipment_model_is_populated():
    # arrange
    need_by_date: datetime = datetime.now()
    equipment_manufacturer = "Test_Manufacturer"
    equipment_model = "Test_Model"

    # act
    equipment_item = Equipment(0, equipment_manufacturer, equipment_model, "Test_Install_Location", need_by_date, None, None, None)

    # assert
    assert equipment_item.model == equipment_model

# this test will verify that the install location is populated
def test_new_equipment_install_location_is_populated():
    # arrange
    need_by_date: datetime = datetime.now()
    equipment_manufacturer = "Test_Manufacturer"
    equipment_model = "Test_Model"
    equipment_install_location = "Test_Install_Location"

    # act
    equipment_item = Equipment(0, equipment_manufacturer, equipment_model, equipment_install_location , need_by_date, None, None, None)

    # assert
    assert equipment_item.install_location == equipment_install_location

# this test will verify that the "need by" date is formatted correctly
def test_new_equipment_need_by_date_is_formatted():
    # arrange
    need_by_date: datetime = datetime.now()
    equipment_manufacturer = "Test_Manufacturer"
    equipment_model = "Test_Model"
    equipment_install_location = "Test_Install_Location"

    # act
    equipment_item = Equipment(0, equipment_manufacturer, equipment_model, equipment_install_location , need_by_date, None, None, None)

    # assert
    assert type(equipment_item.need_by_date) == datetime

# this test will verify that lead time can be populated
def test_new_equipment_lead_time_is_populated():
    # arrange
    need_by_date: datetime = datetime.now()
    equipment_manufacturer = "Test_Manufacturer"
    equipment_model = "Test_Model"
    equipment_install_location = "Test_Install_Location"
    equipment_lead_time = 10

    # act
    equipment_item = Equipment(0, equipment_manufacturer, equipment_model, equipment_install_location , need_by_date, equipment_lead_time, None, None)

    # assert
    assert equipment_item.lead_time == equipment_lead_time

# this test will verify that vendor can be populated
def test_new_equipment_vendor_is_populated():
    # arrange
    need_by_date: datetime = datetime.now()
    equipment_manufacturer = "Test_Manufacturer"
    equipment_model = "Test_Model"
    equipment_install_location = "Test_Install_Location"
    equipment_lead_time = 10
    equipment_vendor = "Test_Vendor"

    # act
    equipment_item = Equipment(0, equipment_manufacturer, equipment_model, equipment_install_location , need_by_date, equipment_lead_time, equipment_vendor, None)

    # assert
    assert equipment_item.vendor == equipment_vendor

# this test will verify that po can be populated
def test_new_equipment_po_is_populated():
    # arrange
    need_by_date: datetime = datetime.now()
    equipment_manufacturer = "Test_Manufacturer"
    equipment_model = "Test_Model"
    equipment_install_location = "Test_Install_Location"
    equipment_lead_time = 10
    equipment_vendor = "Test_Vendor"
    equipment_po = "Test_PO"

    # act
    equipment_item = Equipment(0, equipment_manufacturer, equipment_model, equipment_install_location , need_by_date, equipment_lead_time, equipment_vendor, equipment_po)

    # assert
    assert equipment_item.po == equipment_po