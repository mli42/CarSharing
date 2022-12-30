import json
import argparse
from typing import Dict, List
from Getaround import Getaround


def loadJSON(path: str) -> Dict:
    """Open and load file as JSON
    Args:
        path (str): path of the json file
    Returns:
        Dict: the json data as a dictionnary
        Exits with error code 1 if an exception is caught
    """
    try:
        with open(path, 'r') as fd:
            data = json.load(fd)
    except Exception as e:
        print(e)
        exit(1)
    return data


def saveJSON(rentals: Dict, path: str) -> None:
    """Save the output to json file, exit(1) on error
    Args:
        rentals (Dict): output to be saved
        path (str): path to json file
    """
    string = json.dumps(rentals, sort_keys=True, indent=2)
    try:
        with open(path, 'w') as fd:
            fd.write(string + '\n')
    except Exception as e:
        print(e)
        exit(1)
    print(f"Successfully written file at {path}")


def main():
    """
    python3 main.py --help
    """
    INPUT_PATH = './data/input.json'
    OUTPUT_PATH = './data/output.json'
    EXPECTED_PATH = './data/expected_output.json'

    parser = argparse.ArgumentParser(description=f'Generate {OUTPUT_PATH} from {INPUT_PATH} according to our rental service plan')
    parser.add_argument('--test', action='store_true', help=f'Check if the output is equal to the expected one ({EXPECTED_PATH})')
    args = parser.parse_args()

    input_data = loadJSON(INPUT_PATH)
    rental_service = Getaround(input_data)

    rental_service.compute_rentals()
    output = { 'rentals': rental_service.output }
    saveJSON(output, OUTPUT_PATH)

    if args.test is True:
        expected_data = loadJSON(EXPECTED_PATH)
        print(f"Correct output: {expected_data == output}")


if __name__ == "__main__":
    main()
