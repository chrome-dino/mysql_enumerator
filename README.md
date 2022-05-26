# mysql_enumerator 

Mysql_enumerator is a tool that can be used to evaluate the security posture of a MySQL database. The tool allows for a user to understand the layout of the database by outputting an organized report of the different schemas and tables. The tool can be used both in an offensive or defensive role, whether it is to evaluate the attack surface of the database or to extract information from it. 


## Table of Contents
* <a href="#key-features">Key Features</a></br>
* <a href="#installation">Installation</a></br>
* <a href="#how-to-use">How To Use</a> </br>
* <a href="#notes">Notes</a></br>
* <a href="#license">License</a>


## Key Features

* Build a detailed report on the layout of the database
* Collect information on database users and their associated permissions
* Can operate with a user with limited permissions  
* Extract tables from the database and export them to an excel file


## Installation

```bash
# Clone this repository
$ git clone https://github.com/chrome-dino/mysql_enumerator.git

# From the directory containing your git projects
$ pip install -e mysql_enumerator
```

Uses the following non standard libraries:
* pandas
* pymysql
* setuptools
* cryptography
* openpyxl


## How To Use

### Help Menu

```bash
# Install dependencies
$ npm install

# Run the app
$ npm start
```

### Video



### Examples

```bash
# run the report generator with a standard user
$ py -m mysql_enumerator -db hostname -u user -p password

# run the report generator with elevated permissions and extract info on database users
$ py -m mysql_enumerator -db hostname -u root -p password -a

# extract the rows from a table
$ py -m mysql_enumerator -db hostname -u user -p password -s schema_name -t table_name1,table_name2
```


## Notes

* Tested on python 3.10.4


## License

MIT
