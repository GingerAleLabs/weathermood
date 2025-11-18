'''
!!! EXECUTING THIS SCRIPT RESULTS IN THE DELETION OF ALL THE ENTRIES
Add mock data to the entry table
'''
from backend.model.DbException import DbException
from backend.model.db import insert_mock_data

try:
    insert_mock_data()
except DbException as e:
    print("Could not insert mock data into the database")
    print(e)