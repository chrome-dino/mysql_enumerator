import argparse
import mysql_enumerator
import sys

def main():
    parser = argparse.ArgumentParser()

    # cmd line args
    
    parser.add_argument("-db", "--hostname", help="database",required=True)
    parser.add_argument("-u", "--username", help="User name",required=True)
    parser.add_argument("-p", "--password", help="Password",required=True)
    parser.add_argument("-port", "--port", help="port", type=int, required=False)
    parser.add_argument("-s", "--schema", help="schema",required='-t' in sys.argv)
    parser.add_argument("-t", "--table", help="table", required='-s' in sys.argv)
    parser.add_argument("-a", "--admin", help="admin mode", action=argparse.BooleanOptionalAction)
    parser.add_argument("-v", "--verbose", help="verbose", action=argparse.BooleanOptionalAction)

    args = parser.parse_args()
    
    mysql_enum = mysql_enumerator.MySqlEnumerator(hostname=args.hostname, username=args.username,
    password=args.password, port=args.port, schema=args.schema, table=args.table, admin=args.admin, verbose=args.verbose)
    mysql_enum.run()
    
if __name__ == "__main__":
    main()
