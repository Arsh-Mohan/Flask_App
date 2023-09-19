from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Task.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


class Task(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(500),nullable = False)
    Entry_Date = db.Column(db.DateTime,default = datetime.utcnow)
    
    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"
@app.route('/',methods=["GET","POST"])
def hello_world():
    if request.method=='POST':
        title = request.form['title']
        desc = request.form['desc']
        task = Task(title = title,desc=desc)
        db.session.add(task)
        db.session.commit()
    
    alltask = Task.query.all()
    return render_template('index.html',alltask=alltask)


@app.route('/show')
def products():
    alltask = Task.query.all()
    print(alltask)
    return 'this is products page'

@app.route('/update/<int:sno>',methods=["GET","POST"])
def update(sno):
    if request.method=="POST":
        title = request.form['title']
        desc = request.form['desc']
        task = Task.query.filter_by(sno=sno).first()
        task.title = title
        task.desc = desc
        db.session.add(task)
        db.session.commit()
        return redirect("/")
        
    task = Task.query.filter_by(sno=sno).first()
    return render_template('update.html',task=task)

@app.route('/delete/<int:sno>')
def delete(sno): 
    alltask = Task.query.filter_by(sno=sno).first()
    db.session.delete(alltask)
    db.session.commit() 
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        app.run(debug=True, port=8000)