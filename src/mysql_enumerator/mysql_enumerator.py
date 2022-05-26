import os.path
import mysql_enumerator.mysql_enumerator_constants
import pandas as pd
import pymysql

class MySqlEnumerator():

    def __init__(self, hostname='', username='', password='', port=3306, schema=None, table=None, admin=False, verbose=False):
        # Intialize member variables
        self.hostname = hostname
        self.username = username
        self.password = password
        self.schema = schema
        self.port = port
        self.table = table
        self.admin = admin
        self.verbose = verbose
        self.connection = None
        


    def exfil_table(self, table, cursor):
        sql = "SELECT * FROM " + self.schema + "." + table
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # collect info on all tables in db
    def db_report(self, cursor):
        final = {}
        db_layout = []
        # collect schemas
        sql = "select schema_name from information_schema.schemata"
        cursor.execute(sql)
        result = cursor.fetchall()

        # collect tables for each schema
        for x in result:
            tables = []
            schema = x['schema_name']
            sql = "SELECT table_name FROM information_schema.tables WHERE table_schema = '" + schema
            cursor.execute(sql)
            table_query = cursor.fetchall()

            # collect columns for each table
            for y in table_query:
                table = y['table_name']
                sql = "SELECT COLUMN_NAME,DATA_TYPE FROM information_schema.COLUMNS WHERE table_name = '" + table
                cursor.execute(sql)
                columns = cursor.fetchall()
                cols = []

                for z in columns:
                    cols.append({'column': z['COLUMN_NAME'], 'data_type': z['DATA_TYPE']})
                tables.append({'table': table, 'columns': cols})

            db_layout.append({'schema': schema, 'tables': tables})

        final['db_layout'] = db_layout

        # if running in admin mode collect user data
        if self.admin:
            sql = "SELECT * FROM user"
            cursor.execute(sql)
            users = cursor.fetchall()
            final['users'] = users

        return final


    def run(self):

        # connect to the databse
        self.connection = pymysql.connect(host=self.hostname,
                                     user=self.username,
                                     password=self.password,
                                     # db=args.schema,
                                     charset='utf8mb4',
                                     port=self.port,
                                     cursorclass=pymysql.cursors.DictCursor)

        try:
            with self.connection.cursor() as cursor:
                # if table and schema provided output content of table to an excel file
                if self.table:
                    for x in str(self.table).split(','):
                        results = self.exfil_table(x, cursor)
                        df = pd.DataFrame(results)
                        df.to_excel(x + '.xlsx')
                else:
                    # if no table is provided print out details about all tables in the database
                    results = self.db_report(cursor)
                    for schema in results['schema']:
                        print('SCHEMA: ' + schema['schema'])
                        print('---------------------------------------------------\n')
                        for table in schema['table']:
                            print('\tTABLE: ' + table)
                            for column in table['column']:
                                print('\t\t' + column['column'] + ": " + column['data_type'])
                            print('\n\n')

                    # if running in admin mode print out user info
                    if self.admin:
                        df = pd.DataFrame(results['users'])
                        df.to_excel('users.xlsx')
                        print('USERS')
                        print('---------------------------------------------------\n')
                        for user in results['users']:
                            print('\tHOST: ' + user['Host'])
                            print('\tUSER: ' + user['User'])
                            print('\tPASSWORD: ' + user['Password'] + '  EXPIRED: ' + user['password_expired'])

                            # print out user privs
                            print('\tPRIVILEGES:')
                            if user['Select_priv'] == 'Y':
                                print('\t\tSELECT')
                            if user['Inser_priv'] == 'Y':
                                print('\t\tINSERT')
                            if user['Update_priv'] == 'Y':
                                print('\t\tUPDATE')
                            if user['Delete_priv'] == 'Y':
                                print('\t\tDELETE')
                            if user['Create_priv'] == 'Y':
                                print('\t\tCREATE')
                            if user['Drop_priv'] == 'Y':
                                print('\t\tDROP')
                            if user['File_priv'] == 'Y':
                                print('\t\tFILE')
                            if user['Grant_priv'] == 'Y':
                                print('\t\tGRANT')
                            if user['Super_priv'] == 'Y':
                                print('\t\tSUPER')
                            if user['Create_user_priv'] == 'Y':
                                print('\t\tCREATE_USER')
                            
                            if self.verbose:
                                if user['Reload_priv'] == 'Y':
                                   print('\t\tRELOAD')
                                if user['Shutdown_priv'] == 'Y':
                                   print('\t\tSHUTDOWN')
                                if user['Process_priv'] == 'Y':
                                   print('\t\tPROCESS')
                                if user['References_priv'] == 'Y':
                                   print('\t\tREFERENCES')
                                if user['Index_priv'] == 'Y':
                                   print('\t\tINDEX')
                                if user['Alter_priv'] == 'Y':
                                   print('\t\tALTER')
                                if user['Show_db_priv'] == 'Y':
                                   print('\t\tSHOW_DB')
                                if user['Create_tmp_table_priv'] == 'Y':
                                   print('\t\tCREATE_TMP_TABLE')
                                if user['Lock_tables_priv'] == 'Y':
                                   print('\t\tLOCK_TABLES')
                                if user['Execute_priv'] == 'Y':
                                   print('\t\tEXECUTE')
                                if user['Repl_slave_priv'] == 'Y':
                                   print('\t\tREPL_SLAVE')
                                if user['Create_view_priv'] == 'Y':
                                   print('\t\tCREATE_VIEW')
                                if user['Show_view_priv'] == 'Y':
                                   print('\t\tSHOW_VIEW')
                                if user['Create_routine_priv'] == 'Y':
                                   print('\t\tCREATE_ROUTINE')
                                if user['Alter_routine_priv'] == 'Y':
                                   print('\t\tALTER_ROUTINE')
                                if user['Event_priv'] == 'Y':
                                   print('\t\tEVENT')
                                if user['Trigger_priv'] == 'Y':
                                   print('\t\tTRIGGER')
                                if user['Create_tablespace_priv'] == 'Y':
                                   print('\t\tCREATE_TABLESPACE')
                                if user['Delete_history_priv'] == 'Y':
                                   print('\t\tDELETE_HISTORY')


        except pymysql.err.OperationalError:
            print('Unable to make a connection to the mysql database')
        finally:
            self.connection.close()


