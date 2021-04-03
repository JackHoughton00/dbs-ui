from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.ext.automap import automap_base
import datetime

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    # In the next line change USERNAME to your uOttawa login before the @uOttawa.ca and change PASSWORD to your
    # uOttawa password
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://USER:PASS@web0.eecs.uottawa.ca:15432/group_a03_g30'
       
else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

rooms = db.Table('room', db.metadata, autoload=True, autoload_with=db.engine, schema='hoteldbs')

rooms_hotel_chain = db.Table('room_hotel_chain', db.metadata, autoload=True, autoload_with=db.engine, schema='hoteldbs')


hotel_chain = db.Table('hotel_chain',db.metadata,autoload = True, autoload_with=db.engine, schema = 'hoteldbs')


# Base = automap_base()
# Base.prepare(db.engine,  reflect =True, schema = 'hoteldbs')
# #Rooms = Base.classes.rooms
# #RoomHotelChain = Base.classes.room_hotel_chain
# RoomHC = Base.classes.room_hotel_chain 

 
# class Room_hotel_chain(db.Model):
#     __tablename__ = 'room_hotel_chain'
#     __table_args__ = {'schema': 'hoteldbs'}

#     room_number = db.Column(db.Integer, primary_key = True)
#     hotel_id = db.Column(db.Integer)

#     def __init__(self, room_number,hotel_id):
#         self.room_number = room_number
#         self.hotel_id = hotel_id





# class Rooms(Base):
#     __tablename__ = 'room'
#     __table_args__ = {'schema': 'hoteldbs'}

#     room_number = db.Column(db.Integer, primary_key = True)
#     price = db.Column(db.Double)
#     date_available 



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
    result = db.session.query(hotel_chain.c.city)
    
    itemsList = set()
    for r in result:
        itemsList.add(r[0])

    itemsList = sorted(itemsList)

    print(itemsList)
    if request.method == 'POST':
        role = request.form['role']

        if role == 'customer':
            return render_template('customerSearchPage.html', items=itemsList)
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



# CUSTOMER SEARCH ROOMS SHOULD BE HERE
@app.route('/customerSearchRooms', methods=['POST'])
def customerSearchRooms():


    cityList = db.session.query(hotel_chain.c.city)
    
    itemsList = set()
    for city in cityList:
        itemsList.add(city[0])

    itemsList = sorted(itemsList)

    if request.method == 'POST':
        cityName = request.form['citySelect']
        bookingDate = request.form['startDate']

        if cityName == 'Los angeles':
            cityName = 'Los Angeles'
        elif cityName == 'Rio de janeiro':
            cityName = 'Rio de Janeiro'
        elif cityName == 'New yorkcity':
            cityName = 'New York City'
        elif cityName == 'San jose':
            cityName = 'San Jose'
        
        cityName = cityName.capitalize()
    
        if cityName == '' or bookingDate == '' or cityName=='holder':
            return render_template('customerSearchPage.html', message = 'Either cityName or bookingDate is null.', items = itemsList )
        else:
            
            year = int(bookingDate[0:4])
            month = int(bookingDate[5:7])
            day = int(bookingDate[8:])
            dateTimeFormatted = datetime.datetime(year, month ,day, 0, 0 )
            result = db.session.query(rooms_hotel_chain,rooms,rooms,hotel_chain).select_from(rooms).join(rooms_hotel_chain).join(hotel_chain).filter(
                hotel_chain.c.city == cityName and datetime(rooms.c.date_available) <= dateTimeFormatted).order_by(rooms.c.room_number.asc())
            finalResult = []   
            for r in result:
                tmpList = [] 
                x = r[4]
                if x <= dateTimeFormatted:
                    tmpR3 = str(r[3])
                    tmpR6 = str(r[6])
                    tmpR7 = str(r[7])
                    tmpR0 = str(r[0])

                    tmpList.append('Price: '+tmpR3)
                    tmpList.append('View Type: '+ tmpR6)
                    tmpList.append('Amenities: '+ tmpR7) 
                    tmpList.append('Room Number: '+ tmpR0)
                    finalResult.append(tmpList)
                    print(r)
            return render_template('customerSearchPage.html',items = itemsList, results = result, roomDetails = finalResult)


@app.route('/customerFinishBooking', methods=['POST'])
def customerFinishBooking():
    if request.method == 'POST':

        cusSINNum = request.form['customerSIN']
        cusFirstName = request.form['customerFirstName']
        cusMiddleName = request.form['customerMiddleName']
        cusLastName = request.form['customerLastName']
        cusHouseNum = request.form['customerHouseNumber']
        cusStreetName = request.form['customerStreetName']
        cusPostalCode = request.form['customerPostalCode']
        cusAptNum = request.form['customerApartmentNumber']        
        cusCityName = request.form['customerCity']
        cusCountryName = request.form['customerCountry']
        cusProvinceName = request.form['customerProvince']
        cusPhoneNumber = request.form['customerPhoneNumber'] 

        if cusSINNum == '' or cusFirstName == '' or cusLastName == '' or cusHouseNum == '' or cusStreetName == '' or cusCityName == '' or cusCountryName == '' or cusPostalCode == '' or cusPhoneNumber == '': 
            return render_template('customerBookingPage.html', message = 'One or more of your required fields are empty, please try again')

        return render_template('customerBookingPage.html')


    



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
