from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    #In the next line change USERNAME to your uOttawa login before the @uOttawa.ca and change PASSWORD to your uOttawa password
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://USERNAME@:PASSWORD@web0.eecs.uottawa.ca:15432/group_a03_g30' 
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class TestTable(db.Model): 
    #__tablename__ = 'testtableplswork'
    __table_args__ = {'schema':'hoteldbs'}
    age = db.Column(db.Integer,primary_key = True)

    def __init__(self, age):
        self.age = age


class EmpTable(db.Model):
    __tablename__ = 'employee'
    #below line of code will be how you direct the table to the right schema in the database on postrgre. 
    __table_args__ = {'schema':'hoteldbs'}
    emp_sin_number = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50))
    middle_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    house_number = db.Column(db.String(50))
    street_name = db.Column(db.String(50))
    postal_code = db.Column(db.String(50))
    apt_number = db.Column(db.String(50))
    city = db.Column(db.String(50))
    country = db.Column(db.String(50))
    phone_number = db.Column(db.String(50))
    salary = db.Column(db.String(50))
    


    def __init__(self, emp_sin_number, first_name, middle_name, last_name, house_number, street_name, postal_code, apt_number, city, country, phone_number, salary):
        self.emp_sin_number = emp_sin_number
        self.first_name = first_name
        self.middle_name = middle_name
        self.last_name = last_name
        self.house_number = house_number
        self.street_name = street_name
        self.postal_code = postal_code
        self.apt_number = apt_number
        self.city = city
        self.country = country
        self.phone_number = postal_code
        self.salary = salary 


@app.route('/')
def homePage():
    return render_template('homePage.html')


@app.route('/homeSubmit', methods=['POST'])
def submit():
    if request.method == 'POST':
        role = request.form['role']

        if role == 'customer':
            return render_template('customerPage.html')
        elif role == 'employee':
            return render_template('employeePage.html')
        elif role == 'admin':
            return render_template('homePage.html', message = 'You do not have permission for this. ')
        else: 
            return render_template('homePage.html', message = 'You did not select a role. Please select a role before submitting.')




        

if __name__ == '__main__':
    app.run()