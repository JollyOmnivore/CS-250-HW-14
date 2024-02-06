from flask import *
from flask_sqlalchemy import *
from flask_login import *

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite'
db = SQLAlchemy(app)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80),unique=True)
    password = db.Column(db.String(80))
    name = db.Column(db.String(30))
    age = db.Column(db.Integer)

app.config['SECRET_KEY'] = 'alksdifa;lksdif;alksdifa;lksdifa;lksdfj'
login_manager = LoginManager(app)
login_manager.init_app(app)

@login_manager.user_loader
def load_user(uid):
    user = User.query.filter_by(id=uid).first()
    return user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user is not None and password == user.password:
            login_user(user)
            return redirect('/')
        else:
            return 'FAILURE!'

@app.route ('/secret')
@login_required
def secret():
    return current_user.username + " SUPER AWESOME SECRET!"

@app. route ('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')

@app.route('/', methods=['GET', 'POST'])
def home():
    loggedin = current_user.is_authenticated
    if request.method == 'GET':
        return render_template('home.html', loggedin=loggedin)

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'GET':
        return render_template('create.html')
    elif request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        age = request.form['age']
        if not User.query.filter_by(username=username).all():
            user = User(username=username, password=password, name=name, age=age)
            db.session.add(user)
            db.session.commit()
            login_user(user)
            return redirect('/')
        else:
            return redirect('/create')

@app.route('/view_all', methods=['GET', 'POST'])
@login_required
def view():
    if request.method == 'GET':
        return render_template('view.html', users=User.query.all())


@app.route('/update',methods = ['GET','POST'])
@login_required
def update():
    if request.method == 'GET':
        return render_template('update.html', users=User.query.all())
    elif request.method == 'POST':
        password = request.form['password']
        newpassword = request.form['newpassword']
        user = current_user
        if user.password == password:
            #user = User.query.filter_by(password=password).all()
            user.password = newpassword
            db.session.commit()
            return redirect('/')
        else:
            return redirect('/update')
@app.errorhandler(404)
@app.errorhandler(401)
def functionToRun(err):
    return render_template('errorpage.html', users=User.query.all(), err=err)




if __name__ == '__main__':
  app.run(debug=True)
