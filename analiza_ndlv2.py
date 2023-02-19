print('Progsfdram analizuje i prezentuje podstawowe informacje zawarte w arkuszu pozyskanym ze strony BDL.\nDo uruchomienia niezbędne są zainstalowane biblioteki: Pandas, Geopandas, Numpy, Sklearn.')
input('Jesli biblioteki nie są zainstalowane nastąpi automatyczne zamknięcie programu.\nKliknij enter aby kontynuować.')
#import pandas as pd
# print('jest pd')
from sklearn.linear_model import LinearRegression
# print('sklearn jest')
import sys
# print('sys jest')
import numpy as np
# print('numpy jest')
# from shapely.geometry import Polygon, LineString, Point
# print('shapely jest')
import os
import time
# print('os jest')

# pozyskiwanie pliku
print('python ver p: 3.9.13 -> o: ',sys.version,' ')
# dane = pd.read_csv('f_area_type_dic.txt', delimiter=' ')
decyzja = '0'

#ZAPYTANIE O RODZAJ PLIKU#
decyzja=input('Wczytując .csv wybierz 1\nWczytując shapefile wybierz 2: ')
if decyzja=='1':
    plik=input('podaj nazwę pliku lub pomiń by wczytać G_SUBAREA.csv: ')
    try:
        dan=pd.read_csv(plik)
    except FileNotFoundError:
        dan=pd.read_csv('G_SUBAREA.csv')
    except:
        input('brak pliku')
        exit()
#nie działa błąd driver error
elif decyzja=='2':
    import geopandas as gpd
    plik=input('podaj nazwę pliku lub pomiń by wczytać G_SUBAREA.shp: ')
    try:
        dan = gpd.read_file(plik)
    except:
        try:
            dan = gpd.read_file('G_SUBAREA.shp')
        except:
            input('brak pliku')
            exit()
    finally:
        geo=dan['geometry']
        del dan['geometry']
else:
    input('błędna wartość. kliknij enter aby wyjść')
    exit()        
#PRZEMIANOWANIE KOLUMN#
def zmianakol(yn):
    if yn == 'n':
        print('pozostawiono oryginalne nazwy kolumn')
    
    else:
        kolumny=dan.columns
        nkol = {'a_i_num':'ID','adr_for':'Adres Leśny','site_type':'Siedlisko','stand_stru':'Budowa','rotat_age':'Wiek Rębności',
            'sub_area':'Powierzchnia','prot_categ':'Kat. Ochronna','species_cd':'Gatunek','spec_age':'Wiek','a_year':'Rok',
            'area_type':'Typ Powierzchni','silvicult':'Sposób Zagospodarowania','part_cd':'Zadrzewienie','forest_fun':'Funkcja drzewostanu'}
        dan.rename(columns=nkol, inplace=True)
        print('zmieniono nazwy kolumn')
    kkol = dan.columns
    time.sleep(1)
    os.system('cls')
    time.sleep(1)
    return kkol
#do dodania. opcja dla warstwy .shp podziału dla siedlisk
def siedlisko():
    #siedlisko
    scou= dane[kkol[4]].value_counts().to_frame()
    typys = dane[kkol[4]].unique()
    dane.set_index(kkol[4],inplace=True)
    scou.columns={'Ilość':kkol[4]}
    for x in typys:
        scou.loc[x,'pow [a]']=round(dane.loc[x,kkol[9]].sum(),2)
        scou.loc[x,'pow [%]']=round(dane.loc[x,kkol[9]].sum()/powierzchnia*100,2)
    dane.reset_index(inplace=True)
    print('ilość wydzieleń:',sum,'całkowita powierzchnia:',powierzchnia,'\n',
          scou)
    decyzja = input('czy zapisać dane w pliku .csv? [y/n]')# dodac funkcjonalnosc .shp
    if decyzja == 'y':
        scou.to_csv('siedliska.csv')
        print('dane zostały zapisane w pliku siedliska.csv')
    time.sleep(1)
    os.system('cls')
    time.sleep(1)
        
def wiek():
    print('----------------------------------------\nsredni wiek:',round(dane[kkol[13]].mean(),2),'lat.')
    print('Maksymalny wiek:',round(dan[kkol[13]].max(),2),'lat')
    gos = dane[kkol[6]] == 'GOSP'
    goss= dane.where(gos).dropna(subset=kkol[2])
    print('Maksymalny wiek (lasy gosp):',round(goss[kkol[13]].max(),2),'lat')
    print('5 wydzieleń z najstarszymi drzewami:\n',goss.nlargest(n=5,columns=kkol[13]).loc[:,[kkol[2],kkol[13]]])
    kw = np.arange(0,100,20)
    for x in kw :
        a=dane[kkol[13]].between(x,x+20)
        print(int((x+20)/20),' klasa wieku',dane[kkol[9]].where(a).count(), 'wydzieleń\t',round(dane[kkol[9]].where(a).sum(),2),'a\t', round(dane[kkol[9]].where(a).dropna().sum()/powierzchnia*100,2),'% obszaru lasów')
    a=dane[kkol[13]].between(100,120)
    print('6+ klasa wieku',dane[kkol[9]].where(a).count(), 'wydzieleń\t',round(dane[kkol[9]].where(a).sum()), 'a\t',round(dane[kkol[9]].where(a).sum()/powierzchnia*100),'% obszaru lasów')
    #decyzja= input('czy zapisać dane jako warstwa wektorowa .shp? [y/n]')
    #if decyzja == 'y':
        #cdn
    time.sleep(1)
    os.system('cls')
    time.sleep(1)

def udzial():
    #udzial poszczegolnych gatunkow 
    print('----------------------------------------')
    print('10 gatunkow najczesciej opisanych jako dominujace oraz ilosc wydzielen\n',dane[kkol[11]].value_counts().head(10))
    dane.set_index(kkol[11],inplace=True)
    typys = dane.index.unique().dropna()
    print('powierzchnia oraz % udzial wydzielen wg dominującego gatunku (wyłącznie pow. 0,5%')            
    for x in typys:
        if round(dane.loc[x,kkol[9]].sum()/powierzchnia*100,2) > 0.5:
            print(x,round(dane.loc[x,kkol[9]].sum(),2),'a\t',round(dane.loc[x,kkol[9]].sum()/powierzchnia*100,2),'%')
    decyzja = input('cze chcesz zapisać w pliku csv dane? [y/n]')
    dane.reset_index(inplace=True)
    if decyzja == 'y':
        udz = pd.DataFrame(dane[kkol[11]].value_counts())
        dane.set_index(kkol[11],inplace=True)
        for x in typys:
            udz['powierzchnia'].append(round(dane.loc[x,kkol[9]].sum(),2))
            udz['udzial procentowy'].append(round(dane.loc[x,kkol[9]].sum()/powierzchnia*100,2))
                


decyzja=input('Czy zmienić nazwy kolumn na polskie? [y/n] domyślnie "y":')
kkol = zmianakol(decyzja)
dane=dan.dropna(subset=kkol[7])


###podstawowe informacje###
#dan - podstawowy plik bez geometrii
#geometry - geometria
#dane - pkik bez NaN (z zalozenia tylko lesne)
#dane2 - usuniete

#dane.info()

sum=len(dane)
clear = lambda: os.system('cls')
powierzchnia=round(dane[kkol[9]].sum(),2)
#pow_calk=round(dan['Powierzchnia'].sum(),2)
#spow=round(dane['Powierzchnia'].sum(),2)

while decyzja != '9':
    print('------------------------------\n1- dane dot. całego nadlenictwa\n2- dane dot. wybranych wydzieleń\n3- edycja danych\n9- wyjscie')
    decyzja = input('Wybierz numer i nacisnij enter: ')
    if decyzja == '1':
        print('------------------------------')
        print('1- informacje o typach siedliska\n2- informacje o wieku\n3- informacje o poszczególnych gatunkach\n4- inofmracje o rodzaju powierzchni i pracach\n5- informacje o zadrzewieniu\n\n8- powrót\n9- wyjscie')
        decyzja = input('Wybierz numer i nacisnij enter: ')
        if decyzja == '1':
            siedlisko()
        elif decyzja == '2':
            wiek()
        elif decyzja =='3':
            udzial()
        elif decyzja =='8':
            continue
        
        else:
            print('\nNiewlasciwa wartosc')

 

#bonusy
# - po ukończeniu funkcji z drukiem odczekać sekundę i skasowac wszystko
# - zapis do .shp

# =============================================================================
# 
# 
# pd.DataFrame.to_csv(dane,'G_SUBAREA.csv')
# 
#     
# dane2['sub_area'].count
# dane['sub_area'].value_counts()
# dane2.sub_area
# 
# spr = ssum/sum*100
# print(spr,'% wydzieleń posiada informacje o typie siedliska')
# wybor= input('wartosc liczbowa = 1\nwartosc procentowa - 2\n')
# if wybor == '1':
#     print('ilosc poszczególnych siedlisk:\n', scou)
# elif wybor =='2':
#     print('procentowy udzial siedlisk w wydzieleniach:\n',scou/ssum*100)
# else:
#     print('błąd')
# adres = input('podaj nazwę adresu(mozna jedynie fragment): ')
# dane[dane['adr_for'].str.contains(adres)]
# print('sredni wiek gatunkow dominujacych: ', round(dane['spec_age'].mean(),2),'lat')
#udzial = dane['species_cd'].value_counts()
# sgat = dane['species_cd'].count()
# print('udzial procentowy: \n',round(udzial/sgat*100,3))
# 
# dane.iloc[10,13] = np.NaN
# dane.dropna(inplace=True)
# test = dane.iloc[2:5]
# s = gpd.GeoSeries(test['geometry'])
# s.area
# =============================================================================

# dane.reset_index(inplace=True)

# scou= pd.DataFrame(dane['Siedlisko'].value_counts())
# scou.columns={'Liczba wydzielen':'Siedlisko'}
# dane.set_index('Siedlisko',inplace=True)
# typys = dane.index.unique()
# print('----------------------------------------\n',sum,'wydzieleń z okreslonym typem siedliska')#print('ilosc wydzieleń dla każdego typu:\n',scou)
# print('obszar lasów z okreslonym typem:')
#  for x in typys:
#      print(x,round(dane.loc[x,'Powierzchnia'].sum(),2),'     ',round(dane.loc[x,'Powierzchnia'].sum()/powierzchnia*100,2),'%')
#  dane.reset_index(inplace=True)
# for x in typys:
#     scou.loc[x,'pow [a]']=round(dane.loc[x,'Powierzchnia'].sum(),2)
#     scou.loc[x,'pow [%]']=round(dane.loc[x,'Powierzchnia'].sum()/powierzchnia*100,2)
# scou['pow']=0
# scou.loc[x,'pow']=round(dane.loc[x,'Powierzchnia'].sum(),2)

