import json
from typing import Dict

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
    string = json.dumps(rentals, indent=2)
    try:
        with open(path, 'w') as fd:
            fd.write(string + '\n')
    except Exception as e:
        print(e)
        exit(1)
    print(f"Successfully written file at {path}")
