from teams.exceptions import NegativeTitlesError, InvalidYearCupError, ImpossibleTitlesError
from datetime import datetime, timedelta


from datetime import datetime

# Restante do código...

def data_processing(data):
    titles = data.get('titles')
    first_cup = data.get('first_cup')

    if titles is not None and titles < 0:
        raise NegativeTitlesError()

    if first_cup is not None:
        try:
            first_cup_date = datetime.strptime(first_cup, "%Y-%m-%d")
        except ValueError:
            raise InvalidYearCupError()

        if first_cup_date.year < 1930 or (first_cup_date.year - 1930) % 4 != 0:
            raise InvalidYearCupError()

        expected_years = (datetime.now().year - first_cup_date.year) // 4 + 1
        if titles is not None and titles > expected_years:
            raise ImpossibleTitlesError()
