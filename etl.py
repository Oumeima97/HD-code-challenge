import pytrends
from pytrends.request import TrendReq
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
import pandas as pd
from dotenv import load_dotenv
from S3 import connect_bucket, upload_data, get_env_var

#Getting env variables (S3 credentials)
aws_access_key_id, aws_secret_access_key, region_name = get_env_var()
#Initializing S3 bucket
s3 = connect_bucket(aws_access_key_id, aws_secret_access_key, region_name)
bucket_name = s3.buckets.all()[0]
#Initializing years period
years_period = 5
past_date = datetime.now() - relativedelta(years=years_period)
past_date = past_date.date()
#Initializing keywords list
kw_list = [["devops"], ["machine learning"], ["web dev"], ["artificial intelligence"], ["big data"]] # list of keywords to get data
#pytrends = TrendReq(hl='en-US', tz=60)
for keyword in kw_list:
    pytrends = TrendReq(hl='en-US', tz=60, timeout=(10,25), retries=2, backoff_factor=0.1, requests_args={'verify':False})
    pytrends.build_payload(keyword, cat=0, timeframe=f'{past_date} {date.today()}', geo='en-US', gprop='') 

    data = pytrends.interest_over_time() 
    data = data.reset_index()

    json = data.to_json()
    #Upload to bucket
    filename = '{keyword}.json'
    upload_data(s3, bucket_name, json, filename)
