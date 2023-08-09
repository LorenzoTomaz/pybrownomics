from typing import Optional

from pydantic import UUID5, BaseModel, EmailStr, Field


class SimulationSchema(BaseModel):
    wallet: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "wallet": "John Doe"
            }
        }


class UpdateSimulationModel(BaseModel):
    wallet: str = Field(...)

    class Config:
        schema_extra = {
            "example": {
                "wallet": "John Doe"
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}