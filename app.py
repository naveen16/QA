from flask import Flask, jsonify
from flask import abort
from flask import make_response
from flask import request, render_template, send_from_directory
import sqlite3
import json

app = Flask(__name__, static_url_path='')

sqlite_file = "./qadb.sqlite"

@app.route('/')
def home():
   return render_template('home.html')

@app.route('/static/<path:path>')
def serveStaticFile(path):
   return send_from_directory('static',path)

@app.route('/qatester', methods=['GET','POST'])
def qatester():
   return render_template('qatester.html')

@app.route('/qa/<int:qa_id>', methods=['GET'])
def get_session(qa_id):
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute('SELECT * FROM SESSION WHERE SID='+str(qa_id))
  rows = c.fetchall()
  ans = []
  for row in rows:
    d = {}
    for i,col in enumerate(c.description):
      d[col[0]] = row[i]
    ans.append(d)
  conn.close()
  return json.dumps(ans)

@app.route('/qa/<int:qa_id>/questions/', defaults={'x':''} )
@app.route('/qa/<int:qa_id>/questions/<string:x>', methods=['GET'])
def get_QA(qa_id,x):
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  if x == 'a':
    c.execute('SELECT * FROM QA WHERE SID='+str(qa_id)+' and Answered_By is not null')
  elif x == 'u':
    c.execute('SELECT * FROM QA WHERE SID='+str(qa_id)+' and Answered_By is null')
  else:
    c.execute('SELECT * FROM QA WHERE SID='+str(qa_id))
  rows = c.fetchall()
  ans = []
  for row in rows:
    d = {}
    for i,col in enumerate(c.description):
      d[col[0]] = row[i]
    ans.append(d)
  conn.close()
  return json.dumps(ans)

@app.route('/qa', methods=['POST'])
def create_session():
  if ((not request.json) or 
     (not 'hostname' in request.json) or
     (not 'starttime' in request.json) or
     (not 'endtime' in request.json)):
       abort(400)
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute('SELECT max(SID) FROM SESSION')
  rows = c.fetchall()
  if not rows[0][0]:
    sid = 1
  else:
    sid = rows[0][0] + 1
  insertQry = "INSERT INTO SESSION VALUES ("+str(sid)+",'"+ request.json['hostname']+"','"+ request.json['starttime']+"','"+request.json['endtime']+"')"
  c.execute(insertQry)
  conn.commit()
  conn.close()
  request.json['sid'] = sid
  return json.dumps(request.json), 201

@app.route('/question/<int:qa_id>', methods=['POST'])
def create_question(qa_id):
  if ((not request.json) or
     (not 'question' in request.json) or
     (not 'asked_by' in request.json)):
       abort(400)
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  c.execute('SELECT max(QNO) FROM QA WHERE SID='+str(qa_id))
  rows = c.fetchall()
  if not rows[0][0]:
    qno = 1
  else:
    qno = rows[0][0] + 1
  insertQry = "INSERT INTO QA VALUES ("+str(qa_id)+","+str(qno)+",'"+ request.json['question']+"','"+ request.json['asked_by']+"',null,null,null)"
  c.execute(insertQry)
  conn.commit()
  conn.close()
  return json.dumps(request.json), 201

@app.route('/answer/<int:qa_id>/<int:question_id>', methods=['POST'])
def create_answer(qa_id,question_id):
  if ((not request.json) or
    (not 'answer' in request.json) or
    (not 'answer_url' in request.json) or
    (not 'answered_by' in request.json)):
    abort(400)
  conn = sqlite3.connect(sqlite_file)
  c = conn.cursor()
  insertQry = "UPDATE QA SET Answer='"+request.json['answer']+"',Answer_URL='"+ request.json['answer_url']+"',Answered_By='"+request.json['answered_by']+"' WHERE QNO='"+str(question_id)+"'and SID='"+str(qa_id)+"'"
  print(insertQry)
  c.execute(insertQry)
  conn.commit()
  conn.close()
  return json.dumps(request.json), 201


@app.errorhandler(404)
def not_found(error):
     return make_response(jsonify({'error': 'Not found'}), 404)

@app.errorhandler(400)
def bad_request(error):
     return make_response(jsonify({'error': 'problem'}), 400)

if __name__ == '__main__':
     app.run(host='localhost', debug = True)
