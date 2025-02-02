from pydantic import BaseModel


class InstructionBase(BaseModel):
    """
    Base model for an instruction step.

    Attributes:
        step_number (int): The number representing the order of this instruction in the recipe.
        instruction_text (str): The textual description of the instruction.
    """
    step_number: int
    instruction_text: str


class InstructionCreate(InstructionBase):
    """
    Schema for creating a new instruction step.

    Inherits all fields from InstructionBase and adds:
        recipe_id (int): The identifier of the recipe to which this instruction belongs.

    Contains:
        - step_number: int
        - instruction_text: str
        - recipe_id: int
    """
    recipe_id: int


class InstructionResponse(InstructionBase):
    """
    Schema for returning instruction details in API responses.

    Inherits all fields from InstructionBase and adds:
        instruction_id (int): The unique identifier for the instruction.
    """
    instruction_id: int
