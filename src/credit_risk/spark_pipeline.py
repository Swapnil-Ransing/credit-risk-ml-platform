
import csv
from pathlib import Path

from pyspark.sql import SparkSession
from pyspark.sql.types import (
    StructType,
    StructField,
    StringType,
    IntegerType,
    LongType,
    DoubleType,
)

DATA_PATH = "data/raw/application_train.csv"

def create_spark_session():
    return (
        SparkSession.builder
        .appName("HomeCreditRiskPipeline")
        .master("local[*]")
        .config("spark.sql.shuffle.partitions", "4")
        .getOrCreate()
    )

def build_schema(csv_path):
    # Read only the CSV header using Python.
    with open(csv_path, "r", encoding="utf-8-sig", newline="") as f:
        columns = next(csv.reader(f))

    # Explicit types for important columns.
    type_mapping = {
        "SK_ID_CURR": LongType(),
        "TARGET": IntegerType(),
        "AMT_INCOME_TOTAL": DoubleType(),
        "AMT_CREDIT": DoubleType(),
        "AMT_ANNUITY": DoubleType(),
        "DAYS_BIRTH": IntegerType(),
    }

    fields = [
        StructField(
            column,
            type_mapping.get(column, StringType()),
            True
        )
        for column in columns
    ]

    return StructType(fields)

def main():
    spark = create_spark_session()

    schema = build_schema(DATA_PATH)

    df = (
        spark.read
        .option("header", True)
        .option("mode", "FAILFAST")
        .option("nullValue", "")
        .schema(schema)
        .csv(DATA_PATH)
    )

    print("Dataset schema:")
    df.printSchema()

    print("Total rows:", df.count())
    print("Total columns:", len(df.columns))

    print("First five records:")
    df.show(5, truncate=False)
    
    # Transformation 1: Select important columns
    selected_df = df.select(
        "SK_ID_CURR",
        "TARGET",
        "AMT_INCOME_TOTAL",
        "AMT_CREDIT",
    )

    # Transformation 2: Filter default applications
    default_df = selected_df.filter(
        selected_df.TARGET == 1
    )

    # Transformation 3: Create income in lakhs
    from pyspark.sql.functions import col

    result_df = default_df.withColumn(
        "INCOME_LAKH",
        col("AMT_INCOME_TOTAL") / 100000
    )

    # Action
    result_df.show(10, truncate=False)

    print("Default applications:", result_df.count())
    
    # Null sumary of entire df
    null_summary = calculate_null_summary(df)
    null_summary.show(truncate=False)

    spark.stop()
    

from pyspark.sql.functions import col, sum, when

def calculate_null_summary(df):

    expressions = [
        sum(
            when(col(c).isNull(), 1).otherwise(0)
        ).alias(c)
        for c in df.columns
    ]

    null_counts = df.agg(*expressions)

    return null_counts

if __name__ == "__main__":
    main()