import os
import pandas as pd
from sqlalchemy import create_engine

class UploadData:
    def __init__(self):
        self.current_directory = os.path.dirname(os.path.abspath(__file__))
        self.data_file = [f for f in os.listdir(self.current_directory) if f.endswith('.csv')]
        self.engine = create_engine('postgresql+psycopg2://sofsys:withus4u!@sofsys.postgres.database.azure.com/postgres', connect_args={'sslmode': 'require'})

    def take_data(self):
        if self.data_file:
            data = self.data_file[0]
            df = pd.read_csv(os.path.join(self.current_directory, data))

            with self.engine.begin() as connection:
                # Assuming '기준일' is the column based on which you want to avoid duplicates.
                # Construct a list of unique '기준일' values from the DataFrame
                unique_dates = df['기준일'].unique().tolist()

                # Generate a query to delete existing records that might duplicate
                # Convert the list of dates to a string of comma-separated values for the SQL query
                unique_dates_str = ",".join(f"'{date}'" for date in unique_dates)
                
                # Execute the delete query - adjust '기준일' and 'naver_smart_store_stats' as necessary
                delete_query = f"DELETE FROM naver_smart_store_stats WHERE 기준일 IN ({unique_dates_str})"
                connection.execute(delete_query)
                
                # Insert new data from DataFrame
                try:
                    df.to_sql('naver_smart_store_stats', connection, if_exists='append', index=False)
                except Exception as e:
                    print(f"An error occurred: {e}")

            # Optionally, remove the processed CSV file
            os.remove(os.path.join(self.current_directory, data))

if __name__ == '__main__':
    uploader = UploadData()
    uploader.take_data()
