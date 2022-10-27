## /1/ import flask ando some libraries

from flask import Flask, render_template, request, redirect, url_for



## /4/ import sqlalchemy for DB

from flask_sqlalchemy import SQLAlchemy



## /2/ create app instance 

app = Flask(__name__)



## /5/ set sqlalchemy congfiguartion variables

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app) 



## /6/ create todo model db

class Todo(db.Model):
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100))
	complete = db.Column(db.Boolean)



## /7/ call create_all

with app.app_context():
    db.create_all()
 


## /3/ def home function 

@app.get("/")
def home():
	todo_list = db.session.query(Todo).all()
	return render_template("base.html", todo_list=todo_list)



## /8/ def add function

@app.post("/add")
def add():
	title = request.form.get("title")
	new_todo = Todo(title=title, complete=False)
	db.session.add(new_todo)
	db.session.commit()
	return redirect(url_for("home"))



## /9/ def update fucntion

@app.get("/update/<int:todo_id>")
def update(todo_id):
	todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
	todo.complete = not todo.complete
	db.session.commit()
	return redirect(url_for("home"))



## /10/ def delete fucntion

@app.get("/delete/<int:todo_id>")
def delete(todo_id):
	todo = db.session.query(Todo).filter(Todo.id == todo_id).first()
	db.session.delete(todo)
	db.session.commit()
	return redirect(url_for("home"))
