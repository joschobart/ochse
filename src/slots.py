import datetime
from json import dumps as jd

class Slots:
    DEFAULT_SHIFTS = {
        "Montag": {
            0: "15:30:00",
        },
        "Dienstag": {
            0: "15:30:00",
        },
        "Mittwoch": {
            0: "15:30:00",
        },
        "Donnerstag": {
            0: "15:30:00",
        },
        "Freitag": {
            0: "15:30:00",
            1: "19:30:00",
        },
        "Samstag": {
            0: "13:30:00",
            1: "19:30:00",
        },
    }

    def __init__(self, year, month, shifts={}):
        self.year = year
        self.month = month
        self.shifts = shifts

    @staticmethod
    def workdays_of_month(year, month):
        workdays = []
        weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]

        month_name  = datetime.datetime.strptime(f"{month}", "%b")
        month_nr = int(month_name.strftime("%m"))
        last_day_of_month =  datetime.date(year, month_nr, 1).replace(day=1) - datetime.timedelta(days=1)

        for day in range(1, int(last_day_of_month.day) + 1):
            weekday = datetime.datetime(year, month_nr, day).weekday()
            if weekdays[weekday] == "Sonntag":
                continue
            workdays.append((f"{year}-{month_nr:02d}-{day:02d}", weekdays[weekday]))

        return workdays

    def get_slots(self, workdays):
        shifts_per_weekday = self.shifts or self.DEFAULT_SHIFTS
        return {
            workday[0]: {
                "weekday": workday[1],
                "nr_slots": len(shifts_per_weekday.get(workday[1], {})),
                "slots": shifts_per_weekday.get(workday[1], {}),
            }
            for workday in workdays
        }

    def get_workdays_and_slots(self):
        workdays = self.workdays_of_month(self.year, self.month)
        return self.get_slots(workdays)

    def to_json(self):
        workdays_and_slots = self.get_workdays_and_slots()
        return jd(workdays_and_slots, indent=4)


# Example usage:
# slots = Slots(2025, "Aug")
# workdays_and_slots = slots.get_workdays_and_slots()
# print(workdays_and_slots)

# json_output = slots.to_json()
# print(json_output)

# Example usage with custom shifts:
# custom_shifts = {
#     "Montag": {
#         0: "10:00:00",
#     },
#     "Dienstag": {
#         0: "11:00:00",
#     },
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
