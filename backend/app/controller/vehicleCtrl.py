# Vehicle Controller
def create_vehicle():
    data = request.json
    vehicle = {
        "driver_id": data.get("driver_id"),
        "make": data.get("make"),
        "model": data.get("model"),
        "year": data.get("year"),
        "fuel_type": data.get("fuel_type"),
        "engine_capacity": data.get("engine_capacity"),
        "co2_emission": data.get("co2_emission")
    }
    result = vehicles_collection.insert_one(vehicle)
    return jsonify({"message": "Vehicle added", "id": str(result.inserted_id)})

def get_vehicles(driver_id):
    vehicles = list(vehicles_collection.find({"driver_id": driver_id}))
    for vehicle in vehicles:
        vehicle["_id"] = str(vehicle["_id"])
    return jsonify(vehicles)

def get_vehicle(vehicle_id):
    vehicle = vehicles_collection.find_one({"_id": ObjectId(vehicle_id)})
    if vehicle:
        vehicle["_id"] = str(vehicle["_id"])
        return jsonify(vehicle)
    return jsonify({"message": "Vehicle not found"}), 404

def update_vehicle(vehicle_id):
    data = request.json
    update_data = {k: v for k, v in data.items() if v is not None}
    vehicles_collection.update_one({"_id": ObjectId(vehicle_id)}, {"$set": update_data})
    return jsonify({"message": "Vehicle updated successfully"})

def delete_vehicle(vehicle_id):
    vehicles_collection.delete_one({"_id": ObjectId(vehicle_id)})
    return jsonify({"message": "Vehicle deleted successfully"})