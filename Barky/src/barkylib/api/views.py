from src.barkylib.services import unit_of_work


def equipment_view(manufacturer: str, uow: unit_of_work.SqlAlchemyUnitOfWork):
    with uow:
        results = uow.session.execute(
            """
            SELECT manufacturer, model FROM equipment WHERE manufacturer = :manufacturer
            """,
            dict(manufacturer=manufacturer),
        )
    return [dict(r) for r in results]