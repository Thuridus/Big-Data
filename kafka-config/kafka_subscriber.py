# Install: pip3 install kafka-python
from kafka import KafkaConsumer

ExecutionActive = False

# Is called whenever a spark execution has to be started
def StartSparkExecution():
    global ExecutionActive
    if ExecutionActive == False:
        ExecutionActive = True
    else:
        return
    print("Spark execution finished")
    ExecutionActive = False



# The bootstrap server to connect to
bootstrap = 'my-cluster-kafka-bootstrap:9092'

# Create a comsumer instance
# cf.
print('Starting KafkaConsumer')
#consumer = KafkaConsumer('spark_notification', bootstrap_servers='my-cluster-kafka-bootstrap:9092')
consumer = KafkaConsumer('spark_notification', bootstrap_servers='10.0.2.15:31952')


# Print out all received messages
for msg in consumer:
    #print("Message Received: ", msg)
    message = str(msg.value.decode())
    
    if message == 'new_data_available':
        print("Received import notification from import pod. Starting Spark execution.")
        StartSparkExecution()


