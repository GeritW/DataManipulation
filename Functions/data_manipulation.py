import sqlite3
from enum import Enum
import numpy as np
import pandas as pd
import json

# WARNING = 0
# CHANGE = 1
# DELETE = 2 complete row/column if one is wrong!
# Half DELETE = 3 only false value will be deleted (DB - NULL)

class ChangeType(Enum):
    int = np.dtype('int32') #Error with 64
    datetime = np.dtype('datetime64[ns]')
    str = np.dtype('O')
    float = np.dtype('float_')

class DataManipulation:
    def __init__(self):
        pass

    def __read_excel_file(self):
        """
            Read excel file with specific parameters and safe it to dataframe.
        """
        cols_list = []
        self.rows[0] = self.rows[0].replace(" ", "")
        numbers = self.rows[0].split(',')
        
        #split list and check if there are two parts from slicing
        for i in range(len(numbers)):
            num = numbers[i].split(':')
            if len(num) > 1:
                for j in range(int(num[0]), int(num[1])+1):
                    cols_list.insert(0, j-1)
            else:
                cols_list.insert(0, int(num[0])-1)

        self.data = pd.read_excel(
            io=self.path,
            sheet_name=self.sheet_name,
            index_col=0,
            usecols=self.columns[0],
            skiprows= lambda x: x not in cols_list
        )
        self.data = self.data.T

    def __check_names_and_types(self):
        """
            Compare column names and types in dataframe with name and types from configuration file.
            If data (name or type) is wrong -> Data warning, deleted, or default value.
        """
        expected_types_names = self.config_data["types_and_names"]
        data_dict = dict(zip(self.data.columns, self.data.dtypes))
        expected_names = expected_types_names.keys()
        val = list(expected_names)
        wrong_types = []
        safe_val = []
        i = 0
        j = 0

        if data_dict is not expected_types_names:
            res = list(set(data_dict.keys()).difference(set(expected_names)))
            for x in data_dict:
                if (data_dict[x] != expected_types_names[val[i]]):
                    wrong_types.append(x)
                    safe_val.append(val[i]) #for right type ausgabe
                i = + i + 1

        if wrong_types or res:
            for p in range(len(self.wrong_data)):
                if self.wrong_data[p] and p == 0: #warning
                    if res:
                        print(f"Wrong names: {res}.")
                    for x in self.wrong_data[p]:
                        print(f"Wrong type in column {x}. Has to be {expected_types_names[safe_val[j]]} but is {data_dict[x]}.")
                    j = j+1
                if self.wrong_data[p] and p == 2: #Delete (whole row/col)
                    for x in self.wrong_data[p]:
                        if x in wrong_types:
                            self.data.drop(x, axis=1, inplace=True)
                            print(f"Deleted {x}!") 
                                                            
                if self.wrong_data[p] and p == 1: #Default
                    for x in self.wrong_data[p]:
                        if x in wrong_types:
                            self.data[x] = self.data[x].astype(np.dtype('O'))
                            print(f"Set default type for {self.wrong_data[p]}")
        else:
            print("Names and Datatypes are correct!")
                    
            
    def __check_ranges(self):
        """
            Check if values from row or column are within specific range value.
            If data is not within range -> Change data (Delete, Warning or Default)
        """
        for key, value in self.ranges.items():
                if key in self.data:
                    if (self.data[key] < value[0]).any():
                        self.__change_data(key, self.data[key] < value[0], value[0], key)
                    if (self.data[key] > value[1]).any():
                        self.__change_data(key, self.data[key] > value[1], value[1], key)
                else:
                    print(f"Data (in {key}) is already deleted!")

    def __change_data(self, col, diff, value, key):
        """
            Change wrong data which was not in range -> Delete, Warning or Default.
        """        
        if self.transpose == "False":
            i = self.data.index
            for_loop = range(len(i))
        else:
            i = self.data.index.values  
            for_loop = range(len(diff))

        if key in self.wrong_data[1]:
            for x in for_loop:
                if diff[i[x]]:
                    self.data.at[i[x], col] = value
                    print(f"Default value {value} in {col} -> {i[x]}.")
    
        if key in self.wrong_data[0]:
            for x in for_loop:
                if diff[i[x]]:
                    val = self.data._get_value(i[x], col)
                    if self.transpose == "False":
                        print(f"Row {col} has value out of range: {val} (col {i[x]})")
                    else:
                        print(f"Column {col} has value out of range: {val} (line {i[x]}).")
        
        if key in self.wrong_data[3]:
            for x in for_loop:
                if diff[i[x]]:
                    self.data.at[i[x], col] = np.NaN
                    print(f"Deleted {col} in {i[x]}.")  

    def parse_to_database(self):
        """
            Write dataframe into sql table. 
        """
        connection = sqlite3.connect(self.db_path)
        cur = connection.cursor()
        #check if table exists
        table = cur.execute("SELECT '" + self.db_table + "' FROM sqlite_master WHERE type='table' AND name='" + self.db_table + "'; ").fetchall()
        #check index
        if not self.row_name:
            self.row_name = "INDEX"
        #change direction
        if self.transpose == False:
            self.data.T
        if self.new_table == "replace":
            self.data.to_sql(self.db_table, connection, if_exists="replace", index_label = self.row_name)
        else:
            if not table:
                print("Error -> " + self.db_table + " DOES NOT exist and cannot append!")
            else:
                self.data.to_sql(self.db_table, connection, index_label = self.row_name, if_exists="append")
                    
    def get_tables_from_database(self, table_name):
        connection = sqlite3.connect(self.db_path)
        cur = connection.cursor()
        table = cur.execute("SELECT '" + table_name + "' FROM sqlite_master WHERE type='table' AND name='" + table_name + "'; ").fetchall()
        if not table:
            print("Error -> " + table_name + " DOES NOT exist -> CANNOT be feteched!")
        else:
            self.df = pd.read_sql("select * from '" + table_name + "'", con=connection)
            connection.close()
            print(self.df)

    def __load_configuration(self, config_name):
        #JSON Data
        with open("JSON/"+config_name+".json", "r") as infile:
            data = json.load(infile)

        #Get starting values 
        self.path = data["file_information"]["path"]
        self.sheet_name = data["file_information"]["sheet_name"]

        self.config_data = data[config_name] #could be deleted and just use just data[]
        #Table specific values
        self.columns = self.config_data["position"]["columns"]
        self.rows = self.config_data["position"]["rows"]
        self.transpose = self.config_data["position"]["transpose"]
        self.ranges = self.config_data["ranges"]
        self.db_table = self.config_data["database"]["name"]
        self.new_table = self.config_data["database"]["mode"]
        self.db_path = self.config_data["database"]["path"]
        self.row_name = self.config_data["database"]["row_name"]
        delete_all = self.config_data["wrong_data"]["delete_all"]
        delete_val = self.config_data["wrong_data"]["delete_value"]
        warning = self.config_data["wrong_data"]["warning"]
        default = self.config_data["wrong_data"]["change"]    
        self.wrong_data = [warning, default, delete_all, delete_val]

        for key, value in self.config_data["types_and_names"].items():  #Workaround bc of saving datatype problems
            if value == "int":
                self.config_data["types_and_names"][key] = ChangeType.int.value
            if value == "str":
                self.config_data["types_and_names"][key] = ChangeType.str.value
            if value == "float":
                self.config_data["types_and_names"][key] = ChangeType.float.value
            if value == "datetime":
                self.config_data["types_and_names"][key] = ChangeType.datetime.value

    def verify_import(self, config_name):
        DataManipulation.__load_configuration(self, config_name)
        DataManipulation.__read_excel_file(self)
        DataManipulation.__check_names_and_types(self)
        if not self.ranges:
            print(f"No ranges to check!")
        else:
            DataManipulation.__check_ranges(self)        




class P:
    def __init__(self,x):
        self.x = x
   