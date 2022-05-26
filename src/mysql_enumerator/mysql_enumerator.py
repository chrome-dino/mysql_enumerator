import os.path
import mysql_enumerator.mysql_enumerator_constants


class MySqlEnumerator():

    def __init__(self):
        print('!')

    def exfil_table(self, table, schema, cursor):
        sql = "SELECT * FROM " + schema + "." + table
        cursor.execute(sql)
        result = cursor.fetchall()
        return result

    # collect info on all tables in db
    def db_report(self, cursor, admin):
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
            table_query = cursor.fetchall()

            # collect columns for each table
            for y in table_query:
                table = y['table_name']
                sql = "SELECT COLUMN_NAME,DATA_TYPE FROM information_schema.COLUMNS WHERE table_name = '" + table
                columns = cursor.fetchall()
                cols = []

                for z in columns:
                    cols.append({'column': z['COLUMN_NAME'], 'data_type': z['DATA_TYPE']})
                tables.append({'table': table, 'columns': cols})

        db_layout.append({'schema': schema, 'tables': tables})

        final['db_layout'] = db_layout

        # if running in admin mode collect user data
        if admin:
            sql = "SELECT * FROM user"
        users = cursor.fetchall()
        final['users'] = users

        return final


def run():
    if not args.port:
        args.port = 3306

    # admin mode defaults to False if no option is provided


    if args.admin:
        admin = True
    else:
        admin = False
    
        # connect to the databse
    connection = pymysql.connect(host=args.hostname,
                                 user=args.username,
                                 password=args.password,
                                 # db=args.schema,
                                 charset='utf8mb4',
                                 port=args.port,
                                 cursorclass=pymysql.cursors.DictCursor)
    
    try:
        with connection.cursor() as cursor:
            # if table and schema provided output content of table to an excel file
            if args.t:
                for x in str(args.table).split(','):
                    results = exfil_table(x, args.schema, cursor)
                    df = pd.DataFrame(results)
                    df.to_excel(args.t + '.xlsx')
            else:
                # if no table is provided print out details about all tables in the database
                results = db_report(cursor, admin)
                for schema in results['schema']:
                    print('SCHEMA: ' + schema['schema'])
                    print('---------------------------------------------------\n')
                    for table in schema['table']:
                        print('\tTABLE: ' + table)
                        for column in table['column']:
                            print('\t\t' + column['column'] + ": " + column['data_type'])
                        print('\n\n')
    
                # if running in admin mode print out user info
                if admin:
                    df = pd.DataFrame(results['users'])
                    df.to_excel('users.xlsx')
                    print('USERS')
                    print('---------------------------------------------------\n')
                    for user in results['users']:
                        print('\tHOST: ' + user['Host'])
                        print('\tUSER: ' + user['User'])
                        print('\tPASSWORD: ' + user['Password'] + '  EXPIRED: ' + user['password_expired'])
    
                        # print out user privs. Uncomment to display more privs
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
                        # if user['Reload_priv'] == 'Y':
                        #    print('\t\tRELOAD')
                        # if user['Shutdown_priv'] == 'Y':
                        #    print('\t\tSHUTDOWN')
                        # if user['Process_priv'] == 'Y':
                        #    print('\t\tPROCESS')
                        if user['File_priv'] == 'Y':
                            print('\t\tFILE')
                        if user['Grant_priv'] == 'Y':
                            print('\t\tGRANT')
                        # if user['References_priv'] == 'Y':
                        #    print('\t\tREFERENCES')
                        # if user['Index_priv'] == 'Y':
                        #    print('\t\tINDEX')
                        # if user['Alter_priv'] == 'Y':
                        #    print('\t\tALTER')
                        # if user['Show_db_priv'] == 'Y':
                        #    print('\t\tSHOW_DB')
                        if user['Super_priv'] == 'Y':
                            print('\t\tSUPER')
                        # if user['Create_tmp_table_priv'] == 'Y':
                        #    print('\t\tCREATE_TMP_TABLE')
                        # if user['Lock_tables_priv'] == 'Y':
                        #    print('\t\tLOCK_TABLES')
                        # if user['Execute_priv'] == 'Y':
                        #    print('\t\tEXECUTE')
                        # if user['Repl_slave_priv'] == 'Y':
                        #    print('\t\tREPL_SLAVE')
                        # if user['Create_view_priv'] == 'Y':
                        #    print('\t\tCREATE_VIEW')
                        # if user['Show_view_priv'] == 'Y':
                        #    print('\t\tSHOW_VIEW')
                        # if user['Create_routine_priv'] == 'Y':
                        #    print('\t\tCREATE_ROUTINE')
                        # if user['Alter_routine_priv'] == 'Y':
                        #    print('\t\tALTER_ROUTINE')
                        if user['Create_user_priv'] == 'Y':
                            print('\t\tCREATE_USER')
                        # if user['Event_priv'] == 'Y':
                        #    print('\t\tEVENT')
                        # if user['Trigger_priv'] == 'Y':
                        #    print('\t\tTRIGGER')
                        # if user['Create_tablespace_priv'] == 'Y':
                        #    print('\t\tCREATE_TABLESPACE')
                        # if user['Delete_history_priv'] == 'Y':
                        #    print('\t\tDELETE_HISTORY')
    
    
    except pymysql.err.OperationalError:
        print('Unable to make a connection to the mysql database')
    finally:
        connection.close()
    
    
