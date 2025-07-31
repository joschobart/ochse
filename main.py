import sys
import pandas as pd

from src.worker import Worker
from src.slots import Slots
from src.engine import Engine


def main() -> None:
    """
    The main function.

    Reads an ODS file, creates a list of Worker objects, and prints their details.

    Args:
        None

    Returns:
        None
    """
    if len(sys.argv) != 2:
        print("Usage: python main.py <ods_file>")
        sys.exit(1)

    try:
        ods_file: pd.DataFrame = pd.read_excel(sys.argv[1], engine="odf")
    except Exception as e:
        print(f"Error reading ODS file: {e}")
        sys.exit(1)

    # Create a list of Worker objects
    workers: list[Worker] = []
    for index, row in ods_file.iterrows():
        worker = Worker(
            name=row["Name [Name]"],
            no_go_schichten=row["No-Go-Schichten [Wochentag-Startstunde (zBsp.: Montag-1600)]"],
            frei_tage=row["Frei-Tage [Datum1, Datum2 (zBsp.: 15.08., 17.08.)]"],
            fix_tage=row["Fix-Tage [Wochentag1, Wochentag2 (zBsp.: Mittwoch, Donnerstag)]"],
            anz_tage=row["Anz-Tage [Min.-Max. (zBsp.: 0-4)]"],
            springer=row["Springer [Ja/Nein]"],
            folgetag=row["Folgetag [Ja/Nein]"]
        )
        workers.append(worker)

    # Print the workers
    for worker in workers:
        print(worker.to_dict())
        print()


    slots = Slots(2025, "Aug")
    workdays_and_slots = slots.get_workdays_and_slots()

    engine = Engine(workers, workdays_and_slots)


if __name__ == "__main__":
    main()
