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

#spark.sparkContext.setLogLevel('WARN')

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


#for debugging
print(corona_in.printSchema())     
corona_in.show(10)
print(dax_in.printSchema())     
dax_in.show(10)

#select only necessary rows
corona = corona_in.select(to_date('dateRep', format='dd/MM/yyyy').alias('date'), 
                            corona_in.cases,
                            corona_in.deaths,
                            corona_in.countriesAndTerritories.alias('country'),
                            corona_in.continentExp.alias('continent'),)
                            
#calculate relative difference to previous day for number of cases and death
corona1 = corona.withColumn("prev_date", date_sub(corona.date, 1))

#regester dataframe as temporary view for querieng and transforming it
corona1.createOrReplaceTempView("corona_out")
corona1.show(10)

corona_out1 = spark.sql("SELECT cor1.date, cor1.cases, cor1.deaths, cor1.prev_date, cor2.cases as cases_prev, cor2.deaths as dead_prev FROM corona_out as cor1  LEFT OUTER JOIN  corona_out as cor2 on cor2.date = cor1.prev_date and cor1.country=cor2.country")
corona_out1.show(10)

corona_out = corona_out1.withColumn("cases_rel_diff", expr("(cases-cases_prev)/cases_prev")).withColumn("deaths_rel_diff", expr("(deaths-dead_prev)/dead_prev"))
corona_out.show(10)

#calculate DAX value as a total ammount of all stock values
dax = dax_in.select(sum(dax_in.Open).alias('open_sum'), 
                        sum(dax_in.Close).alias('close_sum'))

#add a column to store difference between open and close values 
#add a date coulmn assuming the DAX values are from previous date
dax_out = dax.withColumn("abs_diff", expr("close_sum - open_sum")).withColumn("date", date_sub(current_date(), 1))

#for debugging
dax_out.show()

# write the results to hdfs
#TODO file name
corona_out.write.format("csv").option("header", "true").mode("append").save(outputFileCorona)
dax_out.write.format("csv").option("header", "true").mode("append").save(outputFileDAX)


#TODO results into mySQL DB

#close SparkSession
spark.stop()


