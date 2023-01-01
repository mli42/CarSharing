import unittest
from typing import List
from Getaround.Getaround import Getaround
from Getaround.RentalRequest import RentalRequest, RentalRequestInit
from Getaround.Car import Car

cars = [
    Car({"id": 1, "price_per_day": 2000, "price_per_km": 10}),
    Car({"id": 2, "price_per_day": 1000, "price_per_km": 10})
]
rentals: List[RentalRequestInit] = [
    {"id": 1, "car_id": 1, "start_date": "2015-12-8",
     "end_date": "2015-12-8", "distance": 100},
    {"id": 2, "car_id": 1, "start_date": "2015-03-31",
     "end_date": "2015-04-01", "distance": 300},
    {"id": 3, "car_id": 1, "start_date": "2015-07-3",
     "end_date": "2015-07-14", "distance": 1000}
]


class TestRentalRequest(unittest.TestCase):
    def test_duration(self):
        config = (
            (0, 1),
            (1, 2),
            (2, 12),
        )
        for rental_index, expected in config:
            rental = RentalRequest(rentals[rental_index])
            self.assertEqual(rental.duration, expected)

    def test_date_exception(self):
        with self.assertRaises(ValueError):
            RentalRequest({"id": 1, "car_id": 1, "start_date": "2015-12-8",
                           "end_date": "2015-12-2", "distance": 100})


class TestGetaround(unittest.TestCase):
    def test_price_per_day(self):
        config = (
            (1, 2000, 2000),
            (2, 2000, 3800),
            (12, 2000, 17800),
        )
        for duration, car_price, expected in config:
            res = Getaround.get_price_per_day(duration, car_price)
            self.assertEqual(res, expected)

    def test_price(self):
        config = (
            (0, 0, 3000),
            (1, 0, 6800),
            (2, 0, 27800),
        )
        for rental_index, car_index, expected in config:
            res = Getaround.get_price(
                RentalRequest(rentals[rental_index]),
                cars[car_index]
            )
            self.assertEqual(res, expected)

    def test_exception_commission(self):
        rental = RentalRequest({"id": 1, "car_id": 1, "start_date": "2015-12-1",
                                "end_date": "2015-12-31", "distance": 100})
        price = Getaround.get_price(rental, cars[1])

        with self.assertRaises(Exception):
            transactions = Getaround.get_transactions(price, rental.duration)
            actions = Getaround.transactions_to_action(transactions)
            print(transactions)
            print(actions)

    def test_transactions(self):
        rental = RentalRequest(rentals[0])
        price = Getaround.get_price(rental, cars[0])
        transactions = Getaround.get_transactions(price, rental.duration)

        self.assertEqual(transactions['driver'], -3000)
        self.assertEqual(transactions['owner'], 2100)
        self.assertEqual(transactions['insurance'], 450)
        self.assertEqual(transactions['assistance'], 100)
        self.assertEqual(transactions['drivy'], 350)


if __name__ == '__main__':
    unittest.main()
