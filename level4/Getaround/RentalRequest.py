from datetime import datetime
from typing import TypedDict


class RentalRequestInit(TypedDict):
    id: int
    car_id: int
    start_date: str
    end_date: str
    distance: int


class RentalRequest:
    def __init__(self, props: RentalRequestInit) -> None:
        self.id = props['id']
        self.car_id = props['car_id']
        self.start_date = self.parse_date(props['start_date'])
        self.end_date = self.parse_date(props['end_date'])
        self.distance = props['distance']

        if (self.start_date > self.end_date):
            raise ValueError('start_date has to be earlier than end_date')
        self.duration = (self.end_date - self.start_date).days + 1

    @staticmethod
    def parse_date(date: str):
        return (
            datetime
            .strptime(date, '%Y-%m-%d')
            .date()
        )
