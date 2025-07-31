import datetime
from json import dumps as jd

class Slots:
    """
    A class to manage slots for different days of the week.

    Attributes:
        DEFAULT_SHIFTS (dict): A dictionary of default shifts for each day of the week.
        MONTHS (list): A list of valid month abbreviations.
    """
    DEFAULT_SHIFTS = {
        "Montag": [
            {"start_time": "15:30:00", "taken": None},
        ],
        "Dienstag": [
            {"start_time": "15:30:00", "taken": None},
        ],
        "Mittwoch": [
            {"start_time": "15:30:00", "taken": None},
        ],
        "Donnerstag": [
            {"start_time": "15:30:00", "taken": None},
        ],
        "Freitag": [
            {"start_time": "15:30:00", "taken": None},
            {"start_time": "19:30:00", "taken": None},
        ],
        "Samstag": [
            {"start_time": "13:30:00", "taken": None},
            {"start_time": "19:30:00", "taken": None},
        ],
    }
    MONTHS = ["jan", "feb", "mar", "apr", "may", 
              "jun", "jul", "aug", "sep", "oct", "nov", "dec",]

    def __init__(self, year: int, month: str, shifts: dict = None):
        """
        Initializes a Slots object.

        Args:
            year (int): The year.
            month (str): The month abbreviation (e.g., "jan", "feb", etc.).
            shifts (dict, optional): A dictionary of custom shifts. Defaults to None.

        Raises:
            ValueError: If the month abbreviation is invalid.
        """
        if not month.lower() in self.MONTHS:
            raise ValueError("Invalid month, valid examples: oct, nov, dec")
        self.year = year
        self.month = month
        self.shifts = shifts if shifts else {}

    @staticmethod
    def workdays_of_month(year: int, month: str) -> list:
        """
        Returns a list of workdays in a given month.

        Args:
            year (int): The year.
            month (str): The month abbreviation (e.g., "jan", "feb", etc.).

        Returns:
            list: A list of tuples containing the date and weekday.
        """
        workdays = []
        weekdays = ["Montag", "Dienstag", "Mittwoch", 
                    "Donnerstag", "Freitag", "Samstag", "Sonntag",]

        month_name  = datetime.datetime.strptime(f"{month}", "%b")
        month_nr = int(month_name.strftime("%m"))
        last_day_of_month =  datetime.date(year, month_nr, 1).replace(day=1) - datetime.timedelta(days=1)

        for day in range(1, int(last_day_of_month.day) + 1):
            weekday = datetime.datetime(year, month_nr, day).weekday()
            workdays.append((f"{year}-{month_nr:02d}-{day:02d}", weekdays[weekday]))

        return workdays

    def get_slots(self, workdays: list) -> dict:
        """
        Returns a dictionary of slots for each workday.

        Args:
            workdays (list): A list of workdays.

        Returns:
            dict: A dictionary of slots for each workday.
        """
        shifts_per_weekday = self.shifts or self.DEFAULT_SHIFTS
        return {
            workday[0]: {
                "weekday": workday[1],
                "nr_slots": len(shifts_per_weekday.get(workday[1], [])),
                "slots": shifts_per_weekday.get(workday[1], []),
            }
            for workday in workdays if len(shifts_per_weekday.get(workday[1], [])) > 0
        }

    def get_workdays_and_slots(self) -> dict:
        """
        Returns a dictionary of workdays and slots.

        Returns:
            dict: A dictionary of workdays and slots.
        """
        workdays = self.workdays_of_month(self.year, self.month)
        return self.get_slots(workdays)

    def to_json(self) -> str:
        """
        Returns a JSON representation of the workdays and slots.

        Returns:
            str: A JSON string.
        """
        workdays_and_slots = self.get_workdays_and_slots()
        return jd(workdays_and_slots, indent=4)


# Example usage:
# def get_values(nested_dict, key):
#     values = []
#     for k, v in nested_dict.items():
#         if k == key:
#             values.append(v)
#         elif isinstance(v, dict):
#             values.extend(get_values(v, key))
#         elif isinstance(v, list):
#             for item in v:
#                 if isinstance(item, dict):
#                     values.extend(get_values(item, key))
#     return values

# slots = Slots(2025, "Aug")

# workdays_and_slots = slots.get_workdays_and_slots()
# print(workdays_and_slots)

# json_output = slots.to_json()
# print(json_output)

# print(f"Nr. of slots: {sum(get_values(workdays_and_slots, "nr_slots"))}")

# Example usage with custom shifts:
# custom_shifts = {
#     "Montag": [
#         {"start_time": "15:30:00", "taken": None},
#     ],
# }
# custom_slots = Slots(2024, "Jan", custom_shifts)
# custom_workdays_and_slots = custom_slots.get_workdays_and_slots()
# print(custom_workdays_and_slots)

# custom_json_output = custom_slots.to_json()
# print(custom_json_output)
# ^--------returns something like this --------v:
# {
#     "2024-01-01": {
#         "weekday": "Montag",
#         "nr_slots": 1,
#         "slots": {
#             "0": "10:00:00"
#         }
#     },
#     "2024-01-02": {
#         "weekday": "Dienstag",
#         "nr_slots": 1,
#         "slots": {
#             "0": "11:00:00"
#         }
#     },
#     "2024-01-03": {
#         "weekday": "Mittwoch",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-04": {
#         "weekday": "Donnerstag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-05": {
#         "weekday": "Freitag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-06": {
#         "weekday": "Samstag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-08": {
#         "weekday": "Montag",
#         "nr_slots": 1,
#         "slots": {
#             "0": "10:00:00"
#         }
#     },
#     "2024-01-09": {
#         "weekday": "Dienstag",
#         "nr_slots": 1,
#         "slots": {
#             "0": "11:00:00"
#         }
#     },
#     "2024-01-10": {
#         "weekday": "Mittwoch",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-11": {
#         "weekday": "Donnerstag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-12": {
#         "weekday": "Freitag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-13": {
#         "weekday": "Samstag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-15": {
#         "weekday": "Montag",
#         "nr_slots": 1,
#         "slots": {
#             "0": "10:00:00"
#         }
#     },
#     "2024-01-16": {
#         "weekday": "Dienstag",
#         "nr_slots": 1,
#         "slots": {
#             "0": "11:00:00"
#         }
#     },
#     "2024-01-17": {
#         "weekday": "Mittwoch",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-18": {
#         "weekday": "Donnerstag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-19": {
#         "weekday": "Freitag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-20": {
#         "weekday": "Samstag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-22": {
#         "weekday": "Montag",
#         "nr_slots": 1,
#         "slots": {
#             "0": "10:00:00"
#         }
#     },
#     "2024-01-23": {
#         "weekday": "Dienstag",
#         "nr_slots": 1,
#         "slots": {
#             "0": "11:00:00"
#         }
#     },
#     "2024-01-24": {
#         "weekday": "Mittwoch",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-25": {
#         "weekday": "Donnerstag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-26": {
#         "weekday": "Freitag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-27": {
#         "weekday": "Samstag",
#         "nr_slots": 0,
#         "slots": {}
#     },
#     "2024-01-29": {
#         "weekday": "Montag",
#         "nr_slots": 1,
#         "slots": {
#             "0": "10:00:00"
#         }
#     },
#     "2024-01-30": {
#         "weekday": "Dienstag",
#         "nr_slots": 1,
#         "slots": {
#             "0": "11:00:00"
#         }
#     },
#     "2024-01-31": {
#         "weekday": "Mittwoch",
#         "nr_slots": 0,
#         "slots": {}
#     }
# }
