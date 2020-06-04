from os import system, name
import sys, sqlite3
from sqlite3 import Error
  

def clear(): 
  
    if name == 'nt': 
        _ = system('cls') 
    else: 
        _ = system('clear')


def create_connection(path):
    connection = None
    try:
        connection = sqlite3.connect(path)
        #print("Connection to SQLite DB successful")
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection
        
        
def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def manageNum_query(connection, query, task):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query, task)
        result = cursor.fetchone()[0]
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


def update_num(conn, task):

    sql = """ UPDATE sklad
              SET num = ?
              WHERE name = ?"""
    cursor = conn.cursor()
    cursor.execute(sql, task)
    conn.commit()


create_table = """
CREATE TABLE IF NOT EXISTS sklad (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  name TEXT NOT NULL,
  num INTEGER,
  numSum INTEGER,
  since DATE);
"""

fill_table = """
INSERT INTO
  sklad (name, num, numSum, since)
VALUES
  ('KK25', 0, '0', '2020-04-16'),
  ('KF25', 0, '0', '2020-04-16'),
  ('NS25', 0, '0', '2020-04-16'),
  ('NG25', 0, '0', '2020-04-16');
"""

select_one_from_table = """
    SELECT CAST(num as INTEGER) FROM sklad
    WHERE name LIKE ?
"""

update_table = """
UPDATE
  sklad
SET
  num = 5
WHERE
  id = 
"""

print_all = """
SELECT * FROM sklad
"""


def mainMenu():

    while (True):
        menuChoice = input("1.Vydať \n2.Vložiť \n3.Výpis\n")

        if menuChoice == '1':
            outFile(connection)

        if menuChoice == '2':
            inFile(connection)

        if menuChoice == '3':
            all = execute_read_query(connection, print_all)
            for obj in all:
                print(obj)
        input()
        clear()


def databaseUpdate(connection, inString, mode):

    inArr = inString.split(',')
    for obj in inArr:
        obj = obj.strip()
        obj = obj.split()
        sortimStr = obj[0]
        sortimNum = int(obj[1])
        sortimNumDB = manageNum_query(connection, select_one_from_table, (sortimStr,))

        if mode == "in":
            update_num(connection, (sortimNumDB + sortimNum, sortimStr))
        else:
            if sortimNumDB - sortimNum < 0:
                print("Tolko tam ani neni!!")
                break
            update_num(connection, (sortimNumDB - sortimNum, sortimStr))
    

def outFile(connection):

    inString = input("Vydať: ") 
    databaseUpdate(connection, inString, "out")
    

def inFile(connection):

    inString = input("Vložiť: ")
    databaseUpdate(connection, inString, "in")


#----------main----------

connection = create_connection(r"C:\Users\marti\source\repos\sklad\sklad\\skladDB")
#execute_query(connection, create_table)

#execute_query(connection, fill_table)

#execute_query(connection, update_table)

mainMenu()
