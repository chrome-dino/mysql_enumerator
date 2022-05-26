import argparse
import mysql_enumerator
import sys

def main():
    parser = argparse.ArgumentParser()

    # cmd line args
    
    parser.add_argument("-db", "--hostname", help="IP address or hostname of the target database",required=True)
    parser.add_argument("-u", "--username", help="Login username",required=True)
    parser.add_argument("-p", "--password", help="Login Password",required=True)
    parser.add_argument("-port", "--port", help="Port number (Defaults to 3306)", type=int, required=False)
    parser.add_argument("-s", "--schema", help="Name of the schema to be used in table extraction mode. Requires the table option",required='-t' in sys.argv)
    parser.add_argument("-t", "--table", help="Name of the table to be used in table extraction mode. Requires the schema option", required='-s' in sys.argv)
    parser.add_argument("-a", "--admin", help="Enable admin mode to extract database user info. Requires admin credentials", action=argparse.BooleanOptionalAction)
    parser.add_argument("-v", "--verbose", help="List additional details in the user report", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    
    mysql_enum = mysql_enumerator.MySqlEnumerator(hostname=args.hostname, username=args.username,
    password=args.password, port=args.port, schema=args.schema, table=args.table, admin=args.admin, verbose=args.verbose)
    mysql_enum.run()
    
if __name__ == "__main__":
    main()
