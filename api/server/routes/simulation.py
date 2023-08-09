from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database import (
    add_simulation,
    delete_simulation,
    retrieve_simulation,
    retrieve_simulations,
    update_simulation,
)
from server.models.simulation import (
    ErrorResponseModel,
    ResponseModel,
    SimulationSchema,
    UpdateSimulationModel,
)

router = APIRouter()

@router.post("/", response_description="Simulation data added into the database")
async def add_simulation_data(simulation: SimulationSchema = Body(...)):
    simulation = jsonable_encoder(simulation)
    new_simulation = await add_simulation(simulation)
    return ResponseModel(new_simulation, "simulation added successfully.")


@router.get("/", response_description="simulations retrieved")
async def get_simulations():
    simulations = await retrieve_simulations()
    if simulations:
        return ResponseModel(simulations, "Simulations data retrieved successfully")
    return ResponseModel(simulations, "Empty list returned")


@router.get("/{id}", response_description="simulation data retrieved")
async def get_simulation_data(id):
    simulation = await retrieve_simulation(id)
    if simulation:
        return ResponseModel(simulation, "simulation data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "simulation doesn't exist.")