from flask import Flask,request, url_for, redirect, render_template,session
import pickle
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)

model=pickle.load(open('model.pkl','rb'))


app.secret_key = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/')
def hello_world():
    return render_template("home1.html")


@app.route('/predict',methods=['POST','GET'])
def predict():
    int_features=[int(x) for x in request.form.values()]
    final=[np.array(int_features)]
    print(int_features)
    print(final)
    prediction=model.predict(final)
    #output='{0:.{1}f}'.format(prediction[0][1], 2)
    output = str(prediction)
    if output>str(0.5):
        return render_template('index.html',pred='Your Forest is in Danger.\nProbability of fire occuring is {}'.format(output))
    else:
        return render_template('index.html',pred='Your Forest is safe.\n Probability of fire occuring is {}'.format(output))
@app.route('/login')
def login():
     return render_template('login.html')
@app.route('/register_data', methods=['POST'])
def register_data():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/index')
def index():
    return render_template('index.html')
@app.route('/login_data', methods=['POST'])
def login_data():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)