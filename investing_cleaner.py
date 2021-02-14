import sqlite3
import pandas
import calendar
from time import strptime

def ism_execute(name_dict, to_sql=True):
    path = "data/" + name_dict + ".csv"
    path_temp = "data/" + name_dict + "_temp.csv"

    Actual_Y = "Actual_Y_" + name_dict
    Actual_M = "Actual_M_" + name_dict
    Actual_D = "Actual_D_" + name_dict
    Release_Y = "Release_Y_" + name_dict
    Release_M = "Release_M_" + name_dict
    Release_D = "Release_D_" + name_dict
    Release_H = "Release_H_" + name_dict
    Release_Date = "Release_Date_" + name_dict
    Actual_Date = "Actual_Date_" + name_dict
    Prev = "Prev_" + name_dict

    # Detect in which row the mistmatch is
    table = pandas.read_csv(filepath_or_buffer=path, index_col= 0)
    month_col = table[Actual_M]
    for i, elem in enumerate(month_col):
        if ":" in elem:
            init_pos = i
            break

    # Detect in which row notation chages again. Is excluded from storage
    for i, elem in enumerate(table[Release_H]):
        if "04:00" in elem:
            last_pos = i-1
            break
    table = table.loc[:last_pos]

    # Trasnform previous months names
    table[Release_M] = table[Release_M].apply(lambda x: strptime(x, '%b').tm_mon).astype('uint8')
    table[Actual_M] = table[Actual_M][0:init_pos].apply(lambda x: strptime(x, '%b').tm_mon)

    # Move all involved cols from specified row
    for i in range(init_pos, len(table[Prev])):
        table.iat[i, -1] = table.iat[i, -2]
        table.iat[i, -2] = table.iat[i, -3]
        table.iat[i, -3] = table.iat[i, -4]
        table.iat[i, -4] = table.iat[i, -5]
        prev_release_m = table.at[i-1, Release_M]
        prev_actual_m = table.at[i-1, Actual_M]
        if prev_release_m == prev_actual_m:     #Association Release-Actual month
            if prev_actual_m == 1:
                table.at[i, Actual_M] = 12
            else:
                table.at[i, Actual_M] = prev_actual_m - 1
        else:
            table.at[i, Actual_M] = prev_actual_m

    table[Actual_M] = table[Actual_M].astype('uint8')

    # Actual_Y logic
    table.insert(loc=0, column=Actual_Y, value=table[Release_Y])
    for i in range(0, len(table[Actual_M])):
        if table.at[i, Actual_M] > table.at[i, Release_M]:
            table.at[i, Actual_Y] = table.at[i, Release_Y] - 1


    # Join Release_Y-Release_M-Release_D
    table.insert(loc=0, column=Release_Date, value='None')
    table.insert(loc=0, column=Actual_Date, value='None')
    table[Release_Date] = table[Release_Y].astype(str) + "-" + table[Release_M].astype(str) + "-" + table[Release_D].astype(str)

    # Join Actual_Y-Actual_M
    table[Actual_Date] = table[Actual_Y].astype(str) + "-" + table[Actual_M].astype(str)

    if to_sql == True:
        con = sqlite3.connect("data/db/economic_data.sqlite")
        table.to_sql(name=name_dict, con=con, if_exists='replace')
    else:
        table.to_csv(path_temp)

def markit_execute(name_dict, to_sql=True):
    path = "data/" + name_dict + ".csv"

    Actual_Y = "Actual_Y_" + name_dict
    Actual_M = "Actual_M_" + name_dict
    Actual_D = "Actual_D_" + name_dict
    Release_Y = "Release_Y_" + name_dict
    Release_M = "Release_M_" + name_dict
    Release_D = "Release_D_" + name_dict
    Release_Date = "Release_Date_" + name_dict
    Actual_Date = "Actual_Date_" + name_dict
    Forecast = "Forecast_" + name_dict
    Prev = "Prev_" + name_dict

    table = pandas.read_csv(filepath_or_buffer=path, index_col= 0)
    table.drop([Forecast, Prev], axis=1, inplace=True)
    month_col = table[Actual_M]
    for i, elem in enumerate(month_col):
        if ":" in elem:
            last_pos = i-1
            break
    table = table.loc[:last_pos]

    # Trasnform previous months names
    table[Release_M] = table[Release_M].apply(lambda x: strptime(x, '%b').tm_mon).astype('uint8')
    table[Actual_M] = table[Actual_M].apply(lambda x: strptime(x, '%b').tm_mon).astype('uint8')

    # Actual_Y logic
    table.insert(loc=0, column=Actual_Y, value=table[Release_Y])
    for i in range(0, len(table[Actual_M])):
        if table.at[i, Actual_M] > table.at[i, Release_M]:
            table.at[i, Actual_Y] = table.at[i, Release_Y] - 1

    # Add 0 before single digit month and day
    table[Release_M] = table[Release_M].apply(lambda x: f'{str(x):>02}')
    table[Release_D] = table[Release_D].apply(lambda x: f'{str(x):>02}')
    table[Actual_M] = table[Actual_M].apply(lambda x: f'{str(x):>02}')

    # Join Release_Y-Release_M-Release_D
    table.insert(loc=0, column=Release_Date, value='None')
    table.insert(loc=0, column=Actual_Date, value='None')
    table[Release_Date] = table[Release_Y].astype(str) + "-" + table[Release_M]+ "-" + table[Release_D]

    # Join Actual_Y-Actual_M + first or second fortnight
    table[Actual_Date] = table[Actual_Y].astype(str) + "-" + table[Actual_M]
    for i, elem in enumerate(table[Release_Date]):
        if int(elem[-2:]) > 15:
            table.at[i, Actual_Date] = table.at[i, Actual_Date] + "-15"
        else:
            table.at[i, Actual_Date] = table.at[i, Actual_Date] + "-30"

    if to_sql == True:
        con = sqlite3.connect("data/db/economic_data.sqlite")
        table.to_sql(name=name_dict, con=con, if_exists='replace')
    else:
        table.to_csv(path)

def michigan_inflation_execute(name_dict, to_sql=True):
    path = "data/" + name_dict + ".csv"

    Actual_V = "Actual_" + name_dict
    Actual_Y = "Actual_Y_" + name_dict
    Actual_M = "Actual_M_" + name_dict
    Actual_D = "Actual_D_" + name_dict
    Release_Y = "Release_Y_" + name_dict
    Release_M = "Release_M_" + name_dict
    Release_D = "Release_D_" + name_dict
    Release_Date = "Release_Date_" + name_dict
    Actual_Date = "Actual_Date_" + name_dict
    Forecast = "Forecast_" + name_dict
    Prev = "Prev_" + name_dict

    table = pandas.read_csv(filepath_or_buffer=path, index_col= 0)
    table.drop([Forecast, Prev], axis=1, inplace=True)

    # Trasnform previous months names
    table[Release_M] = table[Release_M].apply(lambda x: strptime(x, '%b').tm_mon).astype('uint8')
    table[Actual_M] = table[Actual_M].apply(lambda x: strptime(x, '%b').tm_mon).astype('uint8')

    # Actual_Y logic
    table.insert(loc=0, column=Actual_Y, value=table[Release_Y])
    for i in range(0, len(table[Actual_M])):
        if table.at[i, Actual_M] > table.at[i, Release_M]:
            table.at[i, Actual_Y] = table.at[i, Release_Y] - 1

    # Add 0 before single digit month and day
    table[Release_M] = table[Release_M].apply(lambda x: f'{str(x):>02}')
    table[Release_D] = table[Release_D].apply(lambda x: f'{str(x):>02}')
    table[Actual_M] = table[Actual_M].apply(lambda x: f'{str(x):>02}')

    # Join Release_Y-Release_M-Release_D
    table.insert(loc=0, column=Release_Date, value='None')
    table.insert(loc=0, column=Actual_Date, value='None')
    table[Release_Date] = table[Release_Y].astype(str) + "-" + table[Release_M]+ "-" + table[Release_D]

    # Join Actual_Y-Actual_M + first or second fortnight
    table[Actual_Date] = table[Actual_Y].astype(str) + "-" + table[Actual_M] + "-30"
    for i,m in enumerate(table[Actual_M]):
        if i == 0:
            if m != table.at[i+1, Actual_M]:
                table.at[i, Actual_Date] = table.at[i, Actual_Date][:-2] + "15"
        else:
            if m == table.at[i-1, Actual_M]:
                table.at[i, Actual_Date] = table.at[i, Actual_Date][:-2] + "15"

    # Delete 1st row if value is empty (no %)
    if '%' not in str(table.at[0, Actual_V]):
        table = table.iloc[1:]

    # Trim % char from all values and turn em into float
    table[Actual_V] = table[Actual_V].apply(lambda x: x.replace("%", ""))
    table[Actual_V] = pandas.to_numeric(table[Actual_V], downcast="float")

    if to_sql == True:
        con = sqlite3.connect("data/db/economic_data.sqlite")
        table.to_sql(name=name_dict, con=con, if_exists='replace')
    else:
        table.to_csv("data/" + name_dict + "temp.csv")

def ism_new_orders_execute(name_dict, to_sql=True):
    path = "data/" + name_dict + ".csv"

    Actual_V = "Actual_" + name_dict
    Actual_Y = "Actual_Y_" + name_dict
    Actual_M = "Actual_M_" + name_dict
    Actual_D = "Actual_D_" + name_dict
    Release_Y = "Release_Y_" + name_dict
    Release_M = "Release_M_" + name_dict
    Release_D = "Release_D_" + name_dict
    Release_H = "Release_H_" + name_dict
    Release_Date = "Release_Date_" + name_dict
    Actual_Date = "Actual_Date_" + name_dict
    Prev = "Prev_" + name_dict

    # Detect in which row the mistmatch is
    table = pandas.read_csv(filepath_or_buffer=path, index_col= 0)
    month_col = table[Actual_M]
    for i, elem in enumerate(month_col):
        if ":" in elem:
            init_pos = i
            break

    # Move all involved cols from specified row
    table.iat[init_pos, -1] = table.iat[init_pos, -2]
    table.iat[init_pos, -2] = table.iat[init_pos, -3]
    table.iat[init_pos, -3] = table.iat[init_pos, -4]
    table.iat[init_pos, -4] = table.iat[init_pos, -5]

    # Fix specific actual month case for michigan
    table.at[init_pos, Actual_M] = "Sep"
    
    # Trasnform previous months names
    table[Release_M] = table[Release_M].apply(lambda x: strptime(x, '%b').tm_mon).astype('uint8')
    table[Actual_M] = table[Actual_M].apply(lambda x: strptime(x, '%b').tm_mon)

    table[Actual_M] = table[Actual_M].astype('uint8')

    # Actual_Y logic
    table.insert(loc=0, column=Actual_Y, value=table[Release_Y])
    for i in range(0, len(table[Actual_M])):
        if table.at[i, Actual_M] > table.at[i, Release_M]:
            table.at[i, Actual_Y] = table.at[i, Release_Y] - 1


    # Join Release_Y-Release_M-Release_D
    table.insert(loc=0, column=Release_Date, value='None')
    table.insert(loc=0, column=Actual_Date, value='None')
    table[Release_Date] = table[Release_Y].astype(str) + "-" + table[Release_M].astype(str) + "-" + table[Release_D].astype(str)

    # Join Actual_Y-Actual_M
    table[Actual_Date] = table[Actual_Y].astype(str) + "-" + table[Actual_M].astype(str)

    if to_sql == True:
        con = sqlite3.connect("data/db/economic_data.sqlite")
        table.to_sql(name=name_dict, con=con, if_exists='replace')
    else:
        table.to_csv(path)

if __name__ == "__main__":
    ism_execute("IMCEM", False)
    #markit_execute("IPMICMM", False)
    #michigan_inflation_execute("IMCEM", False)
    #ism_new_orders_execute("INOISMM", True)