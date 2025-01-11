from pydantic import BaseModel


class InstructionBase(BaseModel):
    step_number: int
    instruction_text: str


class InstructionCreate(InstructionBase):
    # Inherits all fields from InstructionBase and adds:
    recipe_id: int

    # Contains:
    # - step_number: int
    # - instruction_text: str
    # - recipe_id: int


class InstructionResponse(InstructionBase):
    instruction_id: int
