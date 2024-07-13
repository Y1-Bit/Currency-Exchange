from dataclasses import dataclass


@dataclass
class Currency:
    id: int | None
    code: str
    name: str
    sign: str
