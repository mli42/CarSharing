from datetime import datetime
from typing import Dict, List


class Getaround:
    def __init__(self, input_data: Dict):
        self.output = list()
        self.cars = {car['id']: car for car in input_data['cars']}
        self.rentals = {rental['id']: rental for rental in input_data['rentals']}


    @staticmethod
    def get_price_per_day(duration: int, car_price: int) -> int:
        """Compute the price per day according to the discounts:
            After X days, we apply Y ratio discount on the price per day
            (e.g. 0.5 ratio after 10 days of rentals)
        Args:
            duration (int): duration of the rental in days
            car_price (int): car price per day in cents
        Returns:
            int: computed price for the rental duration
        """
        price_per_day = 0
        discounts = [
            (0.5, 10),
            (0.7, 4),
            (0.9, 1),
            (1.0, 0),
        ]

        for discount_ratio, min_days in discounts:
            if duration <= min_days:
                continue
            discounted_days = duration - min_days
            duration -= discounted_days
            price_per_day += discounted_days * discount_ratio * car_price
        return int(price_per_day)


    def compute_one_rental(self, rental_id: int) -> Dict['id', 'price']:
        """Compute one rental, referred by its ID.
        Returns:
            Dict: Output for the matching rental containing the price.
        """
        rental = self.rentals[rental_id]
        car = self.cars[rental['car_id']]
        parse_date = lambda date_string: datetime.strptime(date_string, '%Y-%m-%d').date()

        start_date = parse_date(rental['start_date'])
        end_date = parse_date(rental['end_date'])
        duration_in_days = (end_date - start_date).days + 1

        price = (
            self.get_price_per_day(duration_in_days, car['price_per_day'])
            + (rental['distance'] * car['price_per_km'])
        )
        return { 'id': rental_id, 'price': price }


    def compute_rentals(self) -> List:
        """Compute all rentals (by calling self.compute_one_rental)
        Returns:
            List: All rentals
        """
        for rental_id in self.rentals.keys():
            price = self.compute_one_rental(rental_id)
            self.output.append(price)
        return self.output
