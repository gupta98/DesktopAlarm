import datetime as dt


def checkTime(time: str):
    time = time.replace(" ", "")
    state = "A"

    for char in time:
        if state == "A":
            if char == "0":
                state = "B"
            elif char == "1":
                state = "C"
            else:
                return False

        elif state == "B":
            if char in "0123456789":
                state = "D"
            else:
                return False

        elif state == "C":
            if char in "012":
                state = "D"
            else:
                return False

        elif state == "D":
            if char == ":":
                state = "E"
            else:
                return False

        elif state == "E":
            if char in "012345":
                state = "F"
            else:
                return False

        elif state == "F":
            if char in "0123456789":
                state = "G"
            else:
                return False

        elif state == "G":
            if char in "AaPp":
                state = "H"
            else:
                return False

        elif state == "H":
            if char in "Mm":
                state = "S"
            else:
                return False

        elif state == "S":
            return False

    return state == "S"


def checkDay(day: str):
    try:
        day = day.replace(" ", "")
        day = day.rstrip(",")

        first_split = day.split(",")
        day_list = set()

        for element in first_split:
            if "-" in element:
                start, end = map(int, element.split("-"))
                start, end = min(start, end), max(start, end)
                if start > 0 and end < 32:
                    for i in range(start, end + 1):
                        day_list.add(i)
                else:
                    return []

            elif 0 < int(element) < 32:
                day_list.add(int(element))

            else:
                return []

        return sorted(list(day_list))

    except:
        return []


def checkMonth(month: str):
    try:
        month = month.replace(" ", "")
        month = month.rstrip(",")

        first_split = month.split(",")
        month_list = set()

        for element in first_split:
            if "-" in element:
                start, end = map(int, element.split("-"))
                start, end = min(start, end), max(start, end)
                if start > 0 and end < 13:
                    for i in range(start, end + 1):
                        month_list.add(i)
                else:
                    return []

            elif 0 < int(element) < 13:
                month_list.add(int(element))

            else:
                return []

        return sorted(list(month_list))

    except:
        return []


def checkYear(year: str):
    try:
        current_year = dt.date.today().year

        year = year.replace(" ", "")
        year = year.rstrip(",")

        first_split = year.split(",")
        year_list = set()

        for element in first_split:
            if "-" in element:
                start, end = map(int, element.split("-"))
                start, end = min(start, end), max(start, end)
                if start >= current_year and end >= current_year:
                    for i in range(start, end + 1):
                        year_list.add(i)
                else:
                    return []

            elif int(element) >= current_year:
                year_list.add(int(element))

            else:
                return []

        return sorted(list(year_list))

    except:
        return []


def checkValidDate(year, month, day):
    try:
        return dt.date(year, month, day) >= dt.date.today()
    except ValueError:
        return False


def checkSpecialDates(special_dates: str):
    try:
        special_dates = special_dates.replace(" ", "")
        special_dates = special_dates.rstrip(",")

        first_split = special_dates.split(",")
        special_dates_list = set()

        for element in first_split:
            if "-" in element:
                start_date, end_date = element.split("-")

                start_day, start_month, start_year = map(int, start_date.split("/"))
                end_day, end_month, end_year = map(int, end_date.split("/"))

                if dt.date(start_year, start_month, start_day) > dt.date(end_year, end_month, end_day):
                    start_date, end_date = end_date, start_date
                    start_day, start_month, start_year = map(int, start_date.split("/"))
                    end_day, end_month, end_year = map(int, end_date.split("/"))

                date = dt.date(year=start_year, month=start_month, day=start_day)
                end_date = dt.date(year=end_year, month=end_month, day=end_day)

                if date >= dt.date.today() and end_date >= dt.date.today():
                    while True:
                        temp_date = f"{date.day}/{date.month}/{date.year}"
                        special_dates_list.add(temp_date)
                        if date == end_date:
                            break
                        date = date + dt.timedelta(days=1)

                else:
                    return []

            else:
                start_day, start_month, start_year = map(int, element.split("/"))
                date = dt.date(year=start_year, month=start_month, day=start_day)
                if date >= dt.date.today():
                    special_dates_list.add(f"{date.day}/{date.month}/{date.year}")
                else:
                    return []

        return sorted(list(special_dates_list),
                      key=lambda x: dt.date(year=int(x.split("/")[2]), month=int(x.split("/")[1]),
                                            day=int(x.split("/")[0])))

    except:
        return []


def specialDMY(D, M, Y):
    days = checkDay(D)
    if days:
        months = checkMonth(M)
        if months:
            years = checkYear(Y)
            if years:
                special_days = set()

                for year in years:
                    for month in months:
                        for day in days:
                            if checkValidDate(year, month, day):
                                date = dt.date(year, month, day)
                                special_days.add(f"{date.day}/{date.month}/{date.year}")
                return sorted(list(special_days),
                              key=lambda x: dt.date(year=int(x.split("/")[2]), month=int(x.split("/")[1]),
                                                    day=int(x.split("/")[0])))
            else:
                return -3  # No year
        else:
            return -2  # No month
    else:
        return -1  # No day


if __name__ == '__main__':
    D = "1-31"
    M = "1,2,4"
    Y = "2021, 2022"
    print(f"\n\n{D}, {M}, {Y} is {specialDMY(D, M, Y)}")
