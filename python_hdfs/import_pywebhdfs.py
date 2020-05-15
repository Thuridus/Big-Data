import pywebhdfs.webhdfs
import logging
import socket

# Enable to get verbose logging
# logging.basicConfig(level=logging.DEBUG)

webhdfs_address = socket.gethostbyname("knox-apache-knox-helm-svc")
print(webhdfs_address)

example_dir = '/user/root/input/example/'
example_file = '/user/root/input/example/example.txt'
example_data = '01010101010101010101010101010101010101010101\n'
rename_dir = '/user/root/input/example_rename'

# create a new client instance
hdfs = pywebhdfs.webhdfs.PyWebHdfsClient(base_uri_pattern=f"http://{webhdfs_address}:8080/webhdfs/v1/",
                                         request_extra_opts={'verify': False, 'auth': ('admin', 'admin-password')})
#hdfs = pywebhdfs.webhdfs.PyWebHdfsClient(base_uri_pattern=f"{webhdfs_address}/webhdfs/v1/",
 #                                        request_extra_opts={'verify': False, 'auth': ('admin', 'admin-password')})


# List root dir
print('-----------------------------------------------------------------')
print('Listing /user/root/:')
hdfs.make_dir("/user/root/", permission=755)
root_dir = hdfs.list_dir("/user/root/")
print(root_dir)

# create a new directory for the example
print('-----------------------------------------------------------------')
print(f'Making new HDFS directory at: {example_dir}')
hdfs.make_dir(example_dir, permission=755)

# get a dictionary of the directory's status
dir_status = hdfs.get_file_dir_status(example_dir)
print(dir_status)

# create a new file on hdfs
print('-----------------------------------------------------------------')
print(f'making new file at: {example_file}')
hdfs.create_file(example_file, example_data)

file_status = hdfs.get_file_dir_status(example_file)
print(file_status)

# get the checksum for the file
file_checksum = hdfs.get_file_checksum(example_file)
print(file_checksum)

# append to the file created in previous step
print('-----------------------------------------------------------------')
print(f'appending to file at: {example_file}')
hdfs.append_file(example_file, example_data)

file_status = hdfs.get_file_dir_status(example_file)
print(file_status)

# checksum reflects file changes
file_checksum = hdfs.get_file_checksum(example_file)
print(file_checksum)

# read in the data for the file
print('-----------------------------------------------------------------')
print(f'reading data from file at: {example_file}')
file_data = hdfs.read_file(example_file)
print(file_data)

# rename the example_dir
print('-----------------------------------------------------------------')
print(f'renaming directory from {example_dir} to {rename_dir}\n')
hdfs.rename_file_dir(example_dir, '/{0}'.format(rename_dir))

# list the contents of the new directory
listdir_stats = hdfs.list_dir(rename_dir)
print(listdir_stats)

example_file = '{dir}/example.txt'.format(dir=rename_dir)

# delete the example file
print('-----------------------------------------------------------------')
print(f'deleting example file at: {example_file}')
hdfs.delete_file_dir(example_file)

# list the contents of the directory
listdir_stats = hdfs.list_dir(rename_dir)
print(listdir_stats)

# delete the example directory
print('-----------------------------------------------------------------')
print(f'deleting the example directory at: {rename_dir}')
hdfs.delete_file_dir(rename_dir, recursive='true')