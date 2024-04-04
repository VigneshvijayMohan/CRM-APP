import mysql.connector


dataBase = mysql.connector.connect(
    host = 'localhost',
    user = 'vignesh',
    passwd = 'kraken12@'
)

cursorObject = dataBase.cursor()

cursorObject.execute("CREATE DATABASE elderco")

print('All done..!')