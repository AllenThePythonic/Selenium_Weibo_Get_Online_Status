import os
import sys
import matplotlib.pyplot as plt
from datetime import date

# Path for spark source folder
os.environ['SPARK_HOME'] = "/spark-1.6.1-bin-hadoop2.6"

# Append pyspark to Python Path
sys.path.append("/spark-1.6.1-bin-hadoop2.6/python")
sys.path.append("/spark-1.6.1-bin-hadoop2.6/python/lib/py4j-0.9-src.zip")

#
# Main
#

if __name__ == '__main__':

    try:

        from pyspark import SparkContext
        from pyspark import SparkConf
        from operator import add

        print(" -- Daily Report -- ")

        sc = SparkContext('local', 'test')
        log_data = sc.textFile("logfile").cache()

        online_status = log_data.filter(lambda line: str(date.today()) in line).filter(lambda line: "online" in line).map(
            lambda line: (line.replace("at", "").replace("online  ", "").split(" ")[0],
                          line.replace("at", "").replace("online  ", "").split(" ")[1] + " ")).reduceByKey(add).flatMap(
            lambda line: (line[0], line[1].split(" ")))

        print(online_status.collect())

        if len(online_status.collect()) > 0:

            date = online_status.collect()[0]

            rdd = sc.parallelize(list(map(lambda x: (x.split(':')[0], 1), online_status.collect()[1]))).reduceByKey(
                add).filter(lambda line: line[0] != '')
            print(rdd.collect())

            t = [x for x, y in sorted(rdd.collect(), reverse=True)]
            s = [y for x, y in sorted(rdd.collect(), reverse=True)]

            axes = plt.gca()
            axes.set_xlim([0, 23])
            axes.set_ylim([0, max(s) + 1])

            plt.plot(t, s)

            plt.xlabel('Time (h)')
            plt.ylabel('Frequency (t)')
            plt.title(date)
            plt.grid(True)
            plt.savefig("BACKUP_"+ date + "_report.png")
            plt.show()

    except ImportError as e:
        print("Can not import Spark Modules", e)
        sys.exit(1)
