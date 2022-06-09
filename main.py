import sys, os # Импорт модулей sys, os и ctypes для запроса прав администратора

from PyQt5 import QtCore, uic # ИМПОРТ PyQt (uic для .xml файлов)
from PyQt5.QtGui import QIcon # Импорт QIcon для отображения иконки (логотипа) программы в углу окна
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QLineEdit, QLabel # ИМПОРТ виджетов из PyQt

import pyowm  # ИМПОРТ модуля pyowm
from pyowm import OWM
from pyowm.utils import config
from pyowm.utils import timestamps
from pyowm.utils.config import get_default_config


config_dict = get_default_config()
config_dict['language'] = 'ru'  # переменная для локализации программы на русский язык [ru]

owm = OWM('78d543125ec3f689ae035d24fc4b700b', config_dict) 
mgr = owm.weather_manager() # Подключение токена (API ключа) и локализация


class MyWidget(QMainWindow): # Главное графическое окно
    def __init__(self):
        super().__init__()
        uic.loadUi('data\\ui.ui', self) # Подключение графического интерфейса через uic (.ui файл)
        self.setFixedSize(590, 600) # Фиксация масштаба главного окна (запрет масштабирования)
        self.setWindowIcon(QIcon('data\\icon.ico')) # Иконка приложения

        self.line.setReadOnly(True) # Запрет изменения содержимого поля ввода для отображения статуса погоды   
        self.temper_line.setReadOnly(True) # Запрет изменения содержимого поля ввода для отображения температуры
        self.speed_line.setReadOnly(True) # Запрет изменения содержимого поля ввода для отображения скорости ветра
        self.vlazhnost_line.setReadOnly(True) # Запрет изменения содержимого поля ввода для отображения влажности

        self.pushButton_2.clicked.connect(self.save_city) # Подключение кнопки "В избранное" к функции save_city
        self.pushButton.clicked.connect(self.observation_weather) # Подключение кнопки "Посмотреть" к функции observation_weather
        self.helpBut.clicked.connect(self.open_information) # Подключение кнопки "Справка" к функции open_information

        if (os.stat("maincity.txt").st_size == 0) == True:  # Проверка файла maincity.txt на наличие содержимого
            f = open('maincity.txt', 'w', encoding='utf-8') # В случае если файл пустой, туда забивается "Москва"
            f.write('Москва')
            f.close()

        file = open('maincity.txt','r', encoding='utf-8')
        self.lineEdit.setText(*file) # ввод региона по умолчанию в поле ввода
        file.close()

        self.observation_weather() # Выполнение функции observation_weather
    
    
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Enter:
            try:
                if self.lineEdit.text() == '':  # проверка на наличие содержимого в поле ввода
                    self.line.setText('Введите в поле выше регион информация о котором вам нужна')
                    self.temper_line.setText('°C')
                    self.speed_line.setText('м/с')
                    self.vlazhnost_line.setText('%')
                else: # В случае, если содержимое в поле ввода какое-либо имеется
                    try: # Обработчик исключений на случай если регион не будет найден
                        self.place = self.lineEdit.text()
                        observation = mgr.weather_at_place(self.place)
                        w = observation.weather
                        temper = w.temperature('celsius')['temp']
                        speed_wind = w.wind()['speed']
                        status_for_line = w.detailed_status

                        self.line.setText('В регионе - ' + self.place + ' сейчас ' + status_for_line)
                        self.temper_line.setText(str(round(temper, 1)) + '°C')
                        self.speed_line.setText(str(round(speed_wind)) + ' м/с')
                        self.vlazhnost_line.setText(str(w.humidity) + '%')
                    except pyowm.commons.exceptions.NotFoundError:
                        self.line.setText('Данный регион не найден! Повторите попытку...')            
                        self.temper_line.setText('°C')
                        self.speed_line.setText('м/с')
                        self.vlazhnost_line.setText('%')
            except:
                self.line.setText('ОШИБКА | ВОЗМОЖНО НЕ ХВАТАЕТ ПРАВ АДМИНИСТРАТОРА')
                self.temper_line.setText('°C')
                self.speed_line.setText('м/с')
                self.vlazhnost_line.setText('%')

        event.accept()


    def save_city(self):  # функция для сохранения введённого региона в избранное
        try:
            f = open('maincity.txt', 'w', encoding='utf-8')
            f.write(self.lineEdit.text())
            f.close()
        except:
            self.line.setText('ОШИБКА | ВОЗМОЖНО НЕ ХВАТАЕТ ПРАВ АДМИНИСТРАТОРА')
            self.temper_line.setText('°C')
            self.speed_line.setText('м/с')
            self.vlazhnost_line.setText('%')
    
    def observation_weather(self):  # функция получения погодной информации и её вывода на полях
        try:
            if self.lineEdit.text() == '':  # проверка на наличие содержимого в поле ввода
                self.line.setText('Введите в поле выше регион информация о котором вам нужна')
                self.temper_line.setText('°C')
                self.speed_line.setText('м/с')
                self.vlazhnost_line.setText('%')
            else: # В случае, если содержимое в поле ввода какое-либо имеется
                try: # Обработчик исключений на случай если регион не будет найден
                    self.place = self.lineEdit.text()
                    observation = mgr.weather_at_place(self.place)
                    w = observation.weather
                    temper = w.temperature('celsius')['temp']
                    speed_wind = w.wind()['speed']
                    status_for_line = w.detailed_status

                    self.line.setText('В регионе - ' + self.place + ' сейчас ' + status_for_line)
                    self.temper_line.setText(str(round(temper, 1)) + '°C')
                    self.speed_line.setText(str(round(speed_wind)) + ' м/с')
                    self.vlazhnost_line.setText(str(w.humidity) + '%')
                except pyowm.commons.exceptions.NotFoundError:
                    self.line.setText('Данный регион не найден! Повторите попытку...')            
                    self.temper_line.setText('°C')
                    self.speed_line.setText('м/с')
                    self.vlazhnost_line.setText('%')
        except:
            self.line.setText('ОШИБКА | ВОЗМОЖНО НЕ ХВАТАЕТ ПРАВ АДМИНИСТРАТОРА')
            self.temper_line.setText('°C')
            self.speed_line.setText('м/с')
            self.vlazhnost_line.setText('%')

    
    def open_information(self): # Функция открытия окна справки
        self.info_form = InfodForm(self, "Данные для второй формы")
        self.info_form.show()


class InfodForm(QMainWindow): # Окно "СПРАВКА"
    def __init__(self, *args):
        super().__init__()
        uic.loadUi('data\\information.ui', self) # Подключение графического интерфейса через uic (.ui файл)
        self.setFixedSize(474, 391) # Фиксация масштаба окна справки (запрет масштабирования)
        self.text_info.setReadOnly(True) # Запрет изменения содержимого поля для отображения информации


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyWidget()
    ex.show()
    sys.exit(app.exec_())
