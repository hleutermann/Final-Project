import requests
from src.barkylib import config

# manufacturer, model, install_location, need_by_date, lead_time, vendor
def post_to_add_equipment(
    manufacturer: str,
    model: str,
    install_location: str,
    need_by_date: str,
    lead_time: str,
    vendor: str,
    po: str,
):
    url = config.get_api_url()

    r = requests.post(
        f"{url}/add_equipment",
        json={
            "manufacturer": manufacturer,
            "model": model,
            "install_location": install_location,
            "need_by_date": need_by_date,
            "lead_time": lead_time,
            "vendor": vendor,
            "po": po,
        },
    )
    assert r.status_code == 201


def get_equipment_by_manufacturer(manufacturer: str):
    url = config.get_api_url()
    return requests.get(f"{url}/equipment/{manufacturer}")
