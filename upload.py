import os
import pandas as pd
from sqlalchemy import create_engine


class upload_data:
    def __init__(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.data_file = [f for f in os.listdir(self.current_directory) if f.endswith('.csv')]
        self.engine = create_engine('postgresql+psycopg2://sofsys:withus4u!@sofsys.postgres.database.azure.com/postgres',connect_args={'sslmode': 'require'})

    def take_data(self):
        connection = self.engine.raw_connection()
        cursor = connection.cursor()
        cursor.execute('DELETE FROM naver_smart_store_stats WHERE id NOT IN (SELECT MIN(id) FROM naver_smart_store_stats GROUP BY 기준일);')
        
        data = self.data_file[0]
        df = pd.DataFrame(pd.read_csv(data))

        try :
            df.to_sql('naver_smart_store_stats', self.engine, if_exists='append', index=False, index_label='기준일')
        except Exception as e:
            print(e)
        else: 
            file = [f for f in os.listdir(self.current_directory) if f.endswith('.csv')][0]
            os.remove(file)

if __name__ == '__main__':
    upload = upload_data()
    upload.take_data()