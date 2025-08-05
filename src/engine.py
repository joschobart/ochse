from typing import List, Dict, Any, Optional
import pandas as pd
import json


class Engine:
    def __init__(self, workers: List[Dict[str, Any]], slots: Dict[str, Dict[str, Any]]):
        self.workers = self.parse_workers(workers)
        self.workdays_and_slots = slots
        self.fill_slots()

    def parse_workers(self, workers: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        for worker in workers:
            # Convert string representations of days into lists
            worker["Frei-Tage"] = (
                worker["Frei-Tage"].split(", ") if worker["Frei-Tage"] else []
            )
            worker["No-Go-Schichten"] = self.parse_no_go_slots(
                worker["No-Go-Schichten"]
            )
            worker["Fix-Tage"] = (
                worker["Fix-Tage"].split(", ") if pd.notna(worker["Fix-Tage"]) else []
            )
            worker.setdefault("shift_count", 0)  # Initialize shift count
        return workers

    def parse_no_go_slots(self, no_go_str: str) -> List[str]:
        return [slot.split("-")[0] for slot in no_go_str.split(", ")]

    def fill_slots(self):
        for date, details in self.workdays_and_slots.items():
            weekday = details["weekday"]
            available_slots = details["slots"]
            assigned_workers = []

            for slot in available_slots:
                assigned_worker = self.assign_worker_to_slot(
                    date, slot, assigned_workers, weekday
                )
                if assigned_worker:
                    assigned_workers.append(assigned_worker)
                else:
                    print(f"Warning: Could not fill slot on {date}.")

    def assign_worker_to_slot(
        self,
        date: str,
        slot: Dict[str, Any],
        assigned_workers: List[Dict[str, Any]],
        weekday: str,
    ) -> Optional[Dict[str, Any]]:
        for worker in self.workers:
            if self.can_assign_worker(worker, date, slot, assigned_workers, weekday):
                slot["taken"] = worker["Name"]
                worker["shift_count"] += 1  # Update the worker's shift count
                print(worker)
                return worker
        return None

    def can_assign_worker(
        self,
        worker: Dict[str, Any],
        date: str,
        slot: Dict[str, Any],
        assigned_workers: List[Dict[str, Any]],
        weekday: str,
    ) -> bool:
        if worker["Name"] in [w["Name"] for w in assigned_workers]:
            return False  # Already assigned to another slot

        # Check if the worker can work on this date
        if date in worker["Frei-Tage"] or weekday in worker["No-Go-Schichten"]:
            return False

        # Check if the worker must work on a fixed day
        if worker["Fix-Tage"] and weekday not in worker["Fix-Tage"]:
            return False

        # Check the number of shifts already assigned
        if worker["shift_count"] >= int(worker["Anz-Tage"].split("-")[1]):
            return False

        # Check if the worker is a springer
        if worker["Springer"] == "Ja":
            return True

        # Check if the worker has reached their minimum shifts
        if worker["shift_count"] < int(worker["Anz-Tage"].split("-")[0]):
            return True

        # Check for folgetag conditions
        if worker["Folgetag"] == "Ja" and self.is_consecutive_day(
            assigned_workers, date
        ):
            return True

        return False

    def is_consecutive_day(
        self, assigned_workers: List[Dict[str, Any]], date: str
    ) -> bool:
        pass

    def to_dict(self) -> str:
        data = {"workers": self.workers, "workdays_and_slots": self.workdays_and_slots}
        return json.dumps(data, indent=4)
