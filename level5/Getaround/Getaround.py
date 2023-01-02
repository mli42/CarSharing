from typing import Dict, List

from .Car import Car
from .RentalRequest import RentalRequest


class Getaround:
    def __init__(
        self,
        cars: Dict[int, Car],
        rentals: Dict[int, RentalRequest]
    ):
        self.output = list()
        self.cars = cars
        self.rentals = rentals

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

    @staticmethod
    def get_price(rental: RentalRequest, car: Car) -> int:
        """Compute the price for the whole rental according to the right car
        Args:
            rental (RentalRequest): requested rental
            car (Car): corresponding car of the rental
        Returns:
            int: the price of the rental
        """
        price = (
            Getaround.get_price_per_day(rental.duration, car.price_per_day)
            + (rental.distance * car.price_per_km)
        )
        return price

    @staticmethod
    def get_transactions(rental_price: int, duration: int) -> Dict[str, float]:
        """Compute all the banking transactions.
            The commission is 30% of the rental price, and split like this:
                - half goes to the insurance
                - 100 cents/day goes to the roadside assistance
                - the rest goes to us
        Args:
            duration (int): duration of the rental in days
            rental_price (int): price of the rental
        Returns:
            Dict: Dict with keys: driver, owner, insurance, assistance, drivy
        """
        total_commission = rental_price * 0.3
        owner_credit = rental_price - total_commission

        insurance_fee = total_commission * 0.5
        assistance_fee = duration * 100
        drivy_fee = total_commission - (insurance_fee + assistance_fee)

        if drivy_fee < 0:
            raise Exception(
                f'Undefined behavior, drivy_fee are negative: {drivy_fee = }'
            )

        return {
            'driver': -rental_price,
            'owner': owner_credit,
            'insurance': insurance_fee,
            'assistance': assistance_fee,
            'drivy': drivy_fee,
        }

    @staticmethod
    def apply_rental_options(transactions: Dict[str, float], rental: RentalRequest) -> None:
        """Apply the fees according to the selected options of the rental
            - GPS: 500/day, all the money goes to the owner
            - Baby Seat: 200/day, all the money goes to the owner
            - Additional Insurance: 1000/day, all the money goes to Getaround
        Args:
            transactions (Dict[str, float]): commissions previously computed (without options)
            rental (RentalRequest): corresponding rental
        """
        for option in rental.options:
            if option == 'gps':
                option_cost = 500 * rental.duration
                transactions['owner'] += option_cost
            elif option == 'baby_seat':
                option_cost = 200 * rental.duration
                transactions['owner'] += option_cost
            elif option == 'additional_insurance':
                option_cost = 1000 * rental.duration
                transactions['drivy'] += option_cost
            else:
                raise Exception(f'Unexpected option {option}')
            transactions['driver'] -= option_cost

    @staticmethod
    def transactions_to_action(transactions: Dict[str, float]) -> List:
        """Format transactions to fit the expected output as array of actions
        Args:
            transactions (Dict):
                - keys are the target of the action,
                - values are the amount of the action
        Returns:
            Dict: formatted array of actions with keys: who, type, amount
        """
        actions = []

        for target, amount in transactions.items():
            actions.append({
                'who': target,
                'type': 'credit' if amount >= 0 else 'debit',
                'amount': int(abs(amount)),
            })
        return actions

    def compute_one_rental(self, rental_id: int) -> Dict:
        """Compute one rental, referred by its ID.
        Returns:
            Dict: Output for the matching rental containing:
            - the rental id,
            - the related banking actions.
        """
        rental = self.rentals[rental_id]
        car = self.cars[rental.car_id]

        price = self.get_price(rental, car)
        transactions = self.get_transactions(price, rental.duration)
        self.apply_rental_options(transactions, rental)
        actions = self.transactions_to_action(transactions)
        return {
            'id': rental_id,
            'options': rental.options,
            'actions': actions,
        }

    def compute_rentals(self) -> List:
        """Compute all rentals (by calling self.compute_one_rental)
        Returns:
            List: All rentals
        """
        for rental_id in self.rentals.keys():
            price = self.compute_one_rental(rental_id)
            self.output.append(price)
        return self.output
