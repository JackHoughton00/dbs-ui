from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    # In the next line change USERNAME to your uOttawa login before the @uOttawa.ca and change PASSWORD to your
    # uOttawa password
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://USERNAME:PASSWORD@web0.eecs.uottawa.ca:15432/group_a03_g30'
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

rooms = db.Table('room', db.metadata, autoload=True, autoload_with=db.engine, schema='hoteldbs')


#
# Base = automap_base()
# Base.prepare(db.engine,reflect =True)
# #Rooms = Base.classes.rooms
#
#
# class Rooms(Base):
#     __tablename__ = 'room'
#     __table_args__ = {'schema': 'hoteldbs'}
#
#
# class EmpTable(Base):
#     __tablename__ = 'employee'
#     #below line of code will be how you direct the table to the right schema in the database on postrgre.
#     __table_args__ = {'schema':'hoteldbs'}
#     emp_sin_number = db.Column(db.Integer, primary_key=True)
#     first_name = db.Column(db.String(50))
#     middle_name = db.Column(db.String(50))
#     last_name = db.Column(db.String(50))
#     house_number = db.Column(db.String(50))
#     street_name = db.Column(db.String(50))
#     postal_code = db.Column(db.String(50))
#     apt_number = db.Column(db.String(50))
#     city = db.Column(db.String(50))
#     country = db.Column(db.String(50))
#     phone_number = db.Column(db.String(50))
#     salary = db.Column(db.String(50))
#
#
#
#     def __init__(self, emp_sin_number, first_name, middle_name, last_name, house_number, street_name, postal_code, apt_number, city, country, phone_number, salary):
#         self.emp_sin_number = emp_sin_number
#         self.first_name = first_name
#         self.middle_name = middle_name
#         self.last_name = last_name
#         self.house_number = house_number
#         self.street_name = street_name
#         self.postal_code = postal_code
#         self.apt_number = apt_number
#         self.city = city
#         self.country = country
#         self.phone_number = postal_code
#         self.salary = salary


# Handling requests that are applicible throughout the entirety of the web app
@app.route('/backHome', methods=['POST'])
def backHome():
    if request.method == 'POST':
        return render_template('homePage.html')


# Handling requests that are applicable on the home page of the web app.
@app.route('/')
def homePage():
    return render_template('homePage.html')


@app.route('/homeSubmit', methods=['POST'])
def submit():
    if request.method == 'POST':
        role = request.form['role']

        if role == 'customer':
            return render_template('customerSearchPage.html')
        elif role == 'employee':
            return render_template('employeeSearchPage.html')
        elif role == 'admin':
            return render_template('homePage.html', message='You do not have permission for this. ')
        else:
            return render_template('homePage.html',
                                   message='You did not select a role. Please select a role before submitting.')


# Handling requests on the customer side of the web app
@app.route('/customerToBooking', methods=['POST'])
def customerToBooking():
    if request.method == 'POST':
        return render_template('customerBookingPage.html')


@app.route('/customerBackToSearch', methods=['POST'])
def customerToSearch():
    if request.method == 'POST':
        return render_template('customerSearchPage.html')


@app.route('/customerFinishBooking', methods=['POST'])
def customerFinishBooking():
    if request.method == 'POST':
        return render_template('customerBookingPage.html', message='Not yet implemented!!!!!!!')


@app.route('/customerSearchRooms', methods=['POST'])
def customerSearchRooms():
    result = db.session.query(rooms).all()
    for r in result:
        print(r)
    return render_template('customerSearchPage.html')


# Handling requests on the employee side of the web app
@app.route('/employeeToBooking', methods=['POST'])
def employeeToBooking():
    if request.method == 'POST':
        return render_template('employeeBookingPage.html')


@app.route('/employeeBackToSearch', methods=['POST'])
def employeeToSearch():
    if request.method == 'POST':
        return render_template('employeeSearchPage.html')


@app.route('/employeeFinishBooking', methods=['POST'])
def employeeFinishBooking():
    if request.method == 'POST':
        return render_template('employeeBookingPage.html', message="Not yet implimented!!!!!")


if __name__ == '__main__':
    app.run()
