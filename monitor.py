from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtMultimedia import *

import json
import sys

import datetime as dt
from plyer import notification

import time

from database import *

main_ui, _ = loadUiType("alarm.ui")


class MainApp(QMainWindow, main_ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Setting the theme #
        self.file = QFile(".\\.needed\\theme\\Irrorater.qss")
        if self.file.open(QFile.ReadOnly | QFile.Text):
            qss = QTextStream(self.file)
            self.setStyleSheet(qss.readAll())
        # Theme set done! #

    def set(self, alarm):
        self.lblAlarmName.setText(alarm['ALARM_NAME'])
        self.lblAlarmTime.setText(alarm['TIME'])

        self.ringtone = alarm['RINGTONE']
        self.url = QUrl.fromLocalFile(self.ringtone)
        self.content = QMediaContent(self.url)
        self.player = QMediaPlayer()
        self.player.setMedia(self.content)

        self.play()

    def restart(self, state):
        if state != QMediaPlayer.StoppedState:
            return
        if self.played == 100:
            return
        self.played += 1
        self.player.play()

    def play(self):
        self.played = 0
        self.player.stateChanged.connect(self.restart)
        self.player.play()


def removeFromToday(alarm):
    with open(FILE_PATH + "today.json", "r") as alarms:
        data = alarms.read()

        if data:
            data = data.replace("\n", "")
            try:
                parsed_json = json.loads(data)
                if alarm in parsed_json:
                    parsed_json.remove(alarm)

                parsed_json.sort(key=lambda x: x["TIME"])
                with open(FILE_PATH + "today.json", "w") as jsonFile:
                    print(json.dumps(parsed_json, indent=4, sort_keys=False).replace(": ", ":"), end="", file=jsonFile)

            except:
                pass


def check():
    now = time.strftime("%I:%M%p")
    with open(FILE_PATH + "today.json", "r") as alarms:
        data = alarms.read()

        if data:
            data = data.replace("\n", "")
            try:
                parsed_json = json.loads(data)

                flag = False
                alarm = {}

                for temp_alarm in parsed_json:
                    if temp_alarm['TIME'].lower() == now.lower():
                        flag = True
                        alarm = temp_alarm
                        break

                if flag:
                    print(flag)
                    app = QApplication(sys.argv)
                    window = MainApp()
                    window.show()
                    removeFromToday(alarm)
                    window.set(alarm)
                    notification.notify(title=alarm['TIME'], message=alarm['ALARM_NAME'])
                    app.exec()

            except:
                pass


if __name__ == '__main__':
    alarmForToday()
    while True:
        check()
        time.sleep(1)
