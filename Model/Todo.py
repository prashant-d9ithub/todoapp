from pydantic import  BaseModel

# Enter Data Validation Model
class todoModel(BaseModel):
    title: str


# Response Data Validation Model
class todoModelR(BaseModel):
    id: int
    title: str