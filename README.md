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
That is you can have different environments with different versions of
python and different versions of libraries installed.

You create the the virtual environment inside any directory
where you wish to store the environment data.


```
python3 -m venv venv
```

And actrivate it with (linux style)
```
source venv/bin/activate
```
Or Microsoft style
```
venv\\Scripts\\activate
```

You can now install flask into this virtual environment (venv)

```
pip install flask
```

pip will install into the currently set venv.

Intellij and pyCharm both allow the selection of a venv or
creation of a new one when a Python project is created.

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

Files put in the static directory are automatically made available
as stored.

The file __static/style.css__ can be accessed in this application
as __http://localhost:8010/static/style.css__

### template files stored under templates

the directory __templates__ is where template files are expected to be found

There are two in this project, one for each of the displayed pages.

For the home page we have __templates/index.html__ which looks like:
```
<html>
    <head>
        <title>{{ title }}</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body>
        <table>
        {% for share in shares: %}
                <tr><td><a href="/detail/{{share.id}}">{{ share.name }}</a></td></tr>
        {% endfor %}
        </table>
    </body>
</html>
```
A fairly standard syntax, perhaps a bit old fashined but works well:

__{{ url_for('static', filename='style.css') }}__

specifies the url to style.css in the static directory and is converted to
__/static/style.css__ but may look different if the app had been configured differently.

The other __templates/detail.html__ is similar.
```
<html>
    <head>
        <title>{{ title }}</title>
        <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}">
    </head>
    <body>
 
       <h1>Details 0f {{detail.name}}</h1>
       <a href="/index">Home</a>
        <table>
                <tr><td>Shares held</td><td>{{detail.number}}</td></tr>
                <tr><td>Price per share</td><td>£{{detail.price}}</td></tr>
                <tr><td>Total value</td><td>£{{detail.value}}</td></tr>
                <tr><td>Cost</td><td>£{{'%02.f'|format(detail.cost)|float}}</td></tr>
                {% if detail.profit <  0 : %}
                    <tr><td>Profit</td><td>-£{{'%0.2f'|format(0.0-detail.profit)|float}}</td></tr>
                {% else: %}
                    <tr><td>Profit</td><td>£{{'%0.2f'|format(detail.profit)|float}}</td></tr>
                {% endif %}
        </table>
       <a href="/index">Home</a>
    </body>
</html>
```
 This takes two parameters __title__ which is a title and __detail__ which is a dict
holding the fields to be displayed.

the somewaht complicated looking pipeline __'%0.2f'|format(detail.profit)|float__ formats
the detail.profit value to have 2 digits after the decimal point.

### database.py

This file contains a class __Portfolio__ that reads the portfolio related data from
the database. the database is __sqlite3__ and contained in a file called __shares.db__.


```
import sqlite3

def getCon():
    return sqlite3.connect("shares.db")

class Portfolio:

```
 The function __getCon__ creates a connection to the database.
 

There are two methods in the Portfolio class which extract that data.

```
    def names(self):
        con = getCon()
        cur = con.cursor()
        res =  cur.execute("SELECT id, name FROM shares").fetchall()
        con.close()
        return [{"id": row[0], "name": row[1]} for row in res];
```
These database access methods all start with getting a connection and finish with closing that connection.

This returns a list of names of shares, the reason for the list __"Comprehension"__ is because
the database query returns a list of tuples, passing a list of dicts is more robust, other parts
of the code just need to know field names rather than obtain values from their position in
the tuple.

The other method is much bigger becaus we are processing a join between multiple tables:
```
    def detail(self, id):
        con = getCon()
        cur = con.cursor()
        price, name, number, cost = cur.execute("""
                          SELECT p.price, s.name, sum(t.number), sum(cost)
                          FROM shares s
                          LEFT JOIN transactions t ON s.id = t.share_id
                          LEFT JOIN prices p ON p.share_id=s.id
                          WHERE s.id=? 
                          AND NOT EXISTS(
                              SELECT * 
                              FROM prices p2
                              WHERE p2.id > p.id
                              AND p2.share_id=p.share_id)
                          GROUP BY p.price
                          """, (id,)).fetchone()
        if number is None:
            number=0
        con.close()
        if cost is None:
            cost=0
        con.close()
        if price is None:
            price=0
        con.close()
        return{"price": price,
               "name": name,
               "number": number,
               "cost": cost,
               "value": price*number,
               "profit": price*number-cost
        }
```

The query is so big because it:
* Selects a share (to get the name).
* Joins on all the related share transactions (buying and selling) so the
	number of shares iand prices can be summed to get a total cost.
* The latest share price to get the current value.

As some of these fields may come out of the query blank (None) they are tested for having
None as their value and changed to 0.

Then a dict is constructed.


### index.py

This is the file that is the controler (in an MVC way) it contains
4 functions 2 of which produce web pages and two of which are
API end points producing json.

These are very simple, and what I like is that like Spring in the java world the urls are
in the same place as the code.

```
app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    """ Home page - a list of companies
        using the templates templates/index.html """
    return render_template('index.html',
        title='Company display',
        companies=pf.names())
```
This function takes the template __templates/index.html__ and populates it with data
two routes are specified / and /index, the render template method is given named parameters
which are then made available to the template.

Very neat.

Another method returns Json/REST API style:
```
@app.route("/api/shares")
def companies():
    """ A list of companies as json """
    print("List of shares owned in portfolio")
    return {"shares": pf.names()}
```

After these have been created the server is started on port 8010.
```
app.run(host="0.0.0.0", port=8010)
```

This is I believe for testing purposes only and there is another mechanism
to run the app for production use.

__index.py__ can be executed:

```
python index.py
```

