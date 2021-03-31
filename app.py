from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    #In the next line change USERNAME to your uOttawa login before the @uOttawa.ca and change PASSWORD to your uOttawa password
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://USERNAME:PASSWORD@web0.eecs.uottawa.ca:15432/group_a03_g30' 
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
def index():
    return render_template('index.html')


@app.route('/submit', methods=['POST'])
def submit():
    if request.method == 'POST':
        emp_sin_number = request.form['emp_sin_number']
        first_name = request.form['first_name']
        middle_name = request.form['middle_name']
        last_name = request.form['last_name']
        house_number = request.form['house_number']
        street_name = request.form['street_name']
        postal_code = request.form['postal_code']
        apt_number = request.form['apt_number']
        city = request.form['city']
        country = request.form['country']
        phone_number = request.form['phone_number']
        salary = request.form['salary']

        # print(customer, dealer, rating, comments)
        if emp_sin_number == '' :
            return render_template('index.html', message='Please enter required fields')
        else:
            #data = EmpTable(emp_sin_number, first_name, middle_name, last_name, house_number, street_name, postal_code, apt_number, city, country, phone_number, salary)
            #db.session.add(data)
            #db.session.commit()
            return render_template('success.html')
        #return render_template('index.html', message='You have already submitted!')


if __name__ == '__main__':
    app.run()