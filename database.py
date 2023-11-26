import pypyodbc
import pandas as pd

import config as cg


def connect_db(DATABASE_DIR, PWD):
    ''' connect to the database
    '''
    conn = None

    try:
        connection = 'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=%s;PWD=%s'%(DATABASE_DIR,PWD)
        conn = pypyodbc.connect(connection)
        cursor =  conn.cursor()
        # print(f'connection : {connection}')
        # print(f'conn: {conn}')
        # print(f'cursor: {cursor}')
    except:
        return False, False
        print(f'>> cannot connect with the database. Bye~')

    return conn, cursor

def fetch_db(DATABASE_DIR, table, col, *,  PWD):
    ''' A function to pull out a column from  a table in the db
        DATABASE_DIR = database location
        table = name of the table
        column = name of the column'''

    conn, cursor = connect_db(DATABASE_DIR , PWD)

    if conn == False:
        col_lt = False
    else:
        col = cursor.execute(f'SELECT {col} FROM [{table}]')
        col = col.fetchall()
        col_lt = []
        for i in col:
            col_lt.append(list(i)[0])
        # Close the cursor and connection
        cursor.close()
        conn.close()

    return col_lt

def fetch_ndw(DATABASE_DIR, table_name, col, col_1,chno, col_2,  *,  PWD):
    ''' fetch the NDW factor closest to today
        DATABASE_DIR = database location
        table_name= name of the table
        col = output data
        col_1 = condition column 1
        chno = chamber number
        col_2 = condition column 2
        '''

    conn, cursor = connect_db(DATABASE_DIR , PWD)

    if conn == False:
        result = False
    else:

         sql = '''SELECT {col}
             FROM {table_name}
             WHERE {col_1} LIKE ? AND [{col_2}] = (SELECT MAX([{col_2}]) FROM {table_name} WHERE {col_1} LIKE ?);
          '''.format(col=col, table_name=table_name, col_1=col_1, col_2=col_2)



    # prepare values to substitute for ? in SQL
    params = (chno, chno)
    try:
        cursor.execute(sql, params)
        result = cursor.fetchone()
        result = result[0][0]

        # Close the cursor and connection
        cursor.close()
        conn.close()

    except:
        print(f'Fail to fetch NDW. You want to add this to the report')

    return result
