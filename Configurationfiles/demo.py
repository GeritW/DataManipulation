import json

all_tables = {
      "file_information" :
      {
            "path" : "../Sample Datasets/DatenSatz_01.xlsx",
            "sheet_name" : "CRF 1.0",
      },
      "demo_parameter" : 
      {
            "types_and_names" : 
            {
                  "age (years)" : "int",
                  "dialysis vintage (month)" : "datetime",
                  "time since 1st diagnosis of CKD (years)" : "str",
                  "regular dialysate calcium concentration (mmol/l)" : "str",
                  "dry weight (kg)" : "float"
            },
            "position" : 
            {
                  "rows" : ["8:10, 12:13"],
                  "columns" : ["A:B, D:E"],
                  "transpose" : True
            },
            "ranges" : 
            {
                  "dry weight (kg)" : [5, 100], #Platzhalter
                  "age (years)" : [10, 100]
            },
            "wrong_data" : 
            {
                  "warning" : [],
                  "change" : [],
                  "delete_all" : [],
                  "delete_value" : ["age (years)"]
            },
            "database": 
            {
                  "name" : "Demo_Params",
                  "mode" : "replace",
                  "row_name": "demographic_parameters",
                  "path" : "C:/Users/HP/Desktop/SQLite/Dummy.db"
            }
      }     
}

with open("Data Manipulation/JSON/demo_parameter.json", "w") as outfile:
    json.dump(all_tables, outfile, indent=4)
