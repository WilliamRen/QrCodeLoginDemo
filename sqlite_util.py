import sqlite3
conn = sqlite3.connect('logins.db')
cursor = conn.cursor()

#Create
cursor.execute('CREATE TABLE prelogin(key INTEGER, time TimeStamp)')
cursor.execute('CREATE TABLE logined(key INTEGER, name nvarchar(20))')

#Insert
#cursor.execute('INSERT INTO prelogin VALUES(%d, datetime("now","localtime"))'%(111111))

#Select
cursor.execute('SELECT * FROM prelogin')
print "\nprelogin: "
print cursor.fetchall()
cursor.execute('SELECT * FROM logined')
print "\nlogined: "
print cursor.fetchall()

cursor.close()
conn.commit()
conn.close()