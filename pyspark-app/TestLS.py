from pyspark.sql.session import SparkSession
from pyspark.sql.functions import to_date
from pyspark import SQLContext

# inputFile = "hdfs://hadoop-hadoop-hdfs-nn:9000/input/Boston_Housing_Data.csv"
#inputInfections = "/Users/shabaldinalidiia/git/Big-Data/pyspark-app/results/infections"
inputInfections = "/Users/shabaldinalidiia/git/Big-Data/python_hdfs/infections.csv"

# outputFile = "hdfs://hadoop-hadoop-hdfs-nn:9000/tmp/Test_LS.txt"
outputFile = "/Users/shabaldinalidiia/git/Big-Data/pyspark-app/Test_LS"


#create SparkSession
spark = (SparkSession.
            builder.
            appName("TestLS").
            getOrCreate())

#read infections info and return dataframe using an infered schema
corona_in = spark.read.option("header", "true") \
        .option("inferSchema", "true") \
        .option("delimiter", ";") \
        .csv(inputInfections)


print(corona_in.printSchema())     
corona_in.show()

#TODO calculate relative difference to previous day
corona_out = corona_in.select(to_date('dateRep', 'dd/MM/yyy').alias('date'), 
                            corona_in.cases,
                            corona_in.deaths,
                            corona_in.countriesAndTerritories.alias('country'),
                            corona_in.continentExp.alias('continent'))
                            
corona_out.show()

# write the result to hdfs
corona_out.write.format("csv").option("header", "false").mode("append").save(outputFile)

#close SparkSession
spark.stop()


