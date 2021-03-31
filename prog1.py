import parser
import matplotlib.pyplot as plt
import matplotlib.tri as tri
import numpy as np
import math
from math import exp,e
from numpy import log,sin,cos,tan,sqrt
import matplotlib.mlab as ml
from matplotlib import cm

from matplotlib.ticker import LinearLocator, FormatStrFormatter
from mpl_toolkits.mplot3d import Axes3D
#komentarz w prog1
#================= zmienne globalne ===============
MAX_ITER=100
EPS=0.0001
x1=0
x2=0
x3=0
x4=0
x5=0

wzor = ''
N = 0
x_start =[]
x_stop = []
kier = []
dl_przedzialu = 0
dl_kier=0
iter = 0
out=[]
SZEF=[]
ACC=7

def Clear():
    global wzor,N,x_start,x_stop,kier,dl_przedzialu,dl_kier,out,SZEF

    wzor = ''
    N = 0
    x_start =[]
    x_stop = []
    kier = []
    dl_przedzialu = 0
    iter = 0
    dl_kier=0
    out=[]
    SZEF=[]

def Wczytaj_Funkcje(F):
    global wzor,N
    wzor = F
    N=Roz_wzor(wzor)

def Wczytaj_Punk_Poczatkowy(P):
    global N,string,x_start
    string=P.split(',')
    for i in string:
        x_start.append(int(i))

def Podaj_Kierunek(K):
    global kier,dl_kier
    string=K.split(',')
    for i in string:
        kier.append(int(i))

    pom=0
    for i in range(N):
        pom=pom+kier[i]**2
    dl_kier=math.sqrt(pom)

def Dlugosc_Przedzialu(DP):
    global dl_przedzialu,x_stop
    dl_przedzialu = DP

    for i in range(N):
        x_stop.append(x_start[i]+kier[i]*dl_przedzialu)


def Roz_wzor(string):
    data=[]
    for i in range(len(string)):
        if string[i]=='x':
            if string[i+1]!='p':
                data.append(string[i+1])

    odp=[]
    for i in data:
        if i not in odp:
            odp.append(i)

    return len(odp)


def f(kier,x0,alfa):
    global x1,x2,x3,x4,x5,out
    out=dekompost(kier,x0,alfa)

    ustaw_x(out)
    exe=eval(wzor)
    return exe

# funkcja zmieniająca problem n wymiarowy w jeden wymiar
def dekompost(kier,x0,alfa):
    odp=[]
    for i in range(len(kier)):
        odp.append(x0[i]+kier[i]*alfa)
    return odp

# ustawia do zmiennych globalnych wartosci x z dostępnego wektora
def ustaw_x(x):
    global x1,x2,x3,x4,x5,x6
    try:
        x1=x[0]
        x2=x[1]
        x3=x[2]
        x4=x[3]
        x5=x[4]
        x6=x[5]
    except IndexError:
        pass

# Algorytm złotego podziału
def golden_method(a,b):
    global kier,x_start,SZEF

    x0=x_start
    k=(math.sqrt(5)-1)/2

    alfa_L=b-k*(b-a)
    alfa_R=a+k*(b-a)
    iter=0
    while((alfa_R-alfa_L)>EPS and MAX_ITER>=iter):
        iter+=1
        if f(kier,x0,alfa_L) < f(kier,x0,alfa_R):
            f(kier,x0,alfa_L)
            SZEF.append(out)
            b=alfa_R
            alfa_R=alfa_L
            alfa_L=b-k*(b-a)
        else:
            f(kier,x0,alfa_R)
            SZEF.append(out)
            a=alfa_L
            alfa_L=alfa_R
            alfa_R=a+k*(b-a)

    return (a+b)/2 , iter



def zwroc_wynik():
    global iter
    wynik,iter=golden_method(0,dl_przedzialu)
    odp=[]
    for i in range(N):
        odp.append(round(x_start[i]+kier[i]*wynik,ACC))

    pom=''
    string = ''
    wek = []
    for i in range(iter):
        #wek=[SZEF[i][0],SZEF[i][1]]
        wek = (SZEF[i])
        ustaw_x(wek)
        #pom=pom+'('+str(i+1)+') '+"f("+str(round(SZEF[i][0],ACC))+", "+str(round(SZEF[i][1],ACC))+')= '+str(round(eval(wzor),ACC))+'\n'
        pom = pom+'('+str(i+1)+') '+"f("+str(np.around(SZEF[i],decimals=ACC))+")= "+str(round(eval(wzor),ACC))+'\n'
    ustaw_x(odp)
    pom=pom+"\n#### rozwiązanie optymalne #####\n"
    #string = "x1*= " + str(round(odp[0],ACC)) + " x2*= "+str(round(odp[1],ACC))+"\n" + "f(x1*,x2*)= "+str(round(eval(wzor),12))
    for i in range(N):
        string = string + "x"+str(i+1)+"*= "+str(round(odp[i],ACC))+"\n"
    string = string + "f("
    for i in range(N):
        string = string + "x"+str(i+1)+"*, "
    string = string[:-2]
    string = string + ")= "+str(round(eval(wzor),12))
    return pom + string

#######################################################################################################
def wykres():
    vector = np.vectorize(np.float)
    npts = 50000
    ngridx = 200
    ngridy = 200
    wsp_zakresu =  dl_kier if(dl_przedzialu <= dl_kier)  else dl_przedzialu

    dl_wek=sqrt((x_start[0]-x_stop[0])**2+(x_start[1]-x_stop[1])**2)

    # WZ [N,S,W,E]
    WZ=[0]*4
    if kier[0]>=0 and kier[1]>=0:
        WZ[0]=dl_wek
        WZ[3]=dl_wek
    elif kier[0]>=0 and kier[1]<=0:
        WZ[3]=dl_wek
        WZ[1]=dl_wek
    elif kier[0]<=0 and kier[1]<=0:
        WZ[1]=dl_wek
        WZ[2]=dl_wek
    elif kier[0]<=0 and kier[1] >= 0:
        WZ[0]=dl_wek
        WZ[2]=dl_wek



    x1_pom = np.random.uniform(-WZ[2]-abs(x_start[0]-1),WZ[3]+abs(x_start[0]+1) , npts)
    x2_pom = np.random.uniform(-WZ[1]-abs(x_start[1]-1),WZ[0]+abs(x_start[1]+1), npts)
    #x1_pom=np.random.uniform(-wsp_zakresu-abs(x_start[0]-1),wsp_zakresu+abs(x_start[0]+1),npts)
    #x2_pom=np.random.uniform(-wsp_zakresu-abs(x_start[1]-1),wsp_zakresu+abs(x_start[1]+1),npts)
    z=[]
    for i in range(len(x1_pom)):
        x1=x1_pom[i]
        x2=x2_pom[i]
        z.append(eval(wzor))
    x1 = x1_pom
    x2 = x2_pom


    fig,ax1=plt.subplots(1,1)

    # Create grid values first.
    xi = np.linspace(-WZ[2]-abs(x_start[0]-1),WZ[3]+abs(x_start[0]+1), ngridx)
    yi = np.linspace(-WZ[1]-abs(x_start[1]-1),WZ[0]+abs(x_start[1]+1), ngridy)

    # Linearly interpolate the data (x, y) on a grid defined by (xi, yi).

    triang = tri.Triangulation(x1, x2)
    interpolator = tri.LinearTriInterpolator(triang, z)
    Xi, Yi = np.meshgrid(xi, yi)
    zi = interpolator(Xi, Yi)

    # Note that scipy.interpolate provides means to interpolate data on a grid
    # as well. The following would be an alternative to the four lines above:
    #from scipy.interpolate import griddata
    #zi = griddata((x, y), z, (xi[None, :], yi[:, None]), method='linear')

    ax1.contour(xi, yi, zi, levels=14, linewidths=0.5, colors='k')
    cntr1 = ax1.contourf(xi, yi, zi, levels=14, cmap="RdBu_r")


    # punkt do prostej kierunkowej
    x_start_values=[x_start[0],x_stop[0]]
    x_stop_values=[x_start[1],x_stop[1]]

    # kolejne punkty iteracyjne
    xii=[]
    yii=[]
    for i in range(iter):
        xii.append(SZEF[i][0])
        yii.append(SZEF[i][1])

    # punkty X,Y minimalne
    x_min=xii[-1]
    y_min=yii[-1]

    ax1.plot(x_start_values,x_stop_values,'lime') #linia kierunku
    ax1.plot(x_start[0],x_start[1],'kx',markersize=12,label='punkt startowy') # punkt startowy
    ax1.plot(xii,yii,'kx') # punkty iteracyjne
    ax1.plot(x_min,y_min,color='lime', marker='.',markersize=12,label='punkt końcowy') #punkt minimalny
    #ax1.scatter(x_min,y_min,s=1000,color='lime',label='punkt końcowy')
    ax1.legend()

    fig.colorbar(cntr1, ax=ax1)

    #ax1.set(xlim=(dl_kier*(x_start[0]-dl_przedzialu-1), dl_kier*(x_start[0]+dl_przedzialu+1)), ylim=(dl_kier*(x_start[1]-dl_przedzialu-1), dl_kier*(x_start[1]+dl_przedzialu+1))) #to ustawia szerokosc plota
    ax1.set(xlim=(-WZ[2]-abs(x_start[0]-1),WZ[3]+abs(x_start[0]+1)), ylim=(-WZ[1]-abs(x_start[1]-1),WZ[0]+abs(x_start[1]+1))) #to ustawia szerokosc plota

    plt.subplots_adjust(hspace=0.5)
    plt.show()
