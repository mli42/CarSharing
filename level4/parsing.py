from utils.json import loadJSON
from typing import Dict, Tuple, List, cast, TypedDict

from Getaround.Car import Car, CarInit
from Getaround.RentalRequest import RentalRequest, RentalRequestInit


class InputType(TypedDict):
    cars: List[CarInit]
    rentals: List[RentalRequestInit]


def parse_input(json_path: str) -> Tuple[Dict[int, Car], Dict[int, RentalRequest]]:
    """Parse cars and rentals from a file. The validity of the input is assumed
    Args:
        json_path (str): path to json file
    Returns:
        Tuple[Dict[int, Car], Dict[int, RentalRequest]]: tuple containing
        dictionnaries of Cars and Rentals where their key is their id
    """
    input_data = cast(InputType, loadJSON(json_path))

    cars = {
        car['id']: Car(car) for car in input_data['cars']
    }
    rentals = {
        rental['id']: RentalRequest(rental) for rental in input_data['rentals']
    }
    return (cars, rentals)
