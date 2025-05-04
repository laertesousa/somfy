from dataclasses import dataclass
from enum import Enum


class Direction(Enum):
    up = "up"
    down = "down"

@dataclass
class Position:
    cause: str
    direction: str
    source: str
    status: str
    value: int

@dataclass
class Status:
    target_id: str
    position: Position

    def is_moving(self) -> bool:
        return self.position.cause != 'target reached'

    def get_direction(self) -> Direction:
        if self.position.direction == 'up / open':
            return Direction.up

        return Direction.down

    @staticmethod
    def from_data(data: dict):
        position_data = data.get("position")
        position = Position(
            cause=position_data['cause'],
            direction=position_data['direction'],
            source=position_data['source'],
            status=position_data['status'],
            value=int(position_data['value'])
        )

        return Status(
            target_id=data['targetID'],
            position=position
        )

@dataclass
class Device:
    ip: str
    mac: str

    @staticmethod
    def from_data(data: dict):
        return Device(data['ip'], data['mac'])