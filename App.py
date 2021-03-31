from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from PyQt5.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QSpinBox
import os
import prog1 as P


def info():
    instr='Instrukcja wprowadzania danych:\n'
    instr=instr+'Wzór - zmienne należy wpisać jako: x1,x2,...x5\n'
    instr=instr+'operator potęgowania - ** \n'
    instr=instr+'funkcja pierwiastkowania kwadratowego - sqrt()\n'
    instr=instr+'funkcja logarytmu - log(liczba,baza)\n'
    instr=instr+'funkcje trygonometryczne - sin(),cos(),tan()\n'
    instr=instr+'********************\n'
    instr=instr+'Akceptowalny format danych:\n'
    instr=instr+'punk startowy: x1,x2\n'
    instr=instr+'kierunek: a1,a2\n'
    instr=instr+'długość przedziału: liczba całkowita dodatnia\n'
    return instr

class Window(QWidget):
#Komentasz nowy
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Metoda złotego podziału')
        width = 1000
        height = 200


        self.setMinimumSize(width, height)

        #Tworzenie obiektów
        self.Wzor = QLineEdit()
        self.Punkt_Startowy = QLineEdit()
        self.Kierunek = QLineEdit()
        self.Dlugosc_Przedzialu = QLineEdit()
        self.Epsilon = QLineEdit()
        self.Ilosc_Iteracji = QLineEdit()

        self.Oblicz = QPushButton("Oblicz")
        self.Wykres = QPushButton("Wykres")
        self.HELP = QPushButton("Pomoc")

        self.Funkcja_1 = QPushButton("(x1-2)**2 + (x2-2)**2")
        self.Funkcja_2 = QPushButton("exp(x1-x2)*x2-2*x1")
        self.Funkcja_3 = QPushButton("sin(x1*x2)-cos(x1)")
        self.Funkcja_4 = QPushButton("log(x2*x1)")
        self.Wyjscie = QTextEdit()

        self.create_Dane_Wejsciowe()
        self.create_Kryteria_Stopu()
        self.create_Przykladowe_Funkcje()
        self.create_Pole_terminalu()

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.Dane_Wejsciowe, 1, 0)
        mainLayout.addWidget(self.Kryteria_Stopu, 1, 1)
        mainLayout.addWidget(self.Przykladowe_Funkcje, 2, 0, 2, 2)
        mainLayout.addWidget(self.Pole_terminalu,1,3,4,1)
        mainLayout.addWidget(self.Oblicz,5,3)
        mainLayout.addWidget(self.Wykres,6,3)
        mainLayout.addWidget(self.HELP,6,0)
        self.setLayout(mainLayout)

        #Guzik klika
        self.Oblicz.clicked.connect(self.Submit)
        self.Wykres.clicked.connect(self.Wypisz_Wymaluj)
        self.Funkcja_1.clicked.connect(self.Przypisz1)
        self.Funkcja_2.clicked.connect(self.Przypisz2)
        self.Funkcja_3.clicked.connect(self.Przypisz3)
        self.Funkcja_4.clicked.connect(self.Przypisz4)
        self.HELP.clicked.connect(self.Przypisz5)


        self.Epsilon.setText("0.0001")
        self.Ilosc_Iteracji.setText("100")

        self.Punkt_Startowy.setText('0,0')
        self.Kierunek.setText('1,1')
        self.Dlugosc_Przedzialu.setText('10')
        self.Wyjscie.setText(info())

    #Jakieśtam funckje pomocnicze
    def Wypisz_Wymaluj(self):
        if P.N!=2:
            self.Wyjscie.setText('Wymiar uniemożliwia wizualizację (wymiar musi być równy 2)')
            return
        else:
            P.wykres()

    def Submit(self):
        P.Clear()
        P.Wczytaj_Funkcje(self.Wzor.text())
        P.Wczytaj_Punk_Poczatkowy(self.Punkt_Startowy.text())
        P.Podaj_Kierunek(self.Kierunek.text())

        if (len(P.x_start)!=len(P.kier))or(len(P.x_start)!=P.N)or(len(P.kier)!=P.N):
            self.Wyjscie.setText('Niezgodność wymiarów (wzór, punkt startowy, wektor kierunkowy)!')
            return

        P.Dlugosc_Przedzialu(int(self.Dlugosc_Przedzialu.text()))
        P.EPS = float(self.Epsilon.text())
        P.MAX_ITER = int(self.Ilosc_Iteracji.text())

        self.Wyjscie.setText(P.zwroc_wynik())


    def create_Dane_Wejsciowe(self):
        self.Dane_Wejsciowe = QGroupBox("Dane Wejściowe")

        layout = QFormLayout()

        layout.addRow("Wzor funkcji", self.Wzor)
        layout.addRow("Punkt startowy", self.Punkt_Startowy)
        layout.addRow("Kierunek", self.Kierunek)
        layout.addRow("Dlugość przedziału", self.Dlugosc_Przedzialu)

        self.Dane_Wejsciowe.setLayout(layout)

    def create_Kryteria_Stopu(self):
        self.Kryteria_Stopu = QGroupBox("Kryteria Stopu")

        layout = QFormLayout()

        layout.addRow("Epsilon", self.Epsilon)
        layout.addRow("Ilość iteracji", self.Ilosc_Iteracji)

        self.Kryteria_Stopu.setLayout(layout)

    def create_Przykladowe_Funkcje(self):
        self.Przykladowe_Funkcje = QGroupBox("Przykładowe funkcje")
        layout = QFormLayout()

        layout.addWidget(self.Funkcja_1)
        layout.addWidget(self.Funkcja_2)
        layout.addWidget(self.Funkcja_3)
        layout.addWidget(self.Funkcja_4)

        self.Przykladowe_Funkcje.setLayout(layout)

    def create_Pole_terminalu(self):
        self.Pole_terminalu = QGroupBox("Wyjście")
        layout = QFormLayout()

        layout.addWidget(self.Wyjscie)

        self.Pole_terminalu.setLayout(layout)

    def Przypisz1(self):
        self.Wzor.setText("(x1-2)**2 + (x2-2)**2")

    def Przypisz2(self):
        self.Wzor.setText("exp(x1-x2)*x2-2*x1")

    def Przypisz3(self):
        self.Wzor.setText("sin(x1*x2)-cos(x1)")

    def Przypisz4(self):
        self.Wzor.setText("log(x2*x1)")

    def Przypisz5(self):
        self.Wyjscie.setText(info())


app = QApplication([])
w = Window()
w.show()
app.exec()
