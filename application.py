from flask import Flask
from flask import render_template

app = Flask(__name__)

@app.route('/qrcodelogin')
def index():
	return render_template('index.html')

import sqlite3
import random
@app.route('/qrcodelogin/get_key')
def get_key():
	conn = sqlite3.connect('logins.db')
	cursor = conn.cursor()
	key = random.randint(0, 999999)
	cursor.execute('INSERT INTO prelogin VALUES(%d, datetime("now","localtime"))'%(key))
	cursor.close()
	conn.commit()
	conn.close()
	return "%6d"%(key)

import time
@app.route('/qrcodelogin/check_login/<int:key>')
def check_login(key):
	conn = sqlite3.connect('logins.db')
	cursor = conn.cursor()
	cursor.execute('SELECT * FROM prelogin WHERE key == {0}'.format(key))
	values = cursor.fetchone()
	if values :
		if (time.time() - time.mktime(time.strptime(values[1], "%Y-%m-%d %H:%M:%S")) > 30) :
				cursor.execute('DELETE FROM prelogin WHERE key == {0}'.format(key))
		cursor.close()
		conn.commit()
		conn.close()
		return 'waiting'
	cursor.execute('SELECT * FROM logined WHERE key == {0}'.format(key))
	values = cursor.fetchone()
	if not values :
		cursor.close()
		conn.commit()
		conn.close()
		return 'timeout'
	cursor.close()
	conn.commit()
	conn.close()
	return values[1]

@app.route('/qrcodelogin/login', methods = ['GET', 'POST'])
def login():
	conn = sqlite3.connect('logins.db')
	cursor = conn.cursor()
	key = request.form['key']
	cursor.execute('SELECT * FROM prelogin WHERE key == {0}'.format(key))
	values = cursor.fetchone()
	if not values : return 'failed'
	cursor.execute('DELETE FROM prelogin WHERE key == {0}'.format(key))
	if (time.time() - time.mktime(time.strptime(values[1], "%Y-%m-%d %H:%M:%S")) > 30) : return 'failed'
	cursor.execute('INSERT INTO logined VALUES({0}, "{1}")'.format(key, request.form['name'].encode('UTF-8')))
	cursor.close()
	conn.commit()
	conn.close()
	return 'succeed'

if __name__ == '__main__':
	#app.run(host="123.57.72.138",port=5001)
	app.run(debug = True)
