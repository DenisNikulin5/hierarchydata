import sys
import json
from sqlalchemy import create_engine
from sqlalchemy.sql import text

#Configs
engine = create_engine("postgresql+psycopg2://user:password@localhost/mydb") #Don't forget to change connection string

#Const
OFFICE_TYPE = 1
DEPARTMENT_TYPE = 2
EMPLOYEE_TYPE = 3
CLI_TIP = """Please use following commands for this tool:
    json-to-db <path-to-json> - import data from json file to PostgreSQL
    office-by-employee-id <id> - get office info using employee id related to this office"""


def import_to_db(json):
    """Import data from JSON to PostgreSQL DB."""
    with engine.connect() as con:
        statement = text("""CREATE TABLE IF NOT EXISTS entity(
            id SERIAL PRIMARY KEY, 
            ParentId INTEGER,
            Name VARCHAR(50) NOT NULL,
            Type INTEGER NOT NULL,
            FOREIGN KEY (ParentId) REFERENCES entity(id));""")
        con.execute(statement)

        query = "INSERT INTO entity(id, ParentId, Name, Type) VALUES "
        for row in test_data:
            query += f"({row['id']}, {row['ParentId'] or 'NULL'}, '{row['Name']}', {row['Type']}), "
        query = query[:-2] + ";"
        
        statement = text(query)
        con.execute(statement)
        con.commit()


def get_office_by_employee_id(emp_i):
    """Get office info using employee id related to this office."""
    with engine.connect() as con:
        # Main expression for getting employee's names recursively based on their office id.
        statement = text("""WITH RECURSIVE e AS(
        SELECT id, ParentId, Name, Type
        FROM entity
        WHERE id = (
            WITH RECURSIVE e AS(                               
                SELECT id, ParentId, Type
                FROM entity """
                f"WHERE id = {emp_i} and Type = {EMPLOYEE_TYPE} " # Subexpresion for getting an office id recursively.
                """UNION SELECT par.id, par.ParentId, par.Type
                FROM entity par
                INNER JOIN e ON e.ParentId = par.id """
            f") SELECT id FROM e where Type = {OFFICE_TYPE}"
        """)
        UNION SELECT sub.id, sub.ParentId, sub.Name, sub.Type
        FROM entity sub
        INNER JOIN e ON sub.ParentId = e.Id"""
        f") SELECT Name, Type FROM e WHERE Type != {DEPARTMENT_TYPE} ORDER BY Type;")
        
        #get result as dict
        res = con.execute(statement).mappings().all()


    #First item must be office always since the expression above ordered by type
    office = res.pop(0)

    # Data verification
    if office["type"] != OFFICE_TYPE:
        #Raise exception if no office
        raise Exception("An error happened when obtaining office info")

    if not all(map(lambda i: i["type"] == EMPLOYEE_TYPE, res)):
        #raise expections if type is not "Employee" for every item on the list
        raise Exception("An error happened when obtaining employee's info")

    return {"name": office["name"], "employees": [e["name"] for e in res]}
    
  

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print(CLI_TIP)
        quit()

    command = sys.argv[1]
    parameter = sys.argv[2]

    if command == "json-to-db":
        try:
            file_data = test_data = json.load(open(sys.argv[2]))
        except:
            print("Error:Please check your json file.")
            raise
        
        import_to_db(file_data)
    elif command == "office-by-employee-id":
        try:
            parameter = int(parameter)
        except:
            print("Invalid id")
            quit()

        office = get_office_by_employee_id(parameter)

        print(office["name"] + ": ", end="")
        
        last_i = len(office["employees"]) - 1
        for i in range(last_i):
            print(office["employees"][i] + ", ", end="")
        print(office["employees"][last_i] + ".")
    else:
        print(CLI_TIP)


        

    
    
    
    








