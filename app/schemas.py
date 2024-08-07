from pydantic import BaseModel, Field, field_validator

class ItemBase(BaseModel):
    name: str = Field(..., description="The name of the item")
    description: str = Field(None, description="The description of the item")

    @field_validator("name")
    def name_must_not_be_empty(cls, v):
        if not v:
            raise ValueError("Name must not be empty")
        return v

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True
