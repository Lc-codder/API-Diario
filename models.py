from dataclasses import dataclass
from typing import Optional

@dataclass
class Category:
    id: Optional[int]
    name: str

@dataclass
class Task:
    id: Optional[int]
    title: str
    description: str
    done: bool
    category_id: Optional[int]