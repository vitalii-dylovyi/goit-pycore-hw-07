from collections import UserDict
from datetime import datetime, timedelta
from typing import Optional, List, Dict
from record import Record


class AddressBook(UserDict):
    def add_record(self, record: Record) -> None:
        self.data[record.name.value] = record

    def find(self, name: str) -> Optional[Record]:
        return self.data.get(name)

    def delete(self, name: str) -> None:
        if name not in self.data:
            raise KeyError(f"Contact {name} not found")
        del self.data[name]

    def get_upcoming_birthdays(self, days: int = 7) -> List[Dict]:
        today = datetime.today().date()
        upcoming_birthdays = []

        for record in self.data.values():
            if not record.birthday:
                continue

            birthday_date = record.birthday.value
            birthday_this_year = birthday_date.replace(year=today.year)

            if birthday_this_year < today:
                birthday_this_year = birthday_this_year.replace(year=today.year + 1)

            days_until = (birthday_this_year - today).days
            if 0 <= days_until <= days:
                congratulation_date = birthday_this_year
                if birthday_this_year.weekday() >= 5:  # Weekend
                    congratulation_date += timedelta(
                        days=(7 - birthday_this_year.weekday())
                    )

                upcoming_birthdays.append(
                    {
                        "name": record.name.value,
                        "birthday": birthday_this_year.strftime("%d.%m.%Y"),
                        "congratulation_date": congratulation_date.strftime("%d.%m.%Y"),
                    }
                )

        return sorted(
            upcoming_birthdays,
            key=lambda x: datetime.strptime(x["birthday"], "%d.%m.%Y"),
        )
