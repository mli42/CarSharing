from typing import TypedDict, Literal


RentalOptionType = Literal['gps', 'baby_seat', 'additional_insurance']


class RentalOptionsInit(TypedDict):
    id: int
    rental_id: int
    type: RentalOptionType


class RentalOptions:
    def __init__(self, props: RentalOptionsInit) -> None:
        self.id = props['id']
        self.rental_id = props['rental_id']
        self.type = props['type']
