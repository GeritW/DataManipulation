import json

all_tables = {
      "file_information" :
      {
            "path" : "../Sample Datasets/DatenSatz_01.xlsx",
            "sheet_name" : "CRF 1.0",
      },
      "ecp" : 
      {
           "types_and_names" : 
            {
                  "HD duration" : "int",
                  "total UF achieved" : "int",
                  "recirculation" : "int",
                  "OH (liter) [BCM]" : "str",
                  "pre HD weight" : "float",
                  "post HD weight" : "float"

             },
            "position" : 
            {
                  
                  "rows" : ["85, 89:92, 98:99"],
                  "columns" : ["A:B"],
                  "transpose" : "True"
            },
             "ranges" : [],

            "wrong_data" : 
            {
                  "warning" : ["pre HD weight"],
                  "change" : [],
                  "delete_all" : [],
                  "delete_value" : ["pre HD weight"]
            },
            "database": 
            {
                  "name" : "ECP",
                  "mode" : "replace",
                  "row_name": "",
                  "path" : "C:/Users/HP/Desktop/SQLite/Dummy.db"
            } 
      }
}

with open("Data Manipulation/JSON/ecp.json", "w") as outfile:
    json.dump(all_tables, outfile, indent=4)