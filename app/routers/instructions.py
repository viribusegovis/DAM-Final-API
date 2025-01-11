from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.instruction import Instruction
from app.schemas.instruction import InstructionResponse

router = APIRouter(prefix="/instructions", tags=["instructions"])


@router.get("/", response_model=List[InstructionResponse])
def get_instructions(db: Session = Depends(get_db)):
    instructions = db.query(Instruction).all()
    return instructions


@router.get("/{instruction_id}", response_model=InstructionResponse)
def get_instruction(instruction_id: int, db: Session = Depends(get_db)):
    instruction = db.query(Instruction).filter(Instruction.instruction_id == instruction_id).first()
    if not instruction:
        raise HTTPException(status_code=404, detail="Instruction not found")
    return instruction
