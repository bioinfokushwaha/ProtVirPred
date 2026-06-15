from pydantic import BaseModel


class PredictionRequest(BaseModel):

    sequence: str

    combination: str