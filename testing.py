import json
import datetime as dt

d1 = {
    "ALARM_ID": "202109131942",
    "ALARM_NAME": "Testing Alarm",
    "TIME": "19:42",
    "CREATE_DATE": dt.date.today().strftime("%d/%m/%Y"),
    "WEEKDAYS": ['Sunday', 'Saturday'],
    "SPECIAL_DAYS": ['20211012', '20211018'],
    "RINGTONE": "Ringtone File"
}

with open(".\\.needed\\files\\json.json", "w") as jsonFile:
    print(json.dumps([d1], indent=4, sort_keys=False), end="", file=jsonFile)
