from PyQt5.QtCore import QDateTime, Qt, QTimer
from PyQt5.QtWidgets import (QApplication, QCheckBox, QComboBox, QDateTimeEdit,
        QDial, QDialog, QGridLayout, QGroupBox, QHBoxLayout, QLabel, QLineEdit,
        QProgressBar, QPushButton, QRadioButton, QScrollBar, QSizePolicy,
        QSlider, QSpinBox, QStyleFactory, QTableWidget, QTabWidget, QTextEdit,
        QVBoxLayout, QWidget)
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from PyQt5.QtWidgets import QPushButton, QLineEdit, QApplication, QFormLayout, QWidget, QTextEdit, QSpinBox
import os
from math import exp,e
from numpy import log,sin,cos,tan,sqrt,log10
import matplotlib.mlab as ml
from matplotlib import cm
import matplotlib.tri as tri
import prog1 as P
import matplotlib.pyplot as plt
from math import sqrt
import numpy as np


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
    instr=instr+'P.kierunek: a1,a2\n'
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
        self.kierunek = QLineEdit()
        self.Dlugosc_Przedzialu = QLineEdit()
        self.Epsilon = QLineEdit()
        self.Ilosc_Iteracji = QLineEdit()
        self.figure=plt.figure()
        self.canvas=FigureCanvas(self.figure)
        self.toolbar=NavigationToolbar(self.canvas,self)


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
        mainLayout.addWidget(self.Pole_terminalu,4,0,2,2)
        mainLayout.addWidget(self.Oblicz,6,0)
        #mainLayout.addWidget(self.Wykres,6,1)
        mainLayout.addWidget(self.HELP,6,1)

        mainLayout.addWidget(self.canvas,1,4,4,1)
        mainLayout.addWidget(self.toolbar,5,4)

        self.setLayout(mainLayout)



        #Guzik klika
        self.Oblicz.clicked.connect(self.Submit)
        self.Oblicz.clicked.connect(self.wykres2)
        self.Funkcja_1.clicked.connect(self.Przypisz1)
        self.Funkcja_2.clicked.connect(self.Przypisz2)
        self.Funkcja_3.clicked.connect(self.Przypisz3)
        self.Funkcja_4.clicked.connect(self.Przypisz4)
        self.HELP.clicked.connect(self.Przypisz5)


        self.Epsilon.setText("0.0001")
        self.Ilosc_Iteracji.setText("100")

        self.Punkt_Startowy.setText('0,0')
        self.kierunek.setText('1,1')
        self.Dlugosc_Przedzialu.setText('10')
        self.Wyjscie.setText(info())




    #Jakieśtam funckje pomocnicze

    def Submit(self):
        P.Clear()
        P.Wczytaj_Funkcje(self.Wzor.text())
        P.Wczytaj_Punk_Poczatkowy(self.Punkt_Startowy.text())
        P.Podaj_Kierunek(self.kierunek.text())

        if (len(P.x_start)!=len(P.kier))or(len(P.x_start)!=P.N)or(len(P.kier)!=P.N):
            self.Wyjscie.setText('Niezgodność wymiarów (wzór, punkt startowy, wektor P.kierunkowy)!')
            self.figure.clear()
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
        layout.addRow("kierunek", self.kierunek)
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

    def wykres2(self):
        if P.N!=2 or len(P.x_start)!=2 or len(P.kier)!=2:
            if (len(P.x_start)!=len(P.kier))or(len(P.x_start)!=P.N)or(len(P.kier)!=P.N):
                self.canvas.draw()
                return


            ax1=self.figure.add_subplot(111)
            text = ax1.text(0.5, 0.5, 'Wizualizacja dostępna tylko\n dla problemów \nn=2',
                ha='center', va='center', size=20)
            self.canvas.draw()
            return
        else:
            vector = np.vectorize(np.float)
            npts = 50000
            ngridx = 200
            ngridy = 200
            wsp_zakresu =  P.dl_kier if(P.dl_przedzialu <= P.dl_kier)  else P.dl_przedzialu

            dl_wek=sqrt((P.x_start[0]-P.x_stop[0])**2+(P.x_start[1]-P.x_stop[1])**2)

            # WZ [N,S,W,E]
            WZ=[0]*4
            if P.kier[0]>=0 and P.kier[1]>=0:
                WZ[0]=dl_wek
                WZ[3]=dl_wek
            elif P.kier[0]>=0 and P.kier[1]<=0:
                WZ[3]=dl_wek
                WZ[1]=dl_wek
            elif P.kier[0]<=0 and P.kier[1]<=0:
                WZ[1]=dl_wek
                WZ[2]=dl_wek
            elif P.kier[0]<=0 and P.kier[1] >= 0:
                WZ[0]=dl_wek
                WZ[2]=dl_wek


            stala=20
            #x1_pom = np.random.uniform(-stala-abs(P.x_start[0]-1),stala+abs(P.x_start[0]+1) , npts)
            #x2_pom = np.random.uniform(-stala-abs(P.x_start[1]-1),stala+abs(P.x_start[1]+1), npts)

            x1_pom = np.random.uniform(-WZ[2]-abs(P.x_start[0]-1),WZ[3]+abs(P.x_start[0]+1),npts)
            x2_pom = np.random.uniform(-WZ[1]-abs(P.x_start[1]-1),WZ[0]+abs(P.x_start[1]+1), npts)

            z=[]
            for i in range(len(x1_pom)):
                x1=x1_pom[i]
                x2=x2_pom[i]
                z.append(eval(P.wzor))
            x1 = x1_pom
            x2 = x2_pom


            #fig,ax1=plt.subplots(1,1)
            ax1=self.figure.add_subplot(111)

            # Create grid values first.
            xi = np.linspace(-WZ[2]-abs(P.x_start[0]-1),WZ[3]+abs(P.x_start[0]+1), ngridx)
            yi = np.linspace(-WZ[1]-abs(P.x_start[1]-1),WZ[0]+abs(P.x_start[1]+1), ngridy)


            triang = tri.Triangulation(x1, x2)
            interpolator = tri.LinearTriInterpolator(triang, z)
            Xi, Yi = np.meshgrid(xi, yi)
            zi = interpolator(Xi, Yi)


            ax1.contour(xi, yi, zi, levels=100, linewidths=0.5, colors='k')
            cntr1 = ax1.contourf(xi, yi, zi, levels=100, cmap="RdBu_r")


            # punkt do prostej P.kierunkowej
            P.x_start_values=[P.x_start[0],P.x_stop[0]]
            P.x_stop_values=[P.x_start[1],P.x_stop[1]]

            # kolejne punkty iteracyjne
            xii=[]
            yii=[]
            for i in range(P.iter):
                xii.append(P.TAB_OUT[i][0])
                yii.append(P.TAB_OUT[i][1])

            # punkty X,Y minimalne
            x_min=xii[-1]
            y_min=yii[-1]

            ax1.plot(P.x_start_values,P.x_stop_values,'lime') #linia P.kierunku
            ax1.plot(P.x_start[0],P.x_start[1],'kx',markersize=12,label='punkt startowy') # punkt startowy
            ax1.plot(xii,yii,'kx') # punkty iteracyjne
            ax1.plot(x_min,y_min,color='lime', marker='.',markersize=12,label='punkt końcowy') #punkt minimalny

            ax1.legend()
            self.figure.colorbar(cntr1, ax=ax1)
            ax1.set(xlim=(-WZ[2]-abs(P.x_start[0]-1),WZ[3]+abs(P.x_start[0]+1)), ylim=(-WZ[1]-abs(P.x_start[1]-1),WZ[0]+abs(P.x_start[1]+1))) #to ustawia szerokosc plota
            self.canvas.draw()



app = QApplication([])
w = Window()
w.show()
app.exec()
