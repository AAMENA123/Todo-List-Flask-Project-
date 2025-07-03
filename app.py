from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db =  SQLAlchemy(app)

class Todo(db.Model):
    sno = db.Column(db.Integer, primary_key = True)
    title =  db.Column(db.String(200), nullable = False )
    desc =  db.Column(db.String(500), nullable = False)
    date_created =  db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/', methods =['GET','POST'])
def hello():
    if request.method =='POST':
        title =request.form['title']
        desc =request.form['desc']
        # desc =request.form['desc']
        todo = Todo(title = title, desc = desc)
        db.session.add(todo)
        db.session.commit()
    alltodos = Todo.query.all()
    return render_template('index.html', alltodos = alltodos)

@app.route('/delete/<int:sno>')
def delete(sno):
  alltodo = Todo.query.filter_by(sno=sno).first()
  db.session.delete(alltodo)
  db.session.commit()
  return redirect('/')

@app.route('/update/<int:sno>',methods =['GET', 'POST'])
def update(sno):
    alltodo = Todo.query.filter_by(sno=sno).first()
    print(alltodo)
    if request.method == 'POST':        
        title = request.form['title']
        desc = request.form['desc']
        alltodo.title = title
        alltodo.desc = desc
        print(alltodo)
        # db.session.add(todo)
        db.session.commit()
        a ="done"
        print("done")
        return redirect(url_for('update',a=a,sno=sno,alltodo=alltodo)) 
    print("flowers are red")  
    a = request.args.get('a')
    return render_template('update.html',alltodo=alltodo,a=a)
        # db.session.commit()
    

if __name__ == "__main__":
    app.run (debug =True)