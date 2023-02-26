from pyspark.sql import SparkSession

if __name__ == '__main__':
    spark = SparkSession.builder.appName("elt-lakehouse-spok").getOrCreate()

    s3_input_users_path = 's3a://spok-landing/users/*'
    s3_output_users_path = 's3a://spok-lakehouse/bronze/users'

    # read users
    df_users = spark.read\
        .format('json')\
        .option('inferSchema', 'true')\
        .option('header','true')\
        .json(s3_input_users_path)

    # convert to delta format
    df_users\
        .write\
        .mode('overwrite')\
        .format('delta')\
        .save(s3_output_users_path)

    spark.stop()