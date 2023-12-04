import time
import pandas as pd
import numpy as np
import os


def choose_columns_names(choose, dan):
    if choose == '1':
        # kolumny = dan.columns
        polish_column_names = {'a_i_num': 'ID', 'adr_for': 'Adres Leśny', 'site_type': 'Siedlisko',
                               'stand_stru': 'Budowa', 'rotat_age': 'Wiek Rębności',
                               'sub_area': 'Powierzchnia', 'prot_categ': 'Kat. Ochronna', 'species_cd': 'Gatunek',
                               'spec_age': 'Wiek', 'a_year': 'Rok',
                               'area_type': 'Typ Powierzchni', 'silvicult': 'Sposób Zacommercial_forestspodarowania',
                               'part_cd': 'Zadrzewienie', 'forest_fun': 'Funkcja drzewostanu'}
        dan.rename(columns=polish_column_names, inplace=True)
        print('zmieniono nazwy kolumn (menu nadal pozostanie po angielsku)')
    else:
        print('Original columns remained')
    orig_columns = dan.columns
    time.sleep(1)
    os.system('cls')
    time.sleep(1)
    return orig_columns


def site_type(data, column_name):
    os.system('cls')
    time.sleep(1)
    area = round(data[column_name[9]].sum(),2)
    site_type_count = data[column_name[4]].value_counts().to_frame()
    unique_site_types = data[column_name[4]].unique()
    siteindex_data= data.set_index(column_name[4])
    site_type_count.columns = {'Ilość': column_name[4]}
    for x in unique_site_types:
        site_type_count.loc[x, 'pow [a]'] = round(siteindex_data.loc[x, column_name[9]].sum(), 2)
        site_type_count.loc[x, 'pow [%]'] = round(siteindex_data.loc[x, column_name[9]].sum() / area * 100, 2)

    print('number of divisions:', sum, 'total area:', area, '\n',
          site_type_count)
    decyzja = input('do you wanna save this data to csv file? [y/n]: ')
    if decyzja == 'y':
        site_type_count.to_csv('sites.csv')
        print('the data has been saved to sites.csv')
    time.sleep(1)
    os.system('cls')
    time.sleep(1)


def forest_age(data, column_name):
    os.system('cls')
    time.sleep(1)
    print('----------------------------------------\naverage age:',round(data[column_name[13]].mean(),2),'lat.')
    print('maximum age:',round(data[column_name[13]].max(),2),'lat')
    area = round(data[column_name[9]].sum(), 2)
    commercial_forests = data[column_name[6]] == 'GOSP'
    commercial_forests_with_data= data.where(commercial_forests).dropna(subset=column_name[2])
    print('maximum age (commercial forests):',round(commercial_forests_with_data[column_name[13]].max(),2),'lat')
    print('5 divisions with oldest trees:\n',
          commercial_forests_with_data.nlargest(n=5,columns=column_name[13]).loc[:,[column_name[2],column_name[13]]],
          '\n')
    kw = np.arange(0,100,20)
    for x in kw :
        a=data[column_name[13]].between(x,x+20)
        print(int((x+20)/20),' class age',data[column_name[9]].where(a).count(), 'divisions\t',round(data[column_name[9]].where(a).sum(),2),'a\t', round(data[column_name[9]].where(a).dropna().sum()/area*100,2),'% lands')
    a=data[column_name[13]].between(100,120)
    print('6+ class age',data[column_name[9]].where(a).count(), 'divisions\t',round(data[column_name[9]].where(a).sum()), 'a\t',round(data[column_name[9]].where(a).sum()/area*100),'% lands')
    time.sleep(1)
    input('click "enter" to continue')
    os.system('cls')
    time.sleep(1)

def select_division(data):
    os.system('cls')
    time.sleep(1)
    print('------------------------------\nGive division adress. '
          'You can give only part of address to see more divisions')
    while True:
        address = input('address structure:\nRR-NN-O-LL-Aaaaaa-Pppp-00\n02-11-1-04-192 used if no value is entered\n')
        if address == '':
            address = '02-11-1-04-192'
        filter_data = data[data.iloc[:,2].str.contains(address)]
        filter_data = filter_data.iloc[:,2:]
        print(f'selected {filter_data.iloc[:, 0].count()} divisions')
        # print(filter_data.head(10))
        if len(filter_data) < 10:
            print(filter_data.iloc[:,:])
        else:
            print(filter_data.iloc[:10,:])

        choose = input('click any button for try again\n\n8 - return\n9 - exit\n')
        if choose == '8':
            break
        elif choose == '9':
            exit()

        #
        # filter_data.head()
        # print(filter_data.count())

def edit_division(data):
    os.system('cls')
    time.sleep(1)
    print('Example for address: 02-11-1-04-192   -d   -00 (used if no value is entered)')
    wrong_count = 0
    while True:
        address = input('address structure:\nRR-NN-O-LL-Aaaaaa-Pppp-00\n')
        if address == '':
            address = '02-11-1-04-192   -d   -00'
        if len(data[data[data.columns[2]].str.contains(address)]) == 0:
            print('division not found')
        else:
            print(f'Selected division: \n{data[data[data.columns[2]].str.contains(address)]}')
            break
    while True:
        column = input('select column name ("species_cd" if no value is entered)\n')
        if column == '':
            column = data.columns[11]
        if column in data.columns:
            print('selected column')
            break
        else:
            print('wrong column name. try again click enter for use example')
    value_index = data[data[data.columns[2]].str.contains(address)].index[0]

    print(f'actual value: {data.at[value_index, column]}')

    while wrong_count < 5:
        new_value = input('add new value: ')
        if type(data.at[value_index, column]) == int or type(data.at[value_index, column]) == np.int64:
            try:
                new_value = np.int64(new_value)
            except:
                print('wrong value.')
                wrong_count += 1
                continue
        if type(data.at[value_index, column]) == type(new_value):
            data.at[value_index, column] = new_value
            print('changes was added successfully')
            break
        else:
            print('wrong type')
            wrong_count += 1
    if wrong_count == 5:
        input('too many wrong attempts. click enter\n')
        return data
    if_save = input('do you wanna save new file?[y/n]: ')
    if if_save == 'y':
        name = input('select file name: ')
        name = f'{name}.csv'
        data.to_csv(name)
        print('success')
    return data
    time.sleep(1)
