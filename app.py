from flask.helpers import url_for
from flask.templating import DispatchingJinjaLoader
import mysql.connector
import csv
import os
from flask import Flask, render_template, request, flash, jsonify,redirect
from werkzeug.utils import secure_filename

'''s = "D:/Dashboard Code/Data"
f = os.listdir(s)[0]'''


def allowed_file(file):
    ALLOWED_EXTENSIONS = {'csv'}
    return '.' in file and \
           file.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def db_connection():
    mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='AJp66$2205',
        database='Dashboard_Data'
    )

    if(mydb):
        print("Connected Successfully")
    else:
        print("Connection Failed")
    
    #return mydb
    return mydb

def clear_data():
    mydb = db_connection() 
    sql = "TRUNCATE Placement_Data;"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    mydb.commit()
    print("all rows deleted from table")
    return mydb


app = Flask(__name__)
app.secret_key = 'dashboard placement'
app.config['Data'] = "D://Dashboard Code/Data"


@app.route('/')
def dashboard():
    return render_template('dashboard.html')

@app.route('/table')
def table():
    return render_template('table.html')

@app.route('/user')
def user():
    return render_template('user.html')

@app.route('/notifications')
def notifications():
    return render_template('notifications.html')

@app.route('/addData')
def notification():
    return render_template('addData.html')

@app.route('/upgrade')
def upgrade():
    return render_template('upgrade.html')

@app.route("/upload",methods = ['POST'])
def upload():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        print(file.filename)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['Data'], filename))
        
#@app.route('/data_entry')
#def data_entry():

    mydb = clear_data()
    s = "D:/Dashboard Code/Data"
    with open(s+"/"+file.filename) as csv_file:
        csvfile = csv.reader(csv_file, delimiter= ',')
        all_value = []

        for row in csvfile:
            value = (row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7])
            
            all_value.append(value)
    
    all_value.pop(0)

    if os.path.exists(s+"/"+file.filename):
        os.remove(s+"/"+file.filename)


    query = """INSERT INTO Placement_Data VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""

    mycursor = mydb.cursor()
    mycursor.executemany(query,all_value)

    mydb.commit()
    print(mycursor.rowcount,"rows inserted in Table")

    return redirect('/')


@app.route("/addRecentData",methods = ['POST'])
def addRecentData():
    if request.method == 'POST':
        req = request.form
        Name = req.get("NAME")
        Enrollment_no = req.get("ENROLLMENT_NO")
        Date = req.get("DATE")
        Department = req.get("DEPARTMENT")
        Company = req.get("COMPANY")
        City = req.get("CITY")
        Country = req.get("COUNTRY")
        Salary = int(req.get("SALARY"))
    
        value = (Name,Enrollment_no,Date,Department,Company,City,Country,Salary)
    print(value)

    mydb = db_connection()
    query = """INSERT INTO Placement_Data VALUES (%s,%s,%s,%s,%s,%s,%s,%s);"""
    
    mycursor = mydb.cursor()
    mycursor.execute(query,value)

    mydb.commit()
    print(mycursor.rowcount,"rows inserted in Table")

    #Need For Update
    return render_template('addData.html')


@app.route('/selector',methods=['POST'])
def selector():
    if request.method == "POST":
        print(request.form)
        print("hello")
        option = request.form.get("PLACEMENT")
    
    print(option)
    if option == "all":
        return render_template('allPlacements.html')
    else:
        return render_template('table.html')

@app.route('/all_placements/',methods=['POST'])
def all_placements():
    mydb = db_connection()

    sql = "SELECT Name, Placement_Date, Department, Company, job_city, job_country, Salary FROM Placement_Data ORDER BY Placement_Date DESC;"
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    
    myresult = mycursor.fetchall()

    Table = [[]*6]*(len(myresult))
    T = [['Name','Date','Department', 'Company', 'City', 'Country', 'Salary($)']]

    for i in range(len(myresult)):
        Table[i] = list(myresult[i])
    
    Table = T + Table
    print(Table)
    '''for i in myresult:
        print(i)'''
    return jsonify(Table)

@app.route('/top_placement_currentYear/',methods=['POST'])
def top_placements_currentYear():
    mydb = db_connection()
    '''mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='AJp66$2205',
        database='Dashboard_Data'
    )'''

    sql = """SELECT Name, Department, Company, job_city, job_country, Salary FROM Placement_Data
WHERE YEAR(Placement_Date)='2021'
ORDER BY Salary DESC LIMIT 10;"""
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    
    myresult = mycursor.fetchall()

    Table = [[]*6]*10
    T = [['Name','Department', 'Company', 'City', 'Country', 'Salary($)']]

    for i in range(10):
        Table[i] = list(myresult[i])
    
    Table = T + Table
    print(Table)
    '''for i in myresult:
        print(i)'''
    return jsonify(Table)

@app.route('/top_placement_ofalltime/',methods=['POST'])
def top_placements_ofalltime():
    mydb = db_connection()
    '''mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='AJp66$2205',
        database='Dashboard_Data'
    )'''

    sql = """SELECT Name, YEAR(Placement_Date), Department, Company, job_city, job_country, Salary FROM Placement_Data
ORDER BY Salary DESC LIMIT 10;"""
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    
    myresult = mycursor.fetchall()

    Table = [[]*6]*10
    T = [['Name','Year','Department', 'Company', 'City', 'Country', 'Salary($)']]

    for i in range(10):
        Table[i] = list(myresult[i])
        Table[i][1] = str(Table[i][1])
    
    Table = T + Table
    print(Table)
    '''for i in myresult:
        print(i)'''
    return jsonify(Table)


@app.route('/populate_Pie/',methods = ['POST'])
def populate_Pie():
    mydb = db_connection()
    '''mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='AJp66$2205',
        database='Dashboard_Data'
    )'''

    sql = """SELECT DISTINCT Department, (COUNT(*)*'100'/(SELECT COUNT(Department) FROM Placement_Data)) AS 'Percentage' FROM Placement_Data GROUP BY Department;"""
    
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    
    myresult = mycursor.fetchall()
    
    #later check for row number
    Pie = [[]*2]*(len(myresult))
    P = [["Department","Percentage"]]
    for i in range(len(myresult)):
        Pie[i] = list(myresult[i])
    
    Pie = P + Pie
    
    print(Pie)
    #return jsonify({'data': render_template('response.html', Pie=Pie)})
    return jsonify(Pie)

@app.route('/populate_Area/',methods = ['POST'])
def populate_Area():
    mydb = db_connection()
    '''mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='AJp66$2205',
        database='Dashboard_Data'
    )'''

    sql = '''SELECT DISTINCT YEAR(Placement_Date) AS "placement_year", ( COUNT(CASE WHEN Department='CE' THEN Department END)) AS 'CE',
(COUNT(CASE WHEN Department='IT' THEN Department END)) AS 'IT',
(count(CASE WHEN Department='EC' THEN Department END)) AS 'EC' FROM Placement_Data
GROUP BY placement_year
ORDER BY placement_year;'''
    
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    
    myresult = mycursor.fetchall()

    Area =  [[]*2]*(len(myresult))

    A = [["","CE","IT","EC"]]
    for i in range(len(myresult)):
        Area[i] = list(myresult[i])
    
    Area = A + Area
    
    print(Area)
    return jsonify(Area)

    
    
@app.route('/populate_Column/',methods = ['POST'])
def populate_Column():
    mydb = db_connection()
    '''mydb = mysql.connector.connect(
        host='127.0.0.1',
        user='root',
        password='AJp66$2205',
        database='Dashboard_Data'
    )'''

    sql = '''SELECT DISTINCT MONTHNAME(Placement_Date) AS "placement_month", ( COUNT(CASE WHEN YEAR(Placement_Date)='2020' THEN Placement_Date END))  AS '2020',
(COUNT(CASE WHEN YEAR(Placement_Date)='2019' THEN Placement_Date END)) AS '2019' FROM Placement_Data
GROUP BY placement_month
ORDER BY FIELD( placement_month, "January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December");'''
    
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    
    myresult = mycursor.fetchall()

    Column =  [[]*2]*(len(myresult))

    C = [["","",""]]
    for i in range(len(myresult)):
        Column[i] = list(myresult[i])
        Column[i][0] = Column[i][0][:3]
    
    Column = C + Column
    
    print(Column)
    return jsonify(Column)

@app.route('/get_notifications/',methods = ['POST'])
def get_notifications():
    mydb = db_connection()

    sql = """SELECT Name, Salary, Company, enrollment_no FROM Dashboard_Data.Placement_Data
             WHERE YEAR(Placement_Date)='2021'
             ORDER BY Placement_Date DESC
             LIMIT 4;"""
    mycursor = mydb.cursor()
    mycursor.execute(sql)
    
    myresult = mycursor.fetchall()

    Nt =  [[]*4]*len(myresult)

    for i in range(len(myresult)):
        Nt[i] = list(myresult[i])
    
    print(Nt)
    return jsonify(Nt)


if __name__ == "__main__":
    app.run(debug=True)














