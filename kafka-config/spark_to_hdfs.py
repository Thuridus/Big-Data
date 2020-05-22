import pywebhdfs.webhdfs
import time
import datetime
import os
import socket
import threading
import os
import sys

# All import logic is part of this class
class HDFSJob:
    def __init__(self, hdfsconn, hdfs_export_path):
        self.hdfsconnection = hdfsconn
        self.hdfsexportpath = hdfs_export_path

        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    # Main Method. Is executed in a deaomized thread
    def run(self):
        while True:
            print("Put pysaprk app to HDFS")
        
            # Put pysaprk file to HDFS
            self.export_sparkFile()
            print("Pyspark app successfully put to HDFS")

    # Put pyspark app to HDFS via Web API
    def export_sparkFile(self):
        # Define path to pyspark app 
        sparkPath = "../pyspark-app/pyspark_driver.py"

        # Define hdfs path of result file
        hdfs_export_filename = self.hdfsexportpath + "/pyspark_driver.py"

        # Check if there is already a file existing and delete it
        if self.hdfsconnection.exists_file_dir(hdfs_export_filename):
            self.hdfsconnection.delete_file_dir(hdfs_export_filename)
        
        # Create pyspark file
        self.hdfsconnection.create_file(hdfs_export_filename, sparkPath, permission=777)
        file_status = hdfsconnection.get_file_dir_status(hdfs_export_filename)
        print(file_status)

# Get IP of Knox Service by DNSLookup
hdfsweburl = "http://" + str(socket.gethostbyname("knox-apache-knox-helm-svc")) + ":8080"

# Connect to HDFS via WebHdfsClient
hdfsconn = pywebhdfs.webhdfs.PyWebHdfsClient(base_uri_pattern=f"{hdfsweburl}/webhdfs/v1/",
                                         request_extra_opts={'verify': False, 'auth': ('admin', 'admin-password')})

# Base paths for the result data
#corona_file_path = "/user/root/tmp/results/corona"
#dax_file_path = "/user/root/tmp/results/dax"
app_file_path = "/user/root/app"

# Create the base directories
hdfsconn.make_dir("/user/root/app", permission=777)
hdfsconn.make_dir("/user/root/tmp", permission=777)
hdfsconn.make_dir("/user/root/tmp/results", permission=777)
hdfsconn.make_dir("/user/root/tmp/results/corona", permission=777)
hdfsconn.make_dir("/user/root/tmp/results/dax", permission=777)
 
# Check if the directories actually were created
foundCorona = False
foundDax = False
root_dir = hdfsconn.list_dir("/user/root/tmp/results")
# Check result directories 
if len(root_dir) > 0:
    for dir in root_dir.values():
        for dir2 in dir.values():
            for dir3 in dir2:
                if dir3["pathSuffix"] == "corona":
                    foundCorona = True
                if dir3["pathSuffix"] == "dax":
                    foundDax = True
# Check app directory
foundApp = False
root_dir = hdfsconn.list_dir("/user/root")
if len(root_dir) > 0:
    for dir in root_dir.values():
        if dir ["pathSuffix"] == "app":
            foundApp = True

if foundCorona and foundDax and foundApp:
    print("Starting separate Import Thread")
    # Init the import thread once
    import_thread = HDFSJob(hdfsconn, app_file_path)
    print("Import thread initialized. Main thread is going to sleep")
    #while True:
        #Sleep and let the thread do the work
        #time.sleep(60)