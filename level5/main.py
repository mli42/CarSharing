import argparse
from typing import Final

from parsing import parse_input
from utils.json import loadJSON, saveJSON
from Getaround.Getaround import Getaround


def main():
    """
    python3 main.py --help
    """
    INPUT_PATH: Final = './data/input.json'
    OUTPUT_PATH: Final = './data/output.json'
    EXPECTED_PATH: Final = './data/expected_output.json'

    parser = argparse.ArgumentParser(
        description=f'Generate {OUTPUT_PATH} from {INPUT_PATH} according to our rental service plan'
    )
    parser.add_argument(
        '--test',
        action='store_true',
        help=f'Check if the output is equal to the expected one ({EXPECTED_PATH})'
    )
    args = parser.parse_args()

    cars, rentals = parse_input(INPUT_PATH)
    rental_service = Getaround(cars, rentals)

    rental_service.compute_rentals()
    output = {'rentals': rental_service.output}
    saveJSON(output, OUTPUT_PATH)

    if args.test is True:
        expected_data = loadJSON(EXPECTED_PATH)
        print(f"Correct output: {expected_data == output}")


if __name__ == "__main__":
    main()
