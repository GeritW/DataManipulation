import json

all_tables = {
      "file_information" :
      {
            "path" : "../Sample Datasets/DatenSatz_01.xlsx",
            "sheet_name" : "CRF 1.0",
      },
      "blood" : 
      {
            "types_and_names" : 
            {
                  "iCa (mmol/l)" : "float",
                  "Hb (g/dl)" : "float",
                  "hematocrit (%)" : "int",
                  "pH" : "float", 
                  "Hco3 (mmol/l)" : "float",
                  "Na (mmol/l)" : "int"
             },
            "position" : 
            {
                  "rows" : ["104:110"],
                  "columns" : ["A:B, D:F"],
                  "transpose" : "False"
            },
            "ranges" : 
            {     
                  "pH" : [7.1, 7.4],
                  "Na (mmol/l)" : [0, 140]
            }, 
            "wrong_data" : 
            {
                  "warning" : [],
                  "change" : ["pH", "Na (mmol/l)"],
                  "delete_all" : [],
                  "delete_value" : []
            },
            "database": 
            {
                  "name" : "Blood (POC)",
                  "mode" : "replace",
                  "row_name": "min",
                  "path" : "C:/Users/HP/Desktop/SQLite/Dummy.db"
            }
       } 
}

with open("Data Manipulation/JSON/blood.json", "w") as outfile:
    json.dump(all_tables, outfile, indent=4)
