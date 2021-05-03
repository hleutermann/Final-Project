from datetime import datetime
from sqlalchemy import create_engine
from flask import Flask, jsonify, request
from src.barkylib.adapters.orm import start_mappers, metadata
from src.barkylib.domain import commands
from src.barkylib.api import views
from src.barkylib import bootstrap

app = Flask(__name__)
bus = bootstrap.bootstrap()

@app.route('/')
def index(self):
    return f'Barky API'

@app.route('/add_equipment', methods=['POST'])
def add_equipment():
    # manufacturer, model, install_location, need_by_date, lead_time, vendor
    manufacturer = request.json["manufacturer"]
    model = request.json["model"]
    install_location = request.json["install_location"]
    need_by_date = request.json["need_by_date"]
    lead_time = request.json["lead_time"]
    vendor = request.json["vendor"]
    po = request.json["po"]

    cmd = commands.AddEquipementCommand(
            manufacturer, model, install_location, need_by_date, lead_time, vendor
    )
    bus.handle(cmd)
    return "OK", 201


@app.route("/equipment/<manufacturer>", methods=['GET'])
def get_equipment_by_manufacturer(self, manufacturer):
    result = views.equipment_view(manufacturer, bus.uow)
    if not result:
         return "not found", 404
    return jsonify(result), 200

def get_equipment_by_id(self, id):
    pass

def delete(self, equipment):
    pass

def update(self, equipment):
    pass

if __name__ == "__main__":
    app.run()