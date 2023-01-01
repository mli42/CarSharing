from typing import TypedDict


class CarInit(TypedDict):
    id: int
    price_per_day: int
    price_per_km: int


class Car:
    def __init__(self, props: CarInit) -> None:
        self.id = props['id']
        self.price_per_day = props['price_per_day']
        self.price_per_km = props['price_per_km']
