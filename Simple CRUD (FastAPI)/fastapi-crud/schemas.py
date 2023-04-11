from pydantic import BaseModel
from typing import Union,Optional

class Magician(BaseModel):
    fullname: str
    description : str
    class Config:
        allow_population_by_field_name = True
        schema_extra = {
            "example" : {
                "fullname" : "Azure",
                "description" : "Frozen Power"
            }
        }
    