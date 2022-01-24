#importing the libraries

from flask import Flask, render_template,redirect,request
from flask_sqlalchemy import SQLAlchemy

#initiating app and database
app=Flask("__name__")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db=SQLAlchemy(app)


#creating database class
class Task_item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(300), nullable=False)
    #to show a task
    def __rep__(self):
        return '<Task %r>' % self.id

db.create_all()

@app.route('/',methods=['POST','GET'])
def home():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Task_item(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an error while adding the task'

    else:
        tasks = Task_item.query.all()
        return render_template("index.html", tasks=tasks)

#for deleting

@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete = Task_item.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an error while deleting that task'

#for updating

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    task = Task_item.query.get_or_404(id)

    if request.method == 'POST':
        task.content = request.form['content']

        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue while updating that task'

    else:
        return render_template('update.html', task=task)

if __name__=="__main__":
    app.run(debug=True)