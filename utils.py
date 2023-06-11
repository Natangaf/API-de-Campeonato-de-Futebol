from teams.exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError
from datetime import datetime, timedelta


def data_processing(selection_info):
    titles = selection_info.get('titles')
    first_cup = selection_info.get('first_cup')

    if titles is not None and titles < 0:
        raise NegativeTitlesError()

    if first_cup is not None:
        try:
            first_cup_date = datetime(first_cup, 1, 1)
        except ValueError:
            raise InvalidYearCupError()

        current_year = datetime.now().year
        expected_years = (current_year - first_cup) // 4 + 1
        if titles is not None and titles > expected_years:
            raise ImpossibleTitlesError()
        
data = {
    "name": "França",
    "titles": -3,
    "top_scorer": "Zidane",
    "fifa_code": "FRA",
    "first_cup": "2000-10-18"
}

print(data_processing(data))
