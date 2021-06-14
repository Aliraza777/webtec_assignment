from flask import Flask
from flask import render_template
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import session
from datetime import datetime
from flask import redirect, url_for
import sqlite3 as sql


app = Flask(__name__)


@app.route('/add')
def new_student():
   return render_template('student.html')


# added remove functionality-------
# function to remove an entry
@app.route('/remove/<id>',methods = ['POST', 'GET'])
def removerec(id):
   if request.method == 'POST':
      con = sql.connect("database.db")
      try:
         # get_id = request.form['id']
         with sql.connect("database.db") as con:
            cur = con.cursor()
            cur.execute("DELETE FROM students WHERE id  = ? ", (id ,))
            con.commit()
            msg = "Record Deleted"
      except:
         con.rollback()
         msg = "Error in Deleting operation"
      
      finally:
         return render_template("removeStudent.html",msg = msg )
         con.close()

@app.route('/newrecord',methods = ['POST', 'GET'])
def addrec():
   if request.method == 'POST':
      con = sql.connect("database.db")
      try:
         nm = request.form['nm']
         addr = request.form['add']
         city = request.form['city']
         pin = request.form['pin']
         with sql.connect("database.db") as con:            
            cur = con.cursor()
            cur.execute("INSERT INTO students (name,addr,city,pin) VALUES (?,?,?,?)",(nm,addr,city,pin) )
            con.commit()
            msg = "Record successfully added"
      except:
         con.rollback()
         msg = "error in insert operation"
      
      finally:
         return render_template("result.html",msg = msg)
         con.close()


@app.route('/list')
def list():
   con = sql.connect("database.db")
   con.row_factory = sql.Row
   cur = con.cursor()
   cur.execute("select * from students")
   rows = cur.fetchall(); 
   # breakpoint()
   return render_template("list.html",rows = rows)


@app.route('/')
def home():
   return render_template('home.html')


if __name__ == '__main__':
   app.run(debug = True)


#### create table 

# import sqlite3

# conn = sqlite3.connect('database.db')
# print "Opened database successfully";

# conn.execute('CREATE TABLE students (name TEXT, addr TEXT, city TEXT, pin TEXT)')
# print "Table created successfully";
# conn.close()