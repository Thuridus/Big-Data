from pyspark.sql.session import SparkSession

# inputFile = "hdfs://hadoop-hadoop-hdfs-nn:9000/input/Boston_Housing_Data.csv"
inputInfections = "/Users/shabaldinalidiia/git/Big-Data/pyspark-app/results/infections"

# outputFile = "hdfs://hadoop-hadoop-hdfs-nn:9000/tmp/Test_LS.txt"
outputFile = "/Users/shabaldinalidiia/git/Big-Data/pyspark-app/Test_LS"


#create SparkSession
spark = (SparkSession
        .builder
        .appName("TestLS")
        .getOrCreate())

#read infections info and return dataframe using an infered schema
df1 = spark.read.option("header", "true") \
        .option("inferSchema", "true") \
        .option("delimiter", ";") \
        .json(inputInfections)

print(df1.printSchema())     
df1.show()

# write the result to hdfs
#df1.saveAsTextFile(outputFile)
#df1.write.csv.option("header", "true").save(outputFile)
#df1.write.csv(outputFile)

#close SparkSession
spark.stop()


