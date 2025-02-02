from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.instruction import Instruction
from app.schemas.instruction import InstructionResponse

# Initialize API Router for instruction endpoints.
router = APIRouter(prefix="/instructions", tags=["instructions"])


@router.get("/", response_model=List[InstructionResponse])
def get_instructions(db: Session = Depends(get_db)):
    """
    Retrieve all instructions.

    This endpoint returns a list of all instruction records from the database.

    Args:
        db (Session): A SQLAlchemy session provided via dependency injection.

    Returns:
        List[InstructionResponse]: A list of instruction details.
    """
    instructions = db.query(Instruction).all()
    return instructions


@router.get("/{instruction_id}", response_model=InstructionResponse)
def get_instruction(instruction_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a specific instruction by its unique identifier.

    Args:
        instruction_id (int): The ID of the instruction to retrieve.
        db (Session): A SQLAlchemy session provided via dependency injection.

    Raises:
        HTTPException: If no instruction with the given ID exists.

    Returns:
        InstructionResponse: Detailed information about the specified instruction.
    """
    instruction = db.query(Instruction).filter(Instruction.instruction_id == instruction_id).first()
    if not instruction:
        raise HTTPException(status_code=404, detail="Instruction not found")
    return instruction
