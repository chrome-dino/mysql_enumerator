import os.path
import mysql_enumerator.mysql_enumerator_constants

class MySqlEnumerator():
   
   def __init__(self):
         

   def exfil_table(self,table,schema,cursor):
       sql = "SELECT * FROM " + schema + "." + table
       cursor.execute(sql)
       result = cursor.fetchall()
       return result


   # collect info on all tables in db
   def db_report(self,cursor, admin):
       final = {}
       db_layout = []
       # collect schemas
       sql = "select schema_name from information_schema.schemata"
       cursor.execute(sql)
       result = cursor.fetchall()

       # collect tables for each schema
       for x in result:
           tables = {}
           schema = x['schema_name']
           sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = '" + schema
           table_query = cursor.fetchall()

           #collect columns for each table
           for y in table_query:
               table = y['table_name']
               sql = "SELECT COLUMN_NAME,DATA_TYPE FROM information_schema.COLUMNS WHERE table_name = '" + table
               columns = cursor.fetchall()
               cols = []

               for z in columns:
                   cols.append({'column':z['COLUMN_NAME'],'data_type':z['DATA_TYPE']})
               tables.append({'table':table,'columns':cols})

           db_layout.append({'schema':schema,'tables':tables})

       final['db_layout'] = db_layout

       # if running in admin mode collect user data
       if admin:
           sql = "SELECT * FROM user"
           users = cursor.fetchall()
           final['users'] = users



       return final

