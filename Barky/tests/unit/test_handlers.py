'''

This set of tests verifies that the required functions operate correctly


'''

from __future__ import annotations
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from typing import Dict, List
import pytest
from src.barkylib import bootstrap
from src.barkylib.domain import commands
from src.barkylib.domain.models import Equipment
from src.barkylib.services import handlers, unit_of_work
from src.barkylib.adapters import repository

from src.barkylib.adapters.orm import start_mappers
from src.barkylib.services.unit_of_work import FakeUnitOfWork


def boostrap_test_app():
    return bootstrap.bootstrap(start_orm=False, uow=FakeUnitOfWork())

#makes the whole sytem (minus api) run
#this is proof of the system/a test what it does

class TestAddEquipment:

    # this test verifies that a piece of equipment can be added
    def test_add_single_equipment(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

        # add one
        bus.handle(
            commands.AddEquipmentCommand(
                0,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nu.isoformat(),  # Need by Date
                None,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )
        
        assert bus.uow.equipments.get_by_id(0) is not None
        assert bus.uow.committed

    # this test verifies that items are retrieved by equipment id
    def test_get_equipment_by_id(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

        # add one
        bus.handle(
            commands.AddEquipmentCommand(
                99,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nu.isoformat(),  # Need by Date
                None,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        assert bus.uow.equipments.get_by_id(99) is not None
        assert bus.uow.committed

    # this test verifies that items are retrieved by equipment manufacturer
    def test_get_equipment_by_manufacturer(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

        # add one
        bus.handle(
            commands.AddEquipmentCommand(
                0,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nu.isoformat(),  # Need by Date
                None,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        records = bus.uow.equipments.get_by_manufacturer(f"Test_Manufacturer")
        assert len(records) == 1

    # this test verifies that items are retrieved by equipment model
    def test_get_equipment_by_model(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)

        # add one
        bus.handle(
            commands.AddEquipmentCommand(
                0,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nu.isoformat(),  # Need by Date
                None,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        records = bus.uow.equipments.get_by_model(f"Test_Model")
        assert len(records) == 1

    # this test verifies that that items are retrieved by get_all
    def test_get_all_equipments(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)
              
        bus.handle(
            commands.AddEquipmentCommand(
                0,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nu.isoformat(),  # Need by Date
                None,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        nuto = nu + timedelta(days = 2, hours=12)

        bus.handle(
            commands.AddEquipmentCommand(
                1,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nu.isoformat(),  # Need by Date
                None,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        records = bus.uow.equipments.get_all()
        assert len(records) == 2


    # this test verifies that that needs info items are retrieved by get_needs_info
    def test_get_needs_info(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0, tzinfo=timezone.utc)
              
        bus.handle(
            commands.AddEquipmentCommand(
                0,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nu.isoformat(),  # Need by Date
                None,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        nuto = nu + timedelta(days = 2, hours=12)

        bus.handle(
            commands.AddEquipmentCommand(
                1,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nuto.isoformat(),  # Need by Date
                10,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        bus.handle(
            commands.AddEquipmentCommand(
                2,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nuto.isoformat(),  # Need by Date
                None,  # Lead Time
                f"Test_Vendor",  # Vendor
                None,  # PO
            )
        )

        nuthe = nu + timedelta(days = 2, hours=12)

        bus.handle(
            commands.AddEquipmentCommand(
                3,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nuthe.isoformat(),  # Need by Date
                10,  # Lead Time
                f"Test_Vendor",  # Vendor
                None,  # PO
            )
        )

        records = bus.uow.equipments.get_needs_info()
        assert len(records) == 3

    # this test verifies that that needs info items are retrieved by get_needs_to_be_ordered
    def test_get_needs_to_be_ordered(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0)
              
        bus.handle(
            commands.AddEquipmentCommand(
                0,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nu,  # Need by Date
                None,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        nuto = nu + timedelta(days = 2)

        bus.handle(
            commands.AddEquipmentCommand(
                1,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nuto,  # Need by Date
                10,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        nuthe = datetime.now() + timedelta(days = 12)

        bus.handle(
            commands.AddEquipmentCommand(
                2,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nuthe,  # Need by Date
                10,  # Lead Time
                f"Test_Vendor",  # Vendor
                None,  # PO
            )
        )

        records = bus.uow.equipments.get_needs_to_be_ordered()
        assert len(records) == 1

    # this test verifies that that needs info items are retrieved by get_ordered
    def test_get_ordered(self):
        bus = boostrap_test_app()

        nu: datetime = datetime(2021, 3, 31, 0, 0, 0, 0)
              
        bus.handle(
            commands.AddEquipmentCommand(
                0,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nu,  # Need by Date
                None,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        nuto = nu + timedelta(days = 2)

        bus.handle(
            commands.AddEquipmentCommand(
                1,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nuto,  # Need by Date
                10,  # Lead Time
                None,  # Vendor
                None,  # PO
            )
        )

        nuthe = datetime.now() + timedelta(days = 12)

        bus.handle(
            commands.AddEquipmentCommand(
                2,
                f"Test_Manufacturer",  # Manufacturer
                f"Test_Model",  # Model
                f"Test_Install_Location",  # Install Location
                nuthe,  # Need by Date
                10,  # Lead Time
                f"Test_Vendor",  # Vendor
                f"Test_PO",  # PO
            )
        )

        records = bus.uow.equipments.get_ordered()
        assert len(records) == 1