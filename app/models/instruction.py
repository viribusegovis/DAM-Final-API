from sqlalchemy import Column, Integer, String, ForeignKey

from app.models.base import Base


class Instruction(Base):
    __tablename__ = "instructions"
    instruction_id = Column(Integer, primary_key=True)
    recipe_id = Column(Integer, ForeignKey("recipes.id", ondelete="CASCADE"))
    step_number = Column(Integer, nullable=False)
    instruction_text = Column(String, nullable=False)
