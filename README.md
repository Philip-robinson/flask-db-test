# Flask test

This is a very simple application, it produces a web interface
and API on data read from a qlite database.

It relates to displaying information about a portfolio of shares
presented in that database.

you need to have python3 python3-venv and flask installed

python3 and python3-venv are both os level installations
flask can be installed with pip

On ubuntu:
```
sudo apt-get install python3
sudo apt-get install python3-venv
```

Standard process is to create a virtual invironment, this is I think not 
necessary but allows an application to be run in isolation from other
applications 

You create the the virtual environment inside the directory
in which youy are to create the code.

```
python3 -m venv venv
```

And actrivate it with
```
source venv/bin/activate
```
microsoft equivalent

```
venv\\Scripts\\activate
```

You can now install flask into this virtual environment (venv)

```
pip install flask
```
## Database initialisation

The database is initialised using the python file __init_db.py__.

This creates the tables using SQL and then inserts rows into those tables also using sql.

```
curs = con.cursor()
curs.executemany("INSERT INTO shares(name) VALUES (?)",[s
     ("Ashtead Group PLC (LSE:AHT)",),
     ("BHP Group PLC (LSE:BHP)",),
...
     ("SThree PLC (LSE:STEM)",),
     ("Telefonica Deutschland Holding AG (XETRA:O2D)",),
     ("Tesco PLC (LSE:TSCO)",)])
```
__executmany__ executes a single sql statement many times with different parameters provided, the
parameters are provided as a list of typles the trailing comma in __("BHP Group PLC (LSE:BHP)",)__ is present
to ensure that the parameters tuple is seen as a tuple rather than a string.
```
curs.executemany("INSERT INTO prices(share_id, price) VALUES (?, ?)", [
    (con.execute("select id from shares where name=?", ("Ashtead Group PLC (LSE:AHT)",)).fetchone()[0], "60.58"),
...
    (con.execute("select id from shares where name=?", ("SThree PLC (LSE:STEM)",)).fetchone()[0], "4.31"),
    (con.execute("select id from shares where name=?", ("Telefonica Deutschland Holding AG (XETRA:O2D)",)).fetchone()[0], "2.458")])
```
The section con.execute("select id from shares where name=?", ("Telefonica Deutschland Holding AG (XETRA:O2D)",)

is intended to get the id of the share entry with the given name.

```
con.commit()
con.close()
```

Then commit and close the session

So we now have a database and can go on to extract data from it and display it on a website


## The application

If you have examined the flask-test application you will recognise this as it is very similar
:x
vi in	 though not exactly the same as the database has slightly different data.
There are five files:
* __database.py__ 
* __index.py__
* __templates/index.html__
* __templates/details.html__
* __static/style.css__

### static files style.css

files put in the static directory are automatically made available
as stored.

the file __static/style.css__ can be accessed in this application
as __http://localhost:8010/static/style.css__

### template files stored under templates

the directory __templates__ is where template files are expected to be found

there are two in this is a fairly standard style of template using {{field}}
and {% some code %} style of modifying the code.

### database.py

This file contains a class that reads the database 

### index.py

This is the file that is the controler (in mvc style) it contains
4 functions 2 of which produce web pages and two are
API end points producing json.

After these have been created the server is started on port 8010.

__index.py__ can be executed:

```
python index.py
```

