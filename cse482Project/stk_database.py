import mysql.connector
from mysql.connector import errorcode
databaseConnector = None
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
	

if __name__ == '__main__':
	StkDatabase.connect()