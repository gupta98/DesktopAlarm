import datetime
import json
import os
import datetime as dt

FILE_PATH = ".\\.needed\\files\\"


def heal_the_corruption():
    # ------------------ #
    if not os.path.exists(FILE_PATH + "alarm.json"):
        with open(FILE_PATH + "alarm.json", "w") as jsonFile:
            jsonFile.write("[\n]")
    # ------------------ #
    with open(FILE_PATH + "alarm.json", "r") as jsonFile:
        data = jsonFile.read()
    if not data:
        with open(FILE_PATH + "alarm.json", "w") as jsonFile:
            jsonFile.write("[\n]")
    # ------------------ #
    with open(FILE_PATH + "alarm.json", "r") as jsonFile:
        data = jsonFile.read()
    try:
        parsed_json = json.loads(data)
    except:
        with open(FILE_PATH + "alarm.json", "w") as jsonFile:
            jsonFile.write("[\n]")


def insertAlarm(alarm_dict):
    with open(FILE_PATH + "alarm.json", "r") as jsonFile:
        data = jsonFile.read()

    if data:
        data = data.replace("\n", "")
        parsed_json = json.loads(data)

        alarm_dict["CREATE_DATE"] = alarm_dict["LAST_MODIFIED_DATE"]
        parsed_json.append(alarm_dict)

        parsed_json.sort(key=lambda x: x["TIME"])
        with open(FILE_PATH + "alarm.json", "w") as jsonFile:
            print(json.dumps(parsed_json, indent=4, sort_keys=False).replace(": ", ":"), end="", file=jsonFile)

        alarmForToday(force=True)
        return True


def modifyAlarm(alarm_dict):
    with open(FILE_PATH + "alarm.json", "r") as jsonFile:
        data = jsonFile.read()

    if data:
        data = data.replace("\n", "")
        parsed_json = json.loads(data)

        for dictionary in parsed_json:
            if dictionary["TIME"] == alarm_dict["TIME"]:
                dictionary["ALARM_NAME"] = alarm_dict["ALARM_NAME"]
                dictionary["LAST_MODIFIED_DATE"] = alarm_dict["LAST_MODIFIED_DATE"]
                dictionary["LAST_MODIFIED_DATE"] = alarm_dict["LAST_MODIFIED_DATE"]
                dictionary["USER_SPECIAL_DATES"] = dictionary["USER_SPECIAL_DAYS"] = dictionary["USER_SPECIAL_MONTHS"] = \
                    dictionary["USER_SPECIAL_YEARS"] = ""

                old_week_set = set(dictionary["WEEKDAYS"].replace(" ", "").split(","))
                new_week_set = set(alarm_dict["WEEKDAYS"].replace(" ", "").split(","))
                dictionary["WEEKDAYS"] = ", ".join(old_week_set | new_week_set).strip(",").strip()

                old_day_set = set(dictionary["SPECIAL_DAYS"].replace(" ", "").split(","))
                new_day_set = set(alarm_dict["SPECIAL_DAYS"].replace(" ", "").split(","))
                special_days = list(old_day_set | new_day_set)
                try:
                    special_days.sort(key=lambda x: dt.date(year=int(x.split("/")[2]),
                                                            month=int(x.split("/")[1]),
                                                            day=int(x.split("/")[0])))
                except:
                    pass
                dictionary["SPECIAL_DAYS"] = ", ".join(special_days).replace(" ", "").strip(", ")

                dictionary["RINGTONE"] = alarm_dict["RINGTONE"]

                break

        parsed_json.sort(key=lambda x: x["TIME"])
        with open(FILE_PATH + "alarm.json", "w") as jsonFile:
            print(json.dumps(parsed_json, indent=4, sort_keys=False).replace(": ", ":"), end="", file=jsonFile)

        alarmForToday(force=True)
        return True


def createAlarm(alarm_dict):
    heal_the_corruption()

    with open(FILE_PATH + "alarm.json", "r") as jsonFile:
        data = jsonFile.read()

    if data:
        data = data.replace("\n", "")
        parsed_json = json.loads(data)

        flag = False
        if parsed_json:
            for dictionary in parsed_json:
                if dictionary["TIME"] == alarm_dict["TIME"]:
                    flag = True
                    break

        if flag:
            return modifyAlarm(alarm_dict)
        else:
            return insertAlarm(alarm_dict)


def alarmList():
    heal_the_corruption()

    with open(FILE_PATH + "alarm.json", "r") as jsonFile:
        data = jsonFile.read()

    if data:
        data = data.replace("\n", "")
        parsed_json = json.loads(data)

        alarmNameDict = {}
        for dictionary in parsed_json:
            string = f"{dictionary['TIME']} ~~ {dictionary['ALARM_NAME']}"
            alarmNameDict[string] = dictionary

        return alarmNameDict


def deleteAlarm(theAlarm):
    heal_the_corruption()

    with open(FILE_PATH + "alarm.json", "r") as jsonFile:
        data = jsonFile.read()

    if data:
        data = data.replace("\n", "")
        parsed_json = json.loads(data)

        if theAlarm in parsed_json:
            parsed_json.remove(theAlarm)

        parsed_json.sort(key=lambda x: x["TIME"])
        with open(FILE_PATH + "alarm.json", "w") as jsonFile:
            print(json.dumps(parsed_json, indent=4, sort_keys=False).replace(": ", ":"), end="", file=jsonFile)

        alarmForToday(force=True)
        return True


def alarmForToday(force=False):
    heal_the_corruption()

    weekDict = {0: "monday",
                1: "tuesday",
                2: "wednesday",
                3: "thursday",
                4: "friday",
                5: "saturday",
                6: "sunday"}

    today = dt.date.today()
    today = f"{today.day}/{today.month}/{today.year}"

    with open(FILE_PATH + "today_flag.txt", "r") as todayFlag:
        flag = todayFlag.read()

    if flag != today or force:
        weekday = weekDict[datetime.date.today().weekday()]

        with open(FILE_PATH + "alarm.json", "r") as jsonFile:
            data = jsonFile.read()

        if data:
            data = data.replace("\n", "")
            parsed_json = json.loads(data)

            new_json = []
            for alarm in parsed_json:
                if weekday in alarm['WEEKDAYS'].lower() or today in alarm['SPECIAL_DAYS']:
                    new_json.append(alarm)

            new_json.sort(key=lambda x: x['TIME'])
            with open(FILE_PATH + "today.json", "w") as jsonFile:
                print(json.dumps(new_json, indent=4, sort_keys=False).replace(": ", ":"), end="", file=jsonFile)

            with open(FILE_PATH + "today_flag.txt", "w") as todayFlag:
                todayFlag.write(today)


if __name__ == '__main__':
    d = {'ALARM_NAME': 'a', 'TIME': '11:00pm', 'CREATE_DATE': '', 'LAST_MODIFIED_DATE': '14/9/2021',
         'USER_ALARM_TIME': '11:00pm', 'USER_SPECIAL_DATES': '14/9/2021,', 'USER_SPECIAL_DAYS': '1',
         'USER_SPECIAL_MONTHS': '1', 'USER_SPECIAL_YEARS': '2200', 'WEEKDAYS': 'Saturday, Sunday',
         'SPECIAL_DAYS': '14/9/2021, 1/1/2200',
         'RINGTONE': 'F:\\IDM Full\\Songs\\Ringtone\\Ringtone Chokkhe Amar Trishna.mp3'}

    alarmForToday()
