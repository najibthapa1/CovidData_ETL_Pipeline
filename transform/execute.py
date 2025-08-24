import sys
import os
import time
from pyspark.sql import SparkSession
from pyspark.sql import functions as F

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utility.utility import setup_logging, format_time


def create_spark_session():
    """Initialize a Spark session."""
    return SparkSession.builder \
        .appName("ETL Transform") \
        .getOrCreate()


def load_and_clean(spark, input_dir, output_dir, logger):
    """Stage 1: Load OWID COVID dataset, select needed cols, save cleaned data."""

    # Load the dataset
    covid_df = spark.read.csv(
        os.path.join(input_dir, "compact.csv"),
        header=True,
        inferSchema=False  # read all as string first
    )

    # Replace string "null" with actual None for numeric columns
    for col_name in ["total_cases", "total_deaths"]:
        covid_df = covid_df.withColumn(
            col_name,
            F.when(F.col(col_name).isin("null", ""), None).otherwise(F.col(col_name))
        )

    # Select required columns, cast, and parse date
    covid_df = covid_df.select(
        F.col("country"),
        F.col("continent"),
        F.to_date(F.col("date"), "dd/MM/yyyy").alias("date"),
        F.col("total_cases").cast("double"),
        F.col("total_deaths").cast("double"),
        F.col("population").cast("long")
    )

    # Filter null country, continent, or date
    covid_df = covid_df.filter(
        F.col("country").isNotNull() & F.col("continent").isNotNull() & F.col("date").isNotNull()
    )

    # Save Stage 1 cleaned data
    covid_df.write.mode("overwrite").parquet(os.path.join(output_dir, "stage1", "covid_data"))

    logger.info("Stage 1: Cleaned OWID data saved")
    return covid_df

def create_aggregated_tables(output_dir, covid_df, logger):
    """Stage 2: Aggregate by country and date (keep totals as-is)."""

    # Just keep the dataset ordered
    daily_country = covid_df.orderBy("country", "date")
    daily_country.write.mode("overwrite").parquet(os.path.join(output_dir, "stage2", "daily_country"))
    logger.info("Stage 2: Aggregated daily country data saved")

    # Save Nepal subset
    daily_nepal = daily_country.filter(F.col("country") == "Nepal")
    daily_nepal.write.mode("overwrite").parquet(os.path.join(output_dir, "stage2", "daily_nepal"))
    logger.info("Stage 2: Aggregated Nepal data saved")

    # Debug output
    print("Daily Country Schema:")
    daily_country.printSchema()
    daily_country.show(5, truncate=False)

    print("Daily Nepal Schema:")
    daily_nepal.printSchema()
    daily_nepal.show(5, truncate=False)


if __name__ == "__main__":
    logger = setup_logging("transform.log")

    if len(sys.argv) != 3:
        logger.error("Usage: python execute.py <input_dir> <output_dir>")
        sys.exit(1)

    logger.info("Transform stage started")
    start = time.time()

    input_dir = sys.argv[1]
    output_dir = sys.argv[2]

    spark = create_spark_session()

    covid_df = load_and_clean(spark, input_dir, output_dir, logger)
    create_aggregated_tables(output_dir, covid_df, logger)

    end = time.time()
    logger.info(f"Transformation pipeline completed in {format_time(end - start)}")