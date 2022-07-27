from unittest import result
from flask import Flask, render_template, request, redirect,jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123@localhost/flasksql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()
        
    allTodo = Todo.query.all() 
    return render_template('index.html', allTodo=allTodo)

@app.route('/show')
def products():
    allTodo = Todo.query.all()
    print(allTodo)
    return 'this is products page'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
        
    todo = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo = Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/armstrong/<int:n>')
def armstrong(n):
    sum=0
    order=len(str(n))
    copy_n=n
    while (n>0):
        digit=n%10
        sum +=digit **order
        n = n//10
    if (sum == copy_n):
        print(f"{copy_n} is a armstrong number")
        result={
            "Number":copy_n,
            "Armstrong": True
            
        }
    else:
        print(f"{copy_n} is not a armstrong number")
        result={
            " Input Number":copy_n,
            "Armstrong": False,
            "List of Armstrong Nos are":[1, 2, 3, 4, 5, 6, 7, 8, 9, 153, 370, 371, 407, 1634, 8208, 9474, 54748]
        }
    return jsonify(result)


if __name__ == "__main__":
    db.create_all()
    app.run(debug=True, port=8000)