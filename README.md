# HierarchyData

This Python script implements logic in order to get office info using employee id related to this office from PostgresDB.
You can also import json data from file to the PostgesDB for your convenience.

# Explanation

We should assume hierarchy depth is unlimited so it's needed to use recursive expressions.

In our case we have 2:
1. Subexpression that is used to get office id.
2. Main expression is used to get employees based on office id.

# Usage

You can run the script with 2 commands availibale:

- json-to-db <path-to-json> - import data from json file tpo PostgreSQL
- office-by-employee-id <id> - get office info using employee id related to this office

    Please ensure json file has valid format. Example:
    [{
    "id": 1,
    "ParentId": null,
    "Name": "St. Petersburg office",
    "Type": 1
    },
    {
    "id": 2,
    "ParentId": 1,
    "Name": "Development department",
    "Type": 2
  
   },
   {
    "id": 3,
    "ParentId": 2,
    "Name": "Иванов",
    "Type": 3
  }]

# Dependencies

I use SQLAlchemy Core + Psycopg2 to execute raw SQL expressions in the script. So please install them:
`pip install SQLAlchemy psycopg2`


# Example
**Input:**

`python main.py office-by-employee-id 17`

**Output:**  

Офис в Москве: Винтиков, Шпунтиков, Морозов, Белова, Крылова, Петрова, Иванова.