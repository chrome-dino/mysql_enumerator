import argparse

def main():
    parser = argparse.ArgumentParser()

    # cmd line args
    
    parser.add_argument("-db", "--hostname", help="database",required=True)
    parser.add_argument("-u", "--username", help="User name",required=True)
    parser.add_argument("-p", "--password", help="Password",required=True)
    parser.add_argument("-port", "--port", help="port", type=int, required=False)
    parser.add_argument("-s", "--schema", help="schema",required=False, required='-t' in sys.argv)
    parser.add_argument("-t", "--table", help="table", required='-s' in sys.argv)
    parser.add_argument("-a", "--admin", help="admin mode", required=False, nargs='?', const='',default='')

    args = parser.parse_args()
    
if __name__ == "__main__":
    main()
