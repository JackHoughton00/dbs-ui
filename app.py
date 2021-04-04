import random
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
import datetime
from sqlalchemy.ext.declarative import declarative_base

app = Flask(__name__)

ENV = 'dev'

if ENV == 'dev':
    app.debug = True
    # In the next line change USERNAME to your uOttawa login before the @uOttawa.ca and change PASSWORD to your
    # uOttawa password
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgresql://jhoug049:EightExtended8ex@web0.eecs.uottawa.ca:15432/group_a03_g30'

else:
    app.debug = False
    app.config['SQLALCHEMY_DATABASE_URI'] = ''

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

rooms = db.Table('room', db.metadata, autoload=True, autoload_with=db.engine, schema='hoteldbs')

rooms_hotel_chain = db.Table('room_hotel_chain', db.metadata, autoload=True, autoload_with=db.engine, schema='hoteldbs')

hotel_chain = db.Table('hotel_chain', db.metadata, autoload=True, autoload_with=db.engine, schema='hoteldbs')

booking = db.Table('booking', db.metadata, autoload = True, autoload_with=db.engine, schema='hoteldbs')

makes = db.Table('makes', db.metadata, autoload = True, autoload_with=db.engine, schema='hoteldbs')

customer = db.Table('customer', db.metadata, autoload = True, autoload_with=db.engine, schema='hoteldbs')

Base = declarative_base()




class Rooms(Base):
    __tablename__ = 'room'
    __table_args__ = {'schema': 'hoteldbs', 'extend_existing': True}
    room_number = db.Column(db.Integer, primary_key=True)
    price = db.Column(db.NUMERIC)
    date_available = db.Column(db.DateTime)
    room_capacity = db.Column(db.VARCHAR(50))
    view_type = db.Column(db.VARCHAR(50))
    amenities = db.Column(db.VARCHAR(50))
    extendable = db.Column(db.BOOLEAN)


class Booking_Room(Base):
    __tablename__ = 'booking_room'
    __table_args__ = {'schema': 'hoteldbs', 'extend_existing': True}
    booking_number = db.Column(db.Integer, primary_key=True)
    room_number = db.Column(db.Integer, primary_key=True)


class Booking(Base):
    __tablename__ = 'booking'
    __table_args__ = {'schema': 'hoteldbs', 'extend_existing': True}
    booking_number = db.Column(db.Integer, primary_key=True)
    room_type = db.Column(db.VARCHAR(50))
    number_occupants = db.Column(db.Integer)
    renting = db.Column(db.BOOLEAN)
    check_in_date = db.Column(db.DateTime)
    check_out_date = db.Column(db.DateTime)
    total_price = db.Column(db.NUMERIC)


class Employee(Base):
    __tablename__ = 'employee'
    __table_args__ = {'schema': 'hoteldbs', 'extend_existing': True}
    cust_sin_number = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(50))
    middle_name = db.Column(db.VARCHAR(50))
    last_name = db.Column(db.VARCHAR(50))
    house_number = db.Column(db.VARCHAR(50))
    street_name = db.Column(db.VARCHAR(50))
    postal_code = db.Column(db.VARCHAR(50))
    apt_number = db.Column(db.VARCHAR(50))
    city = db.Column(db.VARCHAR(50))
    country = db.Column(db.VARCHAR(50))
    phone_number = db.Column(db.VARCHAR(50))
    salary = db.Column(db.NUMERIC)


class Customer(Base):
    __tablename__ = 'customer'
    __table_args__ = {'schema': 'hoteldbs', 'extend_existing': True}
    cust_sin_number = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.VARCHAR(50))
    middle_name = db.Column(db.VARCHAR(50))
    last_name = db.Column(db.VARCHAR(50))
    house_number = db.Column(db.VARCHAR(50))
    street_name = db.Column(db.VARCHAR(50))
    postal_code = db.Column(db.VARCHAR(50))
    apt_number = db.Column(db.VARCHAR(50))
    city = db.Column(db.VARCHAR(50))
    country = db.Column(db.VARCHAR(50))
    province = db.Column(db.VARCHAR(50))
    phone_number = db.Column(db.VARCHAR(50))
    registration_date = db.Column(db.DateTime)

class Makes(Base):
    __tablename__ = 'makes'
    __table_args__ = {'schema': 'hoteldbs', 'extend_existing': True}
    booking_number = db.Column(db.Integer, primary_key=True)
    cust_sin_number = db.Column(db.Integer)
    emp_sin_number = db.Column(db.Integer)


# Handling requests that are applicable throughout the entirety of the web app
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
            return render_template('employeeSearchPage.html', items=itemsList)
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
roomDetails = []


@app.route('/customerSearchRooms', methods=['POST'])
def customerSearchRooms():
    cityList = db.session.query(hotel_chain.c.city)

    itemsList = set()
    for city in cityList:
        itemsList.add(city[0])

    itemsList = sorted(itemsList)

    if request.method == 'POST':
        cityName = request.form['citySelect']
        bookingStartDate = request.form['startDate']
        bookingEndDate = request.form['endDate']

        if cityName == 'Los angeles':
            cityName = 'Los Angeles'
        elif cityName == 'Rio de janeiro':
            cityName = 'Rio de Janeiro'
        elif cityName == 'New yorkcity':
            cityName = 'New York City'
        elif cityName == 'San jose':
            cityName = 'San Jose'

        cityName = cityName.capitalize()

        if cityName == '' or bookingStartDate == '' or cityName == 'holder':
            return render_template('customerSearchPage.html', message='Either cityName or bookingDate is null.',
                                   items=itemsList)
        else:

            yearStart = int(bookingStartDate[0:4])
            monthStart = int(bookingStartDate[5:7])
            dayStart = int(bookingStartDate[8:])

            yearEnd = int(bookingEndDate[0:4])
            monthEnd = int(bookingEndDate[5:7])
            dayEnd = int(bookingEndDate[8:])

            dateTimeFormattedStart = datetime.datetime(yearStart, monthStart, dayStart, 0, 0)
            dateTimeFormattedEnd = datetime.datetime(yearEnd, monthEnd, dayEnd, 0, 0)
            roomDetails.append(dateTimeFormattedStart)
            roomDetails.append(dateTimeFormattedEnd)
            result = db.session.query(rooms_hotel_chain, rooms, rooms, hotel_chain).select_from(rooms).join(
                rooms_hotel_chain).join(hotel_chain).filter(
                hotel_chain.c.city == cityName and datetime(rooms.c.date_available) <= dateTimeFormattedStart).order_by(
                rooms.c.room_number.asc())
            finalResult = []
            for r in result:
                tmpList = []
                x = r[4]
                if x <= dateTimeFormattedStart:
                    tmpR3 = str(r[3])
                    tmpR6 = str(r[6])
                    tmpR7 = str(r[7])
                    tmpR0 = str(r[0])
                    roomDetails.append(tmpR3)
                    roomDetails.append(tmpR0)
                    tmpList.append('Price: ' + tmpR3)
                    tmpList.append('View Type: ' + tmpR6)
                    tmpList.append('Amenities: ' + tmpR7)
                    tmpList.append('Room Number: ' + tmpR0)
                    finalResult.append(tmpList)
                    print(r)
            return render_template('customerSearchPage.html', items=itemsList, results=result, roomDetails=finalResult)


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
        numOccupants = request.form['numberOfOccupants']

        if cusSINNum == '' or cusFirstName == '' or cusLastName == '' or cusHouseNum == '' or cusStreetName == '' \
                or cusCityName == '' or cusCountryName == '' or cusPostalCode == '' or cusPhoneNumber == '' \
                or numOccupants == '':
            return render_template('customerBookingPage.html',
                                   message='One or more of your required fields are empty, please try again')

        startDate = roomDetails[0]
        endDate = roomDetails[1]
        x = endDate - startDate
        x = int(x.days)
        print(x)

        price = float(roomDetails[2])
        roomNum = roomDetails[3]

        price = price * x
        roomTypes = ['Single', 'Double', 'Double-double', 'Triple', 'Quad', 'Queen', 'King', 'Studio', 'Twin']
        roomType = random.choice(roomTypes)
        bookingNum = random.randint(40, 9999)

        newBooking = Booking(booking_number=bookingNum, room_type=roomType, number_occupants=numOccupants,
                             renting=True, check_in_date=startDate, check_out_date=endDate,
                             total_price=price
                             )
        db.session.add(newBooking)
        db.session.commit()

        newCustomer = Customer(cust_sin_number=cusSINNum, first_name=cusFirstName, middle_name=cusMiddleName,
                               last_name=cusLastName, house_number=cusHouseNum, street_name=cusStreetName,
                               postal_code=cusPostalCode, apt_number=cusAptNum, city=cusCityName,
                               country=cusCountryName, province=cusProvinceName, phone_number=cusPhoneNumber,
                               registration_date=datetime.datetime.today()
                               )
        db.session.add(newCustomer)
        db.session.commit()

        newMakes = Makes(booking_number=bookingNum, cust_sin_number=cusSINNum)
        db.session.add(newMakes)
        db.session.commit()

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

@app.route('/employeeSearchRooms', methods=['POST'])
def employeeSearchRooms():
    cityList = db.session.query(hotel_chain.c.city)

    itemsList = set()
    for city in cityList:
        itemsList.add(city[0])

    itemsList = sorted(itemsList)

    if request.method == 'POST':
        cityName = request.form['citySelect']
        bookingStartDate = request.form['startDate']
        bookingEndDate = request.form['endDate']

        if cityName == 'Los angeles':
            cityName = 'Los Angeles'
        elif cityName == 'Rio de janeiro':
            cityName = 'Rio de Janeiro'
        elif cityName == 'New yorkcity':
            cityName = 'New York City'
        elif cityName == 'San jose':
            cityName = 'San Jose'

        cityName = cityName.capitalize()

        if cityName == '' or bookingStartDate == '' or cityName == 'holder':
            return render_template('employeeSearchPage.html', message='Either cityName or bookingDate is null.',
                                   items=itemsList)
        else:

            yearStart = int(bookingStartDate[0:4])
            monthStart = int(bookingStartDate[5:7])
            dayStart = int(bookingStartDate[8:])

            yearEnd = int(bookingEndDate[0:4])
            monthEnd = int(bookingEndDate[5:7])
            dayEnd = int(bookingEndDate[8:])

            dateTimeFormattedStart = datetime.datetime(yearStart, monthStart, dayStart, 0, 0)
            dateTimeFormattedEnd = datetime.datetime(yearEnd, monthEnd, dayEnd, 0, 0)
            roomDetails.append(dateTimeFormattedStart)
            roomDetails.append(dateTimeFormattedEnd)
            result = db.session.query(rooms_hotel_chain, rooms, rooms, hotel_chain).select_from(rooms).join(
                rooms_hotel_chain).join(hotel_chain).filter(
                hotel_chain.c.city == cityName and datetime(rooms.c.date_available) <= dateTimeFormattedStart).order_by(
                rooms.c.room_number.asc())
            finalResult = []
            for r in result:
                tmpList = []
                x = r[4]
                if x <= dateTimeFormattedStart:
                    tmpR3 = str(r[3])
                    tmpR6 = str(r[6])
                    tmpR7 = str(r[7])
                    tmpR0 = str(r[0])
                    roomDetails.append(tmpR3)
                    roomDetails.append(tmpR0)
                    tmpList.append('Price: ' + tmpR3)
                    tmpList.append('View Type: ' + tmpR6)
                    tmpList.append('Amenities: ' + tmpR7)
                    tmpList.append('Room Number: ' + tmpR0)
                    finalResult.append(tmpList)
                    print(r)
            return render_template('employeeSearchPage.html', items=itemsList, results=result, roomDetails=finalResult)


@app.route('/employeeFinishBooking', methods=['POST'])
def employeeFinishBooking():
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
        numOccupants = request.form['numberOfOccupants']

        if cusSINNum == '' or cusFirstName == '' or cusLastName == '' or cusHouseNum == '' or cusStreetName == '' \
                or cusCityName == '' or cusCountryName == '' or cusPostalCode == '' or cusPhoneNumber == '' \
                or numOccupants == '':
            return render_template('employeeBookingPage.html',
                                   message='One or more of your required fields are empty, please try again')

        startDate = roomDetails[0]
        endDate = roomDetails[1]
        x = endDate - startDate
        x = int(x.days)
        print(x)

        price = float(roomDetails[2])
        roomNum = roomDetails[3]

        price = price * x
        roomTypes = ['Single', 'Double', 'Double-double', 'Triple', 'Quad', 'Queen', 'King', 'Studio', 'Twin']
        roomType = random.choice(roomTypes)
        bookingNum = random.randint(40, 9999)

        newBooking = Booking(booking_number=bookingNum, room_type=roomType, number_occupants=numOccupants,
                             renting=True, check_in_date=startDate, check_out_date=endDate,
                             total_price=price
                             )
        db.session.add(newBooking)
        db.session.commit()

        newCustomer = Customer(cust_sin_number=cusSINNum, first_name=cusFirstName, middle_name=cusMiddleName,
                               last_name=cusLastName, house_number=cusHouseNum, street_name=cusStreetName,
                               postal_code=cusPostalCode, apt_number=cusAptNum, city=cusCityName,
                               country=cusCountryName, province=cusProvinceName, phone_number=cusPhoneNumber,
                               registration_date=datetime.datetime.today()
                               )
        db.session.add(newCustomer)
        db.session.commit()

        newMakes = Makes(booking_number=bookingNum, cust_sin_number=cusSINNum )
        db.session.add(newMakes)
        db.session.commit()

        return render_template('employeeBookingPage.html')


@app.route('/employeeCheckIn', methods =['POST'])
def employeeCheckIn():
    if request.method == 'POST':

        return render_template('employeeCheckIn.html')

@app.route('/employeeCheckInSearch', methods = ['POST'])

def employeeCheckInSearch():
    


    if request.method == 'POST':
         
        custSIN = request.form['customerSIN']
        custSIN = int(custSIN)
        result = db.session.query(booking,makes,customer).select_from(booking).join(
        makes).join(customer).filter(
            customer.c.cust_sin_number == makes.c.cust_sin_number and makes.c.booking_number == booking.c.booking_number ).order_by(customer.c.cust_sin_number.asc())

        tmpList = set()
        bookingList = set()
        for r in result: 
            x = r[8]
            y = r[3] 
            if x == custSIN and y == True: 
                tmpList.add(r)
        return render_template('employeeCheckIn.html', items = tmpList)

@app.route('/employeeCheckingCustomerIn', methods = ['POST'])
def employeeCheckingCustomerIn():

    if request.method == 'POST':
        
        tmpData = request.form['bookings']
        tmpData = tmpData.split(',')
        print(tmpData)
        bookingId = tmpData[0][1:]
        print(bookingId)

        return render_template('employeeCheckIn.html')






if __name__ == '__main__':
    app.run()
