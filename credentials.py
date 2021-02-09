import os
from dotenv import load_dotenv

load_dotenv()

host = str(os.getenv('H_HOST'))
user = str(os.getenv('H_USER'))
passwd = str(os.getenv('H_PASSWORD'))
database = str(os.getenv('H_DB'))

api_key = str(os.getenv('API_KEY'))
