import time
from datetime import datetime
from pyspark.sql import SQLContext, Row
sqlContext = SQLContext(sc)

df = sqlContext.read.format('com.databricks.spark.csv').\
  options(header='true', inferschema='true').\
  load('file:///home/oxclo/datafiles/wind/*')


convertTime = lambda t: \
datetime.fromtimestamp( \
time.mktime(time.strptime(t, "%Y-%m-%d? %H:%M")))



df.show(2)

toRow = lambda s: \
Row(stationid=s.Station_ID, \
time=convertTime(s.Interval_End_Time), \
direction=s.Wind_Direction_Deg, \
temp=s.Ambient_Temperature_Deg_C, \
velocity=s.Wind_Velocity_Mtr_Sec)

newDF = df.rdd.map(toRow).toDF()

newDF.show(2)


newDF.write.format("org.apache.spark.sql.cassandra").mode('append').options(table="winddata", keyspace="wind").save() 
