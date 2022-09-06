from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.uic import loadUiType
from PyQt5.QtMultimedia import *

import sys
import os

import json
import datetime as dt
from webbrowser import open as webpage_open
from getpass import getuser

from DFDs import *
from database import *

main_ui, _ = loadUiType("alarmWindow.ui")
view_ui, _ = loadUiType("viewWindow.ui")

ICON_PATH = ".\\.needed\\icons\\"
FILE_PATH = ".\\.needed\\files\\"


class ViewApp(QMainWindow, view_ui):
    def __init__(self, parent=None):
        super(ViewApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Setting the theme #
        self.file = QFile(".\\.needed\\theme\\Irrorater.qss")
        if self.file.open(QFile.ReadOnly | QFile.Text):
            qss = QTextStream(self.file)
            app.setStyleSheet(qss.readAll())
        # Theme set done! #

        self.editParent = None
        self.handleButtons()

        self.alarmNameDict = alarmList()
        for string in sorted(list(self.alarmNameDict.keys())):
            self.lwAlarmList.addItem(string)

    def handleButtons(self):
        self.btnViewAlarmInfo.clicked.connect(self.btnViewAlarmInfoPressed)
        self.lwAlarmList.doubleClicked.connect(self.btnViewAlarmInfoPressed)
        self.btnEditAlarm.clicked.connect(self.btnEditAlarmPressed)
        self.btnDeleteAlarm.clicked.connect(self.btnDeleteAlarmPressed)
        self.btnWhoAmI.clicked.connect(
            lambda: webpage_open("https://www.linkedin.com/in/debtanu-gupta-3b90b4129/") and webpage_open("https://www.facebook.com/debtanu.gupta.7/"))

    def btnViewAlarmInfoPressed(self):
        if len(self.lwAlarmList.selectedItems()):
            try:
                string = ''''''

                for alarm in self.alarmNameDict.values():
                    temp = f"{alarm['TIME']} ~~ {alarm['ALARM_NAME']}"
                    item = self.lwAlarmList.selectedItems()[0].text()

                    if temp == item:
                        string += f"Name: {alarm['ALARM_NAME']}\n\n"
                        string += f"Time: {alarm['TIME']}\n\n"
                        string += f"Create Date: {alarm['CREATE_DATE']}\n\n"
                        string += f"Last Modified: {alarm['LAST_MODIFIED_DATE']}\n\n"
                        string += "Weekdays: " + (alarm['WEEKDAYS'] if alarm['WEEKDAYS'] else "-") + "\n\n"
                        string += "Special Days: " + (alarm['SPECIAL_DAYS'] if alarm['SPECIAL_DAYS'] else "-") + "\n\n"
                        string += f"Ringtone: {alarm['RINGTONE']}" if alarm[
                                                                          'RINGTONE'] != ".\\Basic.mp3" else f"Ringtone: Basic.mp3"

                        break

                self.teAlarmDetails.setText(string)

            except:
                pass

    def btnEditAlarmPressed(self):
        if len(self.lwAlarmList.selectedItems()):
            answer = QMessageBox.question(self, "Edit?", "Do you want to edit the alarm?",
                                          QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                try:
                    flag = False
                    alarm = None
                    for temp_alarm in self.alarmNameDict.values():
                        temp = f"{temp_alarm['TIME']} ~~ {temp_alarm['ALARM_NAME']}"
                        item = self.lwAlarmList.selectedItems()[0].text()

                        if temp == item:
                            alarm = temp_alarm
                            flag = True
                            break

                    if flag:
                        self.editParent = MainApp(self)

                        self.editParent.btnView.setEnabled(False)

                        self.editParent.leAlarmName.setText(alarm["ALARM_NAME"])
                        self.editParent.leTime.setText(alarm["TIME"])
                        self.editParent.teSpecialDates.setText(
                            alarm["USER_SPECIAL_DATES"] if len(alarm["USER_SPECIAL_DATES"]) else alarm["SPECIAL_DAYS"])
                        self.editParent.leSpecialDays.setText(alarm["USER_SPECIAL_DAYS"])
                        self.editParent.leSpecialMonths.setText(alarm["USER_SPECIAL_MONTHS"])
                        self.editParent.leSpecialYears.setText(alarm["USER_SPECIAL_YEARS"])

                        if "monday" in alarm["WEEKDAYS"].lower():
                            self.editParent.chkMonday.setChecked(True)
                        else:
                            self.editParent.chkMonday.setChecked(False)

                        if "tuesday" in alarm["WEEKDAYS"].lower():
                            self.editParent.chkTuesday.setChecked(True)
                        else:
                            self.editParent.chkTuesday.setChecked(False)

                        if "wednesday" in alarm["WEEKDAYS"].lower():
                            self.editParent.chkWednesday.setChecked(True)
                        else:
                            self.editParent.chkWednesday.setChecked(False)

                        if "thursday" in alarm["WEEKDAYS"].lower():
                            self.editParent.chkThursday.setChecked(True)
                        else:
                            self.editParent.chkThursday.setChecked(False)

                        if "friday" in alarm["WEEKDAYS"].lower():
                            self.editParent.chkFriday.setChecked(True)
                        else:
                            self.editParent.chkFriday.setChecked(False)

                        if "saturday" in alarm["WEEKDAYS"].lower():
                            self.editParent.chkSaturday.setChecked(True)
                        else:
                            self.editParent.chkSaturday.setChecked(False)

                        if "sunday" in alarm["WEEKDAYS"].lower():
                            self.editParent.chkSunday.setChecked(True)
                        else:
                            self.editParent.chkSunday.setChecked(False)

                        self.editParent.ringtone = alarm["RINGTONE"]
                        self.editParent.default_ringtone = ".\\Basic.mp3"
                        self.editParent.ringtoneName = self.editParent.ringtone[
                                                       self.editParent.ringtone.rfind("\\") + 1:]
                        self.editParent.lblRingtoneName.setText(self.editParent.ringtoneName)

                        self.editParent.url = QUrl.fromLocalFile(self.editParent.ringtone)
                        self.editParent.content = QMediaContent(self.editParent.url)
                        self.editParent.player = QMediaPlayer()
                        self.editParent.player.setMedia(self.editParent.content)

                        self.editParent.alarmToDelete = alarm
                        self.editParent.setWindowTitle("Edit...")
                        self.editParent.show()

                except:
                    pass

    def btnDeleteAlarmPressed(self):
        if len(self.lwAlarmList.selectedItems()):
            answer = QMessageBox.question(self, "Delete?", "Do you want to delete the alarm?",
                                          QMessageBox.Yes | QMessageBox.No)
            if answer == QMessageBox.Yes:
                try:
                    for alarm in self.alarmNameDict.values():
                        temp = f"{alarm['TIME']} ~~ {alarm['ALARM_NAME']}"
                        item = self.lwAlarmList.selectedItems()[0].text()

                        if temp == item:

                            if deleteAlarm(alarm):
                                self.teAlarmDetails.setText("")

                                self.lwAlarmList.clear()
                                self.alarmNameDict = alarmList()
                                for string in sorted(list(self.alarmNameDict.keys())):
                                    self.lwAlarmList.addItem(string)

                                QMessageBox.information(self, "Deleted!", "Alarm Deleted!")
                            else:
                                QMessageBox.information(self, "Failed!", "Deletion is not possible!")

                            break

                except:
                    pass


class MainApp(QMainWindow, main_ui):
    def __init__(self, parent=None):
        super(MainApp, self).__init__(parent)
        QMainWindow.__init__(self)
        self.setupUi(self)

        # Setting the theme #
        self.file = QFile(".\\.needed\\theme\\Irrorater.qss")
        if self.file.open(QFile.ReadOnly | QFile.Text):
            qss = QTextStream(self.file)
            app.setStyleSheet(qss.readAll())
        # Theme set done! #

        self.ringtone = ".\\Basic.mp3"
        self.default_ringtone = ".\\Basic.mp3"
        self.ringtoneName = "Basic.mp3"
        self.lblRingtoneName.setText(self.ringtoneName)

        self.url = QUrl.fromLocalFile(self.ringtone)
        self.content = QMediaContent(self.url)
        self.player = QMediaPlayer()
        self.player.setMedia(self.content)

        self.parent = parent
        self.alarmToDelete = None
        self.viewWindow = None

        self.handleButtons()

    def handleButtons(self):
        self.btnCheckAll.clicked.connect(self.btnCheckAllPressed)
        self.btnUncheckAll.clicked.connect(self.btnUncheckAllPressed)
        self.btnToday.clicked.connect(self.btnTodayPressed)
        self.btnTomorrow.clicked.connect(self.btnTomorrowPressed)
        self.btnPlay.clicked.connect(self.btnPlayPressed)
        self.btnStop.clicked.connect(self.btnStopPressed)
        self.btnBrowse.clicked.connect(self.btnBrowsePressed)
        self.btnSave.clicked.connect(self.btnSavePressed)
        self.btnView.clicked.connect(self.btnViewPressed)

    # Buttons#
    def btnCheckAllPressed(self):
        self.chkMonday.setChecked(True)
        self.chkTuesday.setChecked(True)
        self.chkWednesday.setChecked(True)
        self.chkThursday.setChecked(True)
        self.chkFriday.setChecked(True)
        self.chkSaturday.setChecked(True)
        self.chkSunday.setChecked(True)

    def btnUncheckAllPressed(self):
        self.chkMonday.setChecked(False)
        self.chkTuesday.setChecked(False)
        self.chkWednesday.setChecked(False)
        self.chkThursday.setChecked(False)
        self.chkFriday.setChecked(False)
        self.chkSaturday.setChecked(False)
        self.chkSunday.setChecked(False)

    def btnTodayPressed(self):
        today = dt.date.today()
        date = f"{today.day}/{today.month}/{today.year}"
        dates = checkSpecialDates(self.teSpecialDates.toPlainText())

        if dates:
            if date not in dates:
                starter = "," if len(self.teSpecialDates.toPlainText().rstrip(",")) else ""
                self.teSpecialDates.setText(self.teSpecialDates.toPlainText().rstrip(",") + starter + date + ",")
            else:
                pass
        else:
            if not len(self.teSpecialDates.toPlainText()):
                starter = "," if len(self.teSpecialDates.toPlainText().rstrip(",")) else ""
                self.teSpecialDates.setText(self.teSpecialDates.toPlainText().rstrip(",") + starter + date + ",")

    def btnTomorrowPressed(self):
        tomorrow = dt.date.today() + dt.timedelta(days=1)
        date = f"{tomorrow.day}/{tomorrow.month}/{tomorrow.year}"
        dates = checkSpecialDates(self.teSpecialDates.toPlainText())

        if dates:
            if date not in dates:
                starter = "," if len(self.teSpecialDates.toPlainText().rstrip(",")) else ""
                self.teSpecialDates.setText(self.teSpecialDates.toPlainText().rstrip(",") + starter + date + ",")
            else:
                pass
        else:
            if not len(self.teSpecialDates.toPlainText()):
                starter = "," if len(self.teSpecialDates.toPlainText().rstrip(",")) else ""
                self.teSpecialDates.setText(self.teSpecialDates.toPlainText().rstrip(",") + starter + date + ",")

    def btnPlayPressed(self):
        self.btnStopPressed()

        if not os.path.exists(self.ringtone):
            self.ringtone = self.default_ringtone
            self.ringtoneName = "Basic.mp3"
            self.lblRingtoneName.setText(self.ringtoneName)

        self.url = QUrl.fromLocalFile(self.ringtone)
        self.content = QMediaContent(self.url)
        self.player = QMediaPlayer()
        self.player.setMedia(self.content)
        self.player.play()

    def btnStopPressed(self):
        self.player.stop()

    def btnBrowsePressed(self):
        self.btnStopPressed()

        path = FILE_PATH + "ringtone_location.txt"

        if os.path.exists(path):
            with open(path, "r") as file:
                location = file.read()

            if not location or not os.path.exists(location):
                with open(path, "w") as file:
                    file.write("C:\\")

        else:
            with open(path, "w") as file:
                file.write("C:\\")

        with open(path, "r") as file:
            location = file.read()

        file = QFileDialog.getOpenFileName(self, "Select Ringtone", location, "*.mp3")[0]
        if file:
            file = file.replace("/", "\\")
            folder = file[:file.rfind("\\") + 1]
            file = file.replace(folder, "")

            with open(path, "w") as temp_file:
                temp_file.write(folder)

            self.ringtone = folder + file
            self.ringtoneName = file
            self.lblRingtoneName.setText(self.ringtoneName)

    def btnSavePressed(self):
        if not self.btnView.isEnabled():
            deleteAlarm(self.alarmToDelete)

        self.btnStopPressed()

        week = ""

        today = dt.date.today()

        alarm_dict = {"ALARM_NAME": "",
                      "TIME": "",
                      "CREATE_DATE": "",
                      "LAST_MODIFIED_DATE": f"{today.day}/{today.month}/{today.year}",

                      "USER_ALARM_TIME": "",
                      "USER_SPECIAL_DATES": "",
                      "USER_SPECIAL_DAYS": "",
                      "USER_SPECIAL_MONTHS": "",
                      "USER_SPECIAL_YEARS": "",

                      "WEEKDAYS": "",
                      "SPECIAL_DAYS": "",
                      "RINGTONE": ""}

        alarm_name = self.leAlarmName.text()
        if not alarm_name:
            QMessageBox.critical(self, "No Alarm Name", "A name for your alarm is required!")
        else:
            alarm_dict["ALARM_NAME"] = alarm_name

            time = self.leTime.text()

            if not checkTime(time):
                QMessageBox.critical(self, "Invalid Time", "Enter valid time!")
            else:
                alarm_dict["TIME"] = alarm_dict["USER_ALARM_TIME"] = time
                all_specific_dates = set()

                special_days = self.teSpecialDates.toPlainText()
                if special_days:
                    alarm_dict["USER_SPECIAL_DATES"] = special_days

                    special_days = set(checkSpecialDates(special_days))
                    if not special_days:
                        QMessageBox.critical(self, "Invalid Date", "Enter valid special date!")
                    else:
                        all_specific_dates |= special_days

                if self.leSpecialDays.text() or self.leSpecialMonths.text() or self.leSpecialYears.text():
                    D = self.leSpecialDays.text()
                    if not D:
                        QMessageBox.critical(self, "No Day", "Enter special day!")
                    else:
                        M = self.leSpecialMonths.text()
                        if not M:
                            QMessageBox.critical(self, "No Month", "Enter special month!")
                        else:
                            Y = self.leSpecialYears.text()
                            if not Y:
                                QMessageBox.critical(self, "No Year", "Enter special year!")
                            else:

                                alarm_dict["USER_SPECIAL_DAYS"] = str(D)
                                alarm_dict["USER_SPECIAL_MONTHS"] = str(M)
                                alarm_dict["USER_SPECIAL_YEARS"] = str(Y)

                                special_dayMonthYear = set(specialDMY(D, M, Y))
                                if not special_dayMonthYear:
                                    QMessageBox.critical(self, "Invalid Input",
                                                         "Enter valid special day/month/year!")
                                else:
                                    all_specific_dates |= special_dayMonthYear.copy()
                                    all_specific_dates = list(all_specific_dates)
                                    all_specific_dates.sort(key=lambda x: dt.date(year=int(x.split("/")[2]),
                                                                                  month=int(x.split("/")[1]),
                                                                                  day=int(x.split("/")[0])))

                alarm_dict["SPECIAL_DAYS"] = ", ".join(all_specific_dates)

                if self.chkMonday.isChecked():
                    week += "Monday, "
                if self.chkTuesday.isChecked():
                    week += "Tuesday, "
                if self.chkWednesday.isChecked():
                    week += "Wednesday, "
                if self.chkThursday.isChecked():
                    week += "Thursday, "
                if self.chkFriday.isChecked():
                    week += "Friday, "
                if self.chkSaturday.isChecked():
                    week += "Saturday, "
                if self.chkSunday.isChecked():
                    week += "Sunday, "
                week = week.rstrip(", ")
                alarm_dict["WEEKDAYS"] = week

                if alarm_dict["WEEKDAYS"] or alarm_dict["SPECIAL_DAYS"]:

                    if not os.path.exists(self.ringtone):
                        self.ringtone = self.default_ringtone
                        self.ringtoneName = "Basic.mp3"
                        self.lblRingtoneName.setText(self.ringtoneName)

                    alarm_dict["RINGTONE"] = self.ringtone

                    if not self.btnView.isEnabled():
                        if createAlarm(alarm_dict):

                            self.parent.lwAlarmList.clear()
                            self.parent.alarmNameDict = alarmList()
                            for string in sorted(list(self.parent.alarmNameDict.keys())):
                                self.parent.lwAlarmList.addItem(string)

                            QMessageBox.information(self, "Success!", "Alarm Edited!")
                            self.clearAll()
                        else:
                            QMessageBox.critical(self, "Alarm Can't be edited!", "Sorry! There is a problem!")
                    else:
                        if createAlarm(alarm_dict):
                            QMessageBox.information(self, "Success!", "Alarm Saved!")
                            self.clearAll()
                        else:
                            QMessageBox.critical(self, "Alarm Can't be saved!", "Sorry! There is a problem!")

                else:
                    QMessageBox.critical(self, "Alarm Can't be saved!", "No date specified!")

    def btnViewPressed(self):
        self.btnStopPressed()

        self.viewWindow = ViewApp()
        self.viewWindow.show()

    def clearAll(self):
        self.leAlarmName.setText("")
        self.leTime.setText("")
        self.teSpecialDates.setText("")
        self.leSpecialDays.setText("")
        self.leSpecialMonths.setText("")
        self.leSpecialYears.setText("")

        self.ringtone = ".\\Basic.mp3"
        self.default_ringtone = ".\\Basic.mp3"
        self.ringtoneName = "Basic.mp3"
        self.lblRingtoneName.setText(self.ringtoneName)

        self.url = QUrl.fromLocalFile(self.ringtone)
        self.content = QMediaContent(self.url)
        self.player = QMediaPlayer()
        self.player.setMedia(self.content)

        self.btnUncheckAllPressed()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainApp()
    window.show()
    sys.exit(app.exec_())
