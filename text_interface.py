import pandas as pd
import functions as f
import os
import time


def importFileInterface():
    language = input('Select language for column data\n1 - Polish\n2 - English\n')
    file_type = input('1 - import .csv file \n2 - import .shp file (only if you are having geopandas library)\n')
    if file_type == '1':
        dan = import_csvfile()
    # nie działa błąd driver error
    elif file_type == '2':
        dan, geo = import_shpfile()
    else:
        input('wrong value')
        exit()
    os.system('cls')

    return dan, language


def import_csvfile():
    plik = input('choose filename (G_SUBAREA.csv if no value is entered): ')
    try:
        dan = pd.read_csv(plik)
    except FileNotFoundError:
        dan = pd.read_csv('pandas-lp/G_SUBAREA.csv')
    except:
        input('file not found')
        exit()
    return dan


def import_shpfile():
    import geopandas as gpd
    plik = input('select filename or skip to read G_SUBAREA.shp: ')
    try:
        dan = gpd.read_file(plik)
    except:
        try:
            dan = gpd.read_file('pandas-lp/G_SUBAREA.shp')
        except:
            input('brak pliku')
            exit()
    finally:
        geo = dan['geometry']
        del dan['geometry']
    return dan, geo


def choose_column_names_ui(dan, language):
    kkol = f.choose_columns_names(language, dan)
    dane = dan.dropna(subset=kkol[7])
    return dane, kkol


def main_interface(data,columns):
    while True:
        os.system('cls')
        print('------------------------------\n1 - forest district data\n'
              '2 - forest division data\n3 - edit data\n9 - exit')
        choose = input('Select number and click enter: ')
        if choose == '1':
            os.system('cls')
            time.sleep(1)
            print('------------------------------')
            print('1 - site type info\n2 - information about age\n'
                  '3 - information about species\n4 - information about activities\n'
                  '5 - info about tree cover\n\n8 - back\n9 - exit\n')
            choose = input('Select number and click enter:\n')
            if choose == '1':
                f.site_type(data, columns)
            elif choose == '2':
                print('dane dot wieku')
                f.forest_age(data, columns)
            elif choose == '3':
                print('not finished yet')
                continue
            elif choose == '8':
                break
            elif choose == '9':
                exit()
            else:
                print('\nwrong value')
        elif choose == '2':
            f.select_division(data)

        elif choose == '3':
            data = f.edit_division(data)

        elif choose == '9':
            exit()
