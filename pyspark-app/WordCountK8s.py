# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
# WordCount for K8s


# %%
from pyspark.sql import SparkSession


# %%
# inputFile = "hdfs://hadoop-hadoop-hdfs-nn:9000/input/Boston_Housing_Data.csv"
inputFile = "/Users/shabaldinalidiia/git/Big-Data/pyspark-app/Boston_Housing_Data.csv"


# %%
# outputFile = "hdfs://hadoop-hadoop-hdfs-nn:9000/tmp/Test_LS.txt"
outputFile = "/Users/shabaldinalidiia/git/Big-Data/pyspark-app/Test_LS.txt"


# %%
#create a SparkSession without local master and app name
spark = (SparkSession.builder.getOrCreate())
# read file 
spark.sparkContext.setLogLevel("ERROR")
input = spark.sparkContext.textFile(inputFile)
counts = input.flatMap(lambda line : line.split(" ")).map(lambda word : [word, 1]).reduceByKey(lambda a, b : a + b)


# %%
# write the result to hdfs
counts.saveAsTextFile(outputFile)


# %%
print(counts.collect())


# %%
spark.stop()

