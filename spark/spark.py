
from pyspark import SparkContext
from pyspark.streaming import StreamingContext
import mysql.connector
from pyspark.sql import SparkSession


db_connection = mysql.connector.connect(user='user', database='PROJET', password='user', host="192.168.33.12",port=3306)
db_cursor = db_connection.cursor()

sc = SparkContext("local[2]","Network")
ssc = StreamingContext(sc, 1)
socket_stream = ssc.socketTextStream("192.168.33.10", 9999)

def isascii(s):
 return len(s) == len(s.encode())

def takeAndPrint(rdd):
 num = 9999999999
 taken = rdd.take(num)
 for record in taken[:num]:
  if(isascii(record)):
   print(record)
   db_cursor.execute("INSERT INTO DATA(name) VALUES " + "('" + str(record) + "')" + ";")
   db_cursor.execute("FLUSH TABLES;")


socket_stream.foreachRDD(takeAndPrint)

ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate



