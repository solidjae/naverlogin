import os
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql+psycopg2://sofsys:withus4u!@sofsys.postgres.database.azure.com/postgres',connect_args={'sslmode': 'require'})



class upload_data:
    def __init__(self):
        current_directory = os.path.dirname(os.path.abspath(__file__))
        self.data_file = [f for f in os.listdir(current_directory) if f.endswith('.csv')]

    def take_data(self):
        data = self.data_file[0]
        df = pd.DataFrame(pd.read_csv(data))
        print(len(df.columns))
        


if __name__ == '__main__':
    upload = upload_data()
    upload.take_data()