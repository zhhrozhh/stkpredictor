import mysql.connector
from mysql.connector import errorcode
databaseConnector = None
__scode = ''
__period = ''
__k = -1
__tablename = ''
class StkDatabase:
	def connect():
		if databaseConnector:
			return databaseConnector
		return mysql.connector.connect(user='zhangh40',password='A47035780',host='localhost',database='zhangh40')
	def close():
		try:
			databaseConnector.close()
		except:
			pass
		databaseConnector = None
	def config(d):
		__scode = d['scode'].replace(' ','_').replace("'",'"')
		__period = d['period']
		__k = int(d['k'])
		if k<0:
			raise Exception('k value error')
		if __period not in ['daily','hourly']:
			raise Exception('period error')
		__tablename = __scode+'_'+str(k)+distMAT+__period
	def create():
		if __tablename == '':
			raise Exception('not configed')
		cursor = StkDatabase.connect().cursor(buffered = True)
		query = 'CREATE TABLE IF NOT EXISTS '+__tablename+'(time VARCHAR(20),'
		for i in range(k):
			query += 'dist'+str(i)+' FLOAT,'
		query+=')' 
		print(query)
		cursor.execute(query)
		databaseConnector.commit()
		cursor.close()
	def drop():
		if __tablename == '':
			raise Exception('not configed')
		cursor = databaseConnector.cursor(buffered = True)
		query = 'DROP IF EXISTS '+__tablename
		cursor.execute(query)
		databaseConnector.commit()
		cursor.close()
	def get(time):
		query = r'SELECT * FROM '+__tablename+'WHERE time = '+time
		cursor = databaseConnector.cursor()
		cursor.execute(query)
		databaseConnector.commit()
		res = list(x for x in cursor)
		cursor.close()
		return res;

if __name__ == '__main__':
	StkDatabase.create(4,'yrd','daily')