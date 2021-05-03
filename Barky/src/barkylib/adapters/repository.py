from abc import ABC, abstractmethod
from datetime import date, datetime, timedelta

# making use of type hints: https://docs.python.org/3/library/typing.html
from typing import List, Set

from src.barkylib.adapters import orm
from src.barkylib.domain.models import Equipment


class AbstractEquipmentRepository(ABC):
    def __init__(self):
        # seen is in reference to events detected
        self.seen = set()

    def add(self, equipment: Equipment) -> None:
        # add to repo
        self._add(equipment)
        # add to event list
        self.seen.add(equipment)

    def get_all(self) -> list[Equipment]:
        equipments: list[Equipment] = self._get_all()
        if equipments:
            self.seen.update(equipments)
        return equipments

    def get_by_id(self, value: int) -> Equipment:
        # get from repo
        equipment: Equipment = self._get_by_id(value)
        if equipment:
            self.seen.add(equipment)
        return equipment

    def get_by_manufacturer(self, value: str) -> list[Equipment]:
        equipments: list[Equipment] = self._get_by_manufacturer(value)
        if equipments:
            self.seen.update(equipments)
        return equipments

    def get_by_model(self, value: str) -> list[Equipment]:
        equipments: list[Equipment] = self._get_by_model(value)
        if equipments:
            self.seen.update(equipments)
        return equipments

    def get_needs_info(self) -> list[Equipment]:
        equipments: list[Equipment] = self._get_needs_info()
        if equipments:
            self.seen.update(equipments)
        return equipments

    def get_needs_to_be_ordered(self) -> list[Equipment]:
        equipments: list[Equipment] = self._get_needs_to_be_ordered()
        if equipments:
            self.seen.update(equipments)
        return equipments

    def get_ordered(self) -> list[Equipment]:
        equipments: list[Equipment] = self._get_ordered()
        if equipments:
            self.seen.update(equipments)
        return equipments

    @abstractmethod
    def _add(self, equipment: Equipment) -> None:
        raise NotImplementedError("Derived classes must implement add_one")

    @abstractmethod
    def _add_all(self, equipments: list[Equipment]) -> None:
        raise NotImplementedError("Derived classes must implement add_all")

    @abstractmethod
    def _delete(equipment: Equipment) -> None:
        raise NotImplementedError("Derived classes must implement delete")

    @abstractmethod
    def _get_all(self) -> list[Equipment]:
        raise NotImplementedError("Derived classes must implement get_all")

    @abstractmethod
    def _get_by_id(self, value: int) -> Equipment:
        raise NotImplementedError("Derived classes must implement get_by_id")

    @abstractmethod
    def _get_by_manufacturer(self, value: str) ->list[Equipment]:
        raise NotImplementedError("Derived classes must implement get_by_manufacturer")

    @abstractmethod
    def _get_by_model(self, value: str) -> list[Equipment]:
        raise NotImplementedError("Derived classes must implement get_by_model")

    @abstractmethod
    def _get_needs_info(self) -> list[Equipment]:
        raise NotImplementedError("Derived classes must implement get_needs_info")

    @abstractmethod
    def _get_needs_to_be_ordered(self) -> list[Equipment]:
        raise NotImplementedError("Derived classes must implement get_needs_to_be_ordered")

    @abstractmethod
    def _get_ordered(self) -> list[Equipment]:
        raise NotImplementedError("Derived classes must implent get_ordered")

    @abstractmethod
    def _update(self, equipment: Equipment) -> None:
        raise NotImplementedError("Derived classes must implement update")

    @abstractmethod
    def _update(self, equipments: list[Equipment]) -> None:
        raise NotImplementedError("Derived classes must implement update")


class SqlAlchemyEquipmentRepository(AbstractEquipmentRepository):
    """
    Uses guidance from the basic SQLAlchemy 1.4 tutorial: https://docs.sqlalchemy.org/en/14/orm/tutorial.html
    """

    def __init__(self, session) -> None:
        super().__init__()
        self.session = session

    def _add(self, equipment: Equipment) -> None:
        self.session.add(equipment)
        # self.session.commit()

    def _add_all(self, equipments: list[Equipment]) -> None:
        self.session.add_all(equipments)
        # self.session.commit()

    def _delete(self, equipment: Equipment) -> None:
        pass

    def _get_all(self) -> list[Equipment]:
        return self.session.query(Equipment).all()

    def _get_by_id(self, value: int) -> Equipment:
        answer = self.session.query(Equipment).filter(Equipment.id == value)
        return answer.one()

    def _get_by_manufacturer(self, value: str) -> list[Equipment]:
        return self.session.query(Equipment).filter(Equipment.manufacturer == value)

    def _get_by_model(self, value: str) -> list[Equipment]:
        return self.session.query(Equipment).filter(Equipment.model == value)

    def _get_needs_info(self) -> list[Equipment]:
        return self.session.query(Equipment).filter((Equipment.vendor == None) or (Equipment.lead_time == None))

    def _get_needs_to_be_ordered(self) -> list[Equipment]:
        return self.session.query(Equipment).filter((Equipment.need_by_date - timedelta(Equipment.lead_time)) <= datetime.now())

    def _get_ordered(self) -> list[Equipment]:
        return self.session.query(Equipment).filter(Equipment.po != None)

    def _update(self, equipment) -> None:
        pass

    def _update(self, equipments: list[Equipment]) -> None:
        pass


class FakeEquipmentRepository(AbstractEquipmentRepository):
    """
    Uses a Python list to store "fake" equipments: https://www.w3schools.com/python/python_lists.asp
    """

    def __init__(self, equipments):
        super().__init__()
        self._equipments = set(equipments)

    def _add(self, equipment) -> None:
        self._equipments.add(equipment)

    def _add_all(self, equipments: list[Equipment]) -> None:
        self._equipments.update(equipments)

    def _delete(self, equipment: Equipment) -> None:
        self._equipments.remove(equipment)

    def _get_all(self) -> list[Equipment]:
        return self._equipments

    # python next function: https://www.w3schools.com/python/ref_func_next.asp
    def _get_by_id(self, value: int) -> Equipment:
        return next((b for b in self._equipments if b.id == value), None)

    def _get_by_manufacturer(self, value: str) -> list[Equipment]:
        return_list = []
        return_list.append(next((b for b in self._equipments if b.manufacturer == value), None))
        return return_list

    def _get_by_model(self, value: str) -> list[Equipment]:
        return_list = []
        return_list.append(next((b for b in self._equipments if b.model == value), None))
        return return_list

    def _get_needs_info(self) -> list[Equipment]:
        return_list = self._equipments
        return_list.remove(next((b for b in self._equipments if((b.vendor != None) and (b.lead_time != None))), None))
        return return_list
    
    def _get_needs_to_be_ordered(self) -> list[Equipment]:
        return_list = self._equipments
        return_list.remove(next((b for b in self._equipments if b.lead_time == None), None))
        return_list.remove(next((b for b in self._equipments if b.need_by_date - timedelta(b.lead_time) > datetime.now()), None))
        return return_list

    def _get_ordered(self) -> list[Equipment]:
        return_list = []
        return_list.append(next((b for b in self._equipments if b.po != None), None))
        return return_list

    def _update(self, equipment: Equipment) -> None:
        try:
            idx = self._equipments.index(equipment)
            bm = self._equipments[idx]
            with equipment:
                bm.id = equipment.id
                bm.manufacturer = equipment.manufacturer
                bm.model = equipment.model
                bm.install_location = equipment.install_location
                bm.need_by_date = equipment.need_by_date
                bm.lead_time = equipment.lead_time
                bm.vendor = equipment.vendor
                self._equipments[idx] = bm
        except:
            self._equipments.append(equipment)

        return None

    def _update(self, equipments: list[Equipment]) -> None:
        for inbm in equipments:
            self._update(inbm)
