from pyspark.sql import SparkSession, SQLContext
from pyspark.sql.functions import to_date, expr, current_date, date_sub, date_format
from pyspark.sql.functions import sum

# inputFile = "hdfs://hadoop-hadoop-hdfs-nn:9000/input/infections/infections.csv"
# inputFile = "hdfs://hadoop-hadoop-hdfs-nn:9000/input/fse/quandl_fse.csv"
inputInfections = "/Users/shabaldinalidiia/git/Big-Data/python_hdfs/infections.csv"
inputDAX = "/Users/shabaldinalidiia/git/Big-Data/python_hdfs/quandl_fse.csv"

# outputFile = "hdfs://hadoop-hadoop-hdfs-nn:9000/tmp/results"
outputFileCorona = "/Users/shabaldinalidiia/git/Big-Data/pyspark-app/result/corona"
outputFileDAX = "/Users/shabaldinalidiia/git/Big-Data/pyspark-app/result/dax"

#create SparkSession
spark = (SparkSession.
            builder.
            appName("pyspark_driver").
            getOrCreate())

#read infections info and return dataframe using an infered schema
corona_in = spark.read.option("header", "true") \
        .option("inferSchema", "true") \
        .option("delimiter", ";") \
        .csv(inputInfections)

#read DAX info and return dataframe using an infered schema
dax_in = spark.read.option("header", "true") \
        .option("inferSchema", "true") \
        .option("delimiter", ";") \
        .csv(inputDAX)

#regester dataframe as temporary view for querieng and transforming it
corona_in.createOrReplaceTempView("corona_in")
dax_in.createOrReplaceTempView("dax_in")

#for debugging purpose
print(corona_in.printSchema())     
corona_in.show(10)
print(dax_in.printSchema())     
dax_in.show(10)

#TODO calculate relative difference to previous day
corona_out = corona_in.select(to_date('dateRep', format='dd/MM/yyyy').alias('date'), 
                            corona_in.cases,
                            corona_in.deaths,
                            corona_in.countriesAndTerritories.alias('country'),
                            corona_in.continentExp.alias('continent'))
                            
corona_out.show()


#calculate DAX value as a total ammount of all stock values
dax = dax_in.select(sum(dax_in.Open).alias('open_sum'), 
                        sum(dax_in.Close).alias('close_sum'))

#add a column to store difference between open and close values 
#add a date coulmn assuming the DAX values are from previous date
dax_out = dax.withColumn("abs_diff", expr("close_sum - open_sum")).withColumn("date", date_sub(current_date(), 1))

#for debugging
dax_out.show()

# write the results to hdfs
corona_out.write.format("csv").option("header", "false").mode("append").save(outputFileCorona)
dax_out.write.format("csv").option("header", "false").mode("append").save(outputFileDAX)


#close SparkSession
spark.stop()


