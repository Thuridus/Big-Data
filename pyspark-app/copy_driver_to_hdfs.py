import pywebhdfs.webhdfs

hdfsweburl = "http://10.0.2.15:31583" # adjust to individual port and ip-adress
hdfsconn = pywebhdfs.webhdfs.PyWebHdfsClient(base_uri_pattern=f"{hdfsweburl}/webhdfs/v1/",
                                         request_extra_opts={'verify': False, 'auth': ('admin', 'admin-password')})

with open('/root/Desktop/github_repo/pyspark-app/pyspark_driver.py', 'r') as file: # Adjust path to your directory
    hdfsconn.make_dir("/app")
    filecontent = file.read()
    hdfsconn.delete_file_dir("/app/pyspark_driver.py")
    hdfsconn.create_file("/app/pyspark_driver.py", filecontent, permission=777)

print("file created")