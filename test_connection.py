import mysql.connector


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="2942123"
)

print(mydb)