# Install: pip3 install kafka-python
from kafka import KafkaConsumer
from sqlalchemy import create_engine
import pywebhdfs.webhdfs
import mysql.connector
import pandas
import threading
import time
import csv
from io import StringIO

class SparkDriverJob:
    def __init__(self, kafka_producer, hdfs_connection, db_host, db_port, db_user, db_pw, db_name):
        self.ExecutionActive = False
        self.kafkaproducer = kafka_producer
        self.hdfsconnection = hdfs_connection
        self.dbhost = db_host
        self.dbport = db_port
        self.dbuser = db_user
        self.dbpw = db_pw
        self.dbname = db_name
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()   
        
    def run(self):
        #self.StartSparkExecution()
        #self.ExportResultToDB()
        #self.ValidateExport()

        for msg in self.kafkaproducer:
            print("Message Received: ", msg)
            message = str(msg.value.decode())
            if message == 'new_data_available':
                print("Received import notification from import pod. Starting Spark execution.")
                #self.StartSparkExecution()   

    # Is called whenever a spark execution has to be started
    def StartSparkExecution(self):
        if self.ExecutionActive == False:
            self.ExecutionActive = True
        else:
            print("Spark is still running")
            return
        # execute spark submit
        
        print("Spark execution finished")
        self.ExecutionActive = False

    def ExportResultToDB(self):
        #read results from hdfs into datafram
        covidcsv = self.hdfsconnection.read_file("/tmp/results/corona.csv").decode()
        dataframecovid = pandas.read_csv(StringIO(covidcsv), index_col='date', keep_default_na=False)
        
        daxcsv = self.hdfsconnection.read_file("/tmp/results/dax.csv").decode()
        dataframedax = pandas.read_csv(StringIO(daxcsv), index_col='Date')
        dataframedax = dataframedax.rename(columns={"Date" : "date", "open_sum" : "open", "close_sum" : "close", "abs_diff": "diff"})
        dataframedax.index.names = ["date"]


        dbengine =  create_engine('mysql+pymysql://{user}:{pw}@{host}:{port}/{db}'.format(user=self.dbuser, pw=self.dbpw, db=self.dbname, port=self.dbport, host=self.dbhost))
        with dbengine.connect() as dbconnection:
            dataframecovid.to_sql('infects', dbconnection, if_exists='append')
            dataframedax.to_sql('dax', dbconnection, if_exists='append')

    def ValidateExport(self):
        dbtest = mysql.connector.connect(host=self.dbhost, port=self.dbport, user=self.dbuser, password=self.dbpw, database=self.dbname, auth_plugin='mysql_native_password')
        cursor = dbtest.cursor()
        cursor.execute("SELECT * FROM infects")
        for val in cursor:
            print(val)
        cursor.close()
        cursor = dbtest.cursor()
        cursor.execute('SELECT * FROM dax')
        for val in cursor:
            print(val)
        cursor.close()
        dbtest.close()




# Connect to HDFS to gather result data
#hdfsweburl = "http://" + str(socket.gethostbyname("knox-apache-knox-helm-svc")) + ":8080"
hdfsweburl = "http://10.0.2.15:31583"
hdfsconn = pywebhdfs.webhdfs.PyWebHdfsClient(base_uri_pattern=f"{hdfsweburl}/webhdfs/v1/",
                                         request_extra_opts={'verify': False, 'auth': ('admin', 'admin-password')})

# Debug preparation code
#hdfsconn.make_dir("/tmp/results")
#dataframecovid = pandas.read_csv("/root/Desktop/github_repo/pyspark-app/result/corona/part-00000-c5db4887-e907-453b-b95e-753eb8d81c40-c000.csv", index_col='date', keep_default_na=False, encoding='utf-8')
#print(dataframecovid)
#csvdata = dataframecovid.to_csv(sep=",",index=True, line_terminator='\n', encoding='utf-8')
#hdfsconn.delete_file_dir("/tmp/results/corona.csv")
#hdfsconn.create_file("/tmp/results/corona.csv", csvdata, permission=777)

#hdfsconn.delete_file_dir("/tmp/results/dax.csv")
#dataframedax = pandas.read_csv("/root/Desktop/github_repo/pyspark-app/result/dax/part-00000-1a7de9b8-84a2-4682-8950-483587a10c67-c000.csv", index_col='Date', keep_default_na=False, encoding='utf-8')
#hdfsconn.create_file("/tmp/results/dax.csv", dataframedax.to_csv(sep=",", index=True, line_terminator="\n"), permission=777)

with open('/root/Desktop/github_repo/pyspark-app/pyspark_driver.py', 'r') as file:
    hdfsconn.make_dir("/app")
    filecontent = file.read()
    hdfsconn.delete_file_dir("/app/pyspark_driver.py")
    hdfsconn.create_file("/app/pyspark_driver.py", filecontent, permission=777)


# Clear DB
#dbtest = mysql.connector.connect(host='10.0.2.15', port='30813', user='root', password='mysecretpw', database='mysqldb', auth_plugin='mysql_native_password')
#dbcursor = dbtest.cursor()
#dbcursor.execute('DELETE FROM infects')
#dbcursor.execute('DELETE FROM dax')
#dbcursor.close()
#dbtest.close()




# The bootstrap server to connect to
bootstrap = 'my-cluster-kafka-bootstrap:9092'

# Create a comsumer instance
print('Starting KafkaConsumer')
#consumer = KafkaConsumer('spark_notification', bootstrap_servers='my-cluster-kafka-bootstrap:9092')
consumer = KafkaConsumer('spark_notification', bootstrap_servers='10.0.2.15:31952')




driverjob = SparkDriverJob(consumer, hdfsconn, '10.0.2.15', 30813, 'root', 'mysecretpw', 'mysqldb')


# Create Dataframe from results on HDFS
#dataframecovid = pandas.read_csv("/root/Desktop/github_repo/pyspark-app/result/corona/part-00000-c5db4887-e907-453b-b95e-753eb8d81c40-c000.csv", index_col='date')
#dataframedax = pandas.read_csv("/root/Desktop/github_repo/pyspark-app/result/dax/part-00000-1a7de9b8-84a2-4682-8950-483587a10c67-c000.csv", index_col='Date')
#dataframedax = dataframedax.rename(columns={"Date" : "date", "open_sum" : "open", "close_sum" : "close", "abs_diff": "diff"})
#dataframedax.index.names = ["date"]


#dbengine =  create_engine('mysql+pymysql://{user}:{pw}@10.0.2.15:30813/{db}'.format(user='root', pw='mysecretpw', db='mysqldb'))
#with dbengine.connect() as dbconnection:
#    result = dataframecovid.to_sql('infects', dbconnection, if_exists='append')
#    re6sult = dataframedax.to_sql('dax', dbconnection, if_exists='append')




