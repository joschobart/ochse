class Worker:
    def __init__(
        self,
        name: str,
        no_go_schichten: list[str],
        frei_tage: list[str],
        fix_tage: list[str],
        anz_tage: str,
        springer: str,
        folgetag: str,
    ):
        """
        Initializes a Worker object.

        Args:
            name (str): The worker's first name.
            no_go_schichten (list[str]): A list of no-go shifts (e.g., "Montag-1600").  # noqa: E501
            frei_tage (list[str]): A list of free days (e.g., ["15.08.", "17.08."]).
            fix_tage (list[str]): A list of fixed days (e.g., ["Mittwoch", "Donnerstag"]).
            anz_tage (str): The number of days (e.g., "0-4").
            springer (str): Whether the worker is a springer ("Ja" or "Nein").
            folgetag (str): Whether the worker works on the next day ("Ja" or "Nein").
        """
        self.name: str = name
        self.no_go_schichten: list[str] = no_go_schichten
        self.frei_tage: list[str] = frei_tage
        self.fix_tage: list[str] = fix_tage
        self.anz_tage: str = anz_tage
        self.springer: str = springer
        self.folgetag: str = folgetag

    def __str__(self) -> str:
        return f"Worker: {self.name}\nNo-Go-Schichten: {self.no_go_schichten}\nFrei-Tage: {self.frei_tage}\nFix-Tage: {self.fix_tage}\nAnz-Tage: {self.anz_tage}\nSpringer: {self.springer}\nFolgetag: {self.folgetag}"  # noqa: E501

    def to_dict(self) -> dict:
        """
        Returns a dictionary representation of the worker.

        Returns:
            dict: A dictionary containing the worker's attributes.
        """
        return {
            "Name": self.name,
            "No-Go-Schichten": self.no_go_schichten,
            "Frei-Tage": self.frei_tage,
            "Fix-Tage": self.fix_tage,
            "Anz-Tage": self.anz_tage,
            "Springer": self.springer,
            "Folgetag": self.folgetag,
        }
