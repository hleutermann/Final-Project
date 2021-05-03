from __future__ import annotations
from dataclasses import asdict
from typing import List, Dict, Callable, Type, TYPE_CHECKING

from src.barkylib.domain import commands, events, models

if TYPE_CHECKING:
    from . import unit_of_work

def add_equipment(
    cmd: commands.AddEquipmentCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        # look to see if we already have this bookmark as the title is set as unique
        ''' not necessary due to this not having to be unique'''
        equipments = uow.equipments.get_by_id(value=cmd.id)

        # checks to see if the list is empty
        if not equipments:
            equipment = models.Equipment(
                cmd.id, cmd.manufacturer, cmd.model, cmd.install_location, cmd.need_by_date, cmd.lead_time, cmd.vendor, cmd.po
            )
            uow.equipments.add(equipment)
        uow.commit()

# ListEquipmentCommand: order_by: str order: str
def list_equipment(
    cmd: commands.ListEquipmentCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    equipments = None
    with uow:
        equipments = uow.equipments.all()
        
    return equipments


# DeleteEquipmentCommand: id: int
def delete_equipment(
    cmd: commands.DeleteEquipmentCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        pass


# EditEquipmentCommand(Command):
def edit_equipment(
    cmd: commands.EditEquipmentCommand,
    uow: unit_of_work.AbstractUnitOfWork,
):
    with uow:
        pass


EVENT_HANDLERS = {
    events.EquipmentAdded: [add_equipment],
    events.EquipmentListed: [list_equipment],
    events.EquipmentDeleted: [delete_equipment],
    events.EquipmentEdited: [edit_equipment],
}  # type: Dict[Type[events.Event], List[Callable]]

COMMAND_HANDLERS = {
    commands.AddEquipmentCommand: add_equipment,
    commands.ListEquipmentCommand: list_equipment,
    commands.DeleteEquipmentCommand: delete_equipment,
    commands.EditEquipmentCommand: edit_equipment,
}  # type: Dict[Type[commands.Command], Callable]
