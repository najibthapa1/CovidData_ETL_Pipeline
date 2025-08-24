import sys
import os
import time
import psycopg2
from pyspark.sql import SparkSession

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utility.utility import setup_logging, format_time


def create_spark_session():
    """Initialize a Spark session."""
    spark = (
        SparkSession.builder
        .appName("COVID19 Load")
        .config(
            "spark.jars",
            "/Users/najibthapa1/Documents/College/bigdata/pyspark/venv/lib/python3.12/site-packages/pyspark/jars/postgresql-42.7.7.jar"
        )
        .config("spark.driver.host", "127.0.0.1")  # <- avoid loopback issues on macOS
        .getOrCreate()
    )
    return spark


def create_postgres_tables(pg_un, pg_pw):
    """Create PostgreSQL tables if they don't exist."""
    cursor = None
    conn = None
    try:
        conn = psycopg2.connect(
            dbname="postgres",
            user=pg_un,
            password=pg_pw,
            host="localhost",
            port="5432"
        )
        cursor = conn.cursor()

        table_queries = [
            """
            CREATE TABLE IF NOT EXISTS daily_country (
                country TEXT,
                continent TEXT,
                date DATE,
                total_cases BIGINT,
                total_deaths BIGINT,
                population LONG
            );
            """,
            """
            CREATE TABLE IF NOT EXISTS daily_nepal (
                country TEXT,
                continent TEXT,
                date DATE,
                total_cases BIGINT,
                total_deaths BIGINT,
                population LONG
            );
            """
        ]

        for query in table_queries:
            cursor.execute(query)
        conn.commit()
        logger.info("PostgreSQL tables created successfully.")

    except Exception as e:
        logger.warning(f"Error creating tables: {e}")
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


def load_to_postgres(spark, input_dir, pg_un, pg_pw):
    """Load cleaned COVID Parquet files to PostgreSQL."""
    jdbc_url = "jdbc:postgresql://localhost:5432/postgres"
    connection_properties = {
        "user": pg_un,
        "password": pg_pw,
        "driver": "org.postgresql.Driver"
    }

    # Updated paths & table names to match Transform output
    tables = [
        ("stage2/daily_country", "daily_country"),
        ("stage2/daily_nepal", "daily_nepal")
    ]

    for parquet_path, table_name in tables:
        try:
            df = spark.read.parquet(os.path.join(input_dir, parquet_path))
            df.write \
                .mode("overwrite") \
                .jdbc(jdbc_url, table_name, properties=connection_properties)
            logger.info(f"Loaded {table_name} to PostgreSQL")
        except Exception as e:
            logger.warning(f"Error loading {table_name}: {e}")


if __name__ == "__main__":
    logger = setup_logging("load.log")
    if len(sys.argv) != 4:
        logger.error("Usage: python execute.py <input_dir> <pg_un> <pg_pw>")
        sys.exit(1)

    input_dir = sys.argv[1]
    pg_un = sys.argv[2]
    pg_pw = sys.argv[3]

    if not os.path.exists(input_dir):
        logger.error(f"Input directory {input_dir} does not exist.")
        sys.exit(1)

    logger.info("Load stage started")
    start = time.time()

    spark = create_spark_session()
    create_postgres_tables(pg_un, pg_pw)
    load_to_postgres(spark, input_dir, pg_un, pg_pw)

    end = time.time()
    logger.info("Load stage completed")
    logger.info(f"Total time taken: {format_time(end - start)}")