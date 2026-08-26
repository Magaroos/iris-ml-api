from pydantic import BaseModel, Field

class PredictionInput(BaseModel):
    sepal_length: float = Field(..., gt=4, lt=8)
    sepal_width: float = Field(..., gt=2, lt=5)
    petal_length: float = Field(..., gt=1, lt=7)
    petal_width: float = Field(..., gt=0.1, lt=3)