from flask import Flask, render_template, url_for, request, redirect
from flask.helpers import flash
from form import Todo
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.secret_key = 'secretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'


db = SQLAlchemy(app)

class Todos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), index=True)


@app.route('/', methods=['GET', 'POST'])
def home():
    form = Todo()
    if request.method == 'POST':
        name = form.text.data
        dle = Todos.query.filter(Todos.name == name).first()
        if dle:
            flash('This Todo is already in the TodoList!')
        else:
            db.session.add(Todos(name=name))
            db.session.commit()
    return render_template('index.html', form=form, title='My Todo List', mytodos=Todos.query.all())


@app.route('/delete/<int:id>')
def delete(id):
    dle = Todos.query.get_or_404(id)
    try:
        db.session.delete(dle)
        db.session.commit()
        return redirect(url_for('home'))
    except:
        return flash('Something went wrong.')

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    item = Todos.query.get_or_404(id)
    if request.method == 'POST':
        try:
            item.name = request.form['name']
            db.session.commit()
            return redirect(url_for('home'))
        except:
            return 'Something went wrong'
    else:
        return render_template('update.html', item=item)
if __name__ == "__main__":
    app.run(debug=True)
