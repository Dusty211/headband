from typing import List, Optional
from sqlmodel import Field, SQLModel, Column, JSON
from pgvector.sqlalchemy import Vector

class Sources(SQLModel, table=True):
    __tablename__ = "sources"

    id: Optional[int] = Field(default=None, primary_key=True)
    source: str = Field(index=True)
    meta: Optional[dict] = Field(default=None, sa_column=Column(JSON))

class Chunks(SQLModel, table=True):
    __tablename__ = "chunks"

    id: Optional[int] = Field(default=None, primary_key=True)
    source_id: int = Field(foreign_key="sources.id")
    chunk: str
    meta: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    embedding: List[float] = Field(sa_column=Column(Vector(4096)))