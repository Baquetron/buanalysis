import sqlite3
import pandas

NUM_ROWS = "13"   # Num of rows to display in plot

def one_line_table(con, a1):
    df = pandas.read_sql_query(
        "SELECT Actual_Date_"+ a1 +" AS DATE, Actual_"+ a1 +" FROM "+ a1 +" LIMIT "+ NUM_ROWS, con)
    return df

def two_line_table(con, a1, a2):
    df = pandas.read_sql_query(
        "SELECT Actual_Date_"+ a1 +" AS DATE, Actual_"+ a1 +", Actual_"+ a2 +" FROM "+ a1 +", "+ a2 +" WHERE Actual_Date_"+ a1 +" = Actual_Date_"+ a2 +" LIMIT "+ NUM_ROWS, con)
    return df

def three_line_table(con, a1, a2, a3):
    df = pandas.read_sql_query(
        "SELECT Actual_Date_"+ a1 +" AS DATE, Actual_"+ a1 +", Actual_"+ a2 +", Actual_"+ a3 +" FROM "+ a1 +", "+ a2 +", "+ a3 +" WHERE (Actual_Date_"+ a1 +" = Actual_Date_"+ a2 +" AND Actual_Date_"+ a2 +" = Actual_Date_"+ a3 +" LIMIT "+ NUM_ROWS +")", con)    
    return df

def four_line_table(con, a1, a2, a3, a4):
    df = pandas.read_sql_query(
        "SELECT Actual_Date_"+ a1 +" AS DATE, Actual_"+ a1 +", Actual_"+ a2 +", Actual_"+ a3 +", Actual_"+ a4 +" FROM "+ a1 +", "+ a2 +", "+ a3 +", "+ a4 +" WHERE (Actual_Date_"+ a1 +" = Actual_Date_"+ a2 +" AND Actual_Date_"+ a2 +" = Actual_Date_"+ a3 +" AND Actual_Date_"+ a3 +" = Actual_Date_"+ a4 +" LIMIT "+ NUM_ROWS +")", con) 
    return df

def simple_table_to_plot(con, out, name, a, *args):   #At least one index in inputs
    ind = [a]
    for i, elem in enumerate(args):
        ind.append(elem)
    # Probar a hacer un split para las entradas múltiples a ver si cuela
    if len(ind) == 1:
        df = one_line_table(con, ind[0])
    elif len(ind) == 2:
        df = two_line_table(con, ind[0], ind[1])
    elif len(ind) == 3:
        df = three_line_table(con, ind[0], ind[1], ind[2])
    elif len(ind) == 4:
        df = four_line_table(con, ind[0], ind[1], ind[2], ind[3])  
    else:
        print("4 indeces max!")
        return 0
    
    df.to_sql(name=name, con=out, if_exists='replace')

if __name__ == "__main__":
    con = sqlite3.connect("data/db/economic_data.sqlite")
    out = sqlite3.connect("data/db/dashboard_data.sqlite")
    a = "FERDIM"
    name = "Excess_Reserves_of_Depository_Institutions"
    simple_table_to_plot(con, out, name, a)



