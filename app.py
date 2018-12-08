from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request, render_template, send_from_directory
import sqlite3
import json

app = Flask(__name__, static_url_path='')

sqlite_file = "./notabledb.sqlite"

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/static/<path:path>')
def serveStaticFile(path):
   return send_from_directory('static',path)

@app.route('/notabletester', methods=['GET','POST'])
def notabletester():
   return render_template('notabletester.html')

#Get All Doctors
@app.route('/doctors', methods=['GET'])
def get_doctors():
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute('SELECT * FROM PHYSICIAN')
  rows = c.fetchall()
  ans = []
  for row in rows:
    d = {}
    for i,col in enumerate(c.description):
      d[col[0]] = row[i]
    ans.append(d)
  conn.close()
  return json.dumps(ans)

#Get all appointments for a Physician and a date
@app.route('/appointments/<int:pid>/<string:d>', methods=['GET'])
def get_appointments(pid,d):
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute("SELECT * FROM APPOINTMENT WHERE PID="+str(pid)+" AND APPDATE='"+d+"'")
  rows = c.fetchall()
  ans = []
  for row in rows:
    d = {}
    for i,col in enumerate(c.description):
      d[col[0]] = row[i]
    ans.append(d)
  conn.close()
  return json.dumps(ans)

#Delete an appointment using the appointment ID
@app.route('/deleteAppt/<int:aid>', methods=['GET'])
def delete_Appt(aid):
  print("IN DELETE")
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute('DELETE FROM APPOINTMENT WHERE AID='+str(aid))
  conn.commit()
  conn.close()
  jsonObj = {'DELETED':aid}
  return json.dumps(jsonObj), 201

#Create an appointment
@app.route('/appointment', methods=['POST'])
def create_appointment():
  #make sure all fields are included
  if ((not request.json) or
     (not 'pfname' in request.json) or
     (not 'plname' in request.json) or
     (not 'date' in request.json) or
     (not 'time' in request.json) or
     (not 'atype' in request.json) or
     (not 'pid' in request.json)):
       abort(400)
  pid = request.json['pid']
  tm = request.json['time'].strip()
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  #make sure the Physician id given is valid
  c.execute("SELECT pid FROM PHYSICIAN WHERE pid="+str(pid))
  rows = c.fetchall()
  if not rows:
    jsonObj = {'MESSAGE':str(pid)+" is invalid. Enter a valid Physician ID.",'status':'204'}
    return json.dumps(jsonObj), 201
  #make sure not to give a Physician more than 3 appointments for a single time
  c.execute("SELECT count(*) from APPOINTMENT WHERE pid="+str(pid)+" AND appdate='"+request.json['date']+"' AND apptime='"+request.json['time']+"'")
  rows = c.fetchall()
  if not rows or rows[0][0] < 3:
    #make sure the appointment time is in interval of 15 mins
    k = tm[3:]
    if k not in ['00','15','30','45']:
      jsonObj = {'MESSAGE':"Time must be in intervals of 15 mins.",'status':'204'}
      return json.dumps(jsonObj), 201
    c.execute('SELECT max(AID) FROM APPOINTMENT')
    rows = c.fetchall()
    if not rows:
      aid = 1
    else:
      aid = rows[0][0] + 1
    insertQry = "INSERT INTO APPOINTMENT VALUES ("+\
      str(aid)+",'"+\
      request.json['pfname']+"','"+\
      request.json['plname']+"','"+\
      request.json['date']+"','"+\
      request.json['time']+"','"+\
      request.json['atype']+"',"+\
      request.json['pid']+")"
    c.execute(insertQry)
    conn.commit()
    conn.close()
    request.json['aid'] = aid
    return json.dumps(request.json), 201
  else:
    jsonObj = {'MESSAGE':"Doctor already has 3 appointments at this time.",'status':'204'}
    return json.dumps(jsonObj), 201

@app.errorhandler(404)
def not_found(error):
     return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
     return make_response(jsonify({'error': 'problem'}), 400)

if __name__ == '__main__':
     app.run(host='localhost', debug = True)
