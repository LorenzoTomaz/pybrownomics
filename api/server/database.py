
import motor.motor_asyncio

from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb+srv://glaicon:v7nQsK9X131QLrzB3SvxeohWFDD@cluster0.ycwx8.mongodb.net/?retryWrites=true&w=majority"


client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.simulations

simulation_collection = database.get_collection("simulation_collection")


# helpers
def simulation_helper(simulation) -> dict:
    return {
        "id": str(simulation["_id"]),
        "wallet": simulation["wallet"]
    }


# Retrieve all simulations present in the database
async def retrieve_simulations():
    simulations = []
    async for simulation in simulation_collection.find():
        simulations.append(simulation_helper(simulation))
    return simulations


# Add a new simulation into to the database
async def add_simulation(simulation_data: dict) -> dict:
    simulation = await simulation_collection.insert_one(simulation_data)
    new_simulation = await simulation_collection.find_one({"_id": simulation.inserted_id})
    return simulation_helper(new_simulation)


# Retrieve a simulation with a matching ID
async def retrieve_simulation(id: str) -> dict:
    simulation = await simulation_collection.find_one({"_id": ObjectId(id)})
    if simulation:
        return simulation_helper(simulation)


# Update a simulation with a matching ID
async def update_simulation(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    simulation = await simulation_collection.find_one({"_id": ObjectId(id)})
    if simulation:
        updated_simulation = await simulation_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_simulation:
            return True
        return False


# Delete a simulation from the database
async def delete_simulation(id: str):
    simulation = await simulation_collection.find_one({"_id": ObjectId(id)})
    if simulation:
        await simulation_collection.delete_one({"_id": ObjectId(id)})
        return True