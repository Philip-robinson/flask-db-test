from flask import Flask, render_template
import database


pf = database.Portfolio()

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    """ Home page - a list of companies 
        using the templates templates/index.html """
    return render_template('index.html',
        title='Company display',
        shares=pf.names())
                             
@app.route('/detail/<name>')
def detail(name):
    """ Details page - a list of information about 1 company 
        using the templates templates/detail.html """
    print("Got name "+name) 
    print("Deatil is ", pf.detail(name))
    ret = pf.detail(name)
    return render_template('detail.html',
        title='Share display for '+name,
        detail=ret)

@app.route("/api/shares")
def companies():
    """ A list of companies as json """
    print("List of shares owned in portfolio")
    return {"shares": pf.names()}

@app.route("/api/share/detail/<name>")
def company(name):
    """ The details of one company (as specified by name)
        as json """
    print("detail of shares owned for ", name)
    ret = pf.detail(name)
    return ret

# start the application on port 8010
app.run(port=8010)
