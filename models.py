import dataclasses
from typing import List


@dataclasses.dataclass
class Event:
    id: str
    title: str
    overview: str


@dataclasses.dataclass
class Period:
    id: str
    title: str
    overview: str
    events: List[Event]


@dataclasses.dataclass
class Build:
    id: str
    title: str
    overview: str
    periods: List[Period]
