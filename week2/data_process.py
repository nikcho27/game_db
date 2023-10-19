import pandas as pd
import os
import mysql.connector
from sqlalchemy import create_engine

# Define your MySQL database connection parameters
host = 'localhost'
user = 'root'
password = '2942123'
database = 'game_db'

# Create a MySQL database connection using mysql.connector
conn = mysql.connector.connect(
    host=host,
    user=user,
    password=password,
    database=database
)
# Specify the directory where your CSV files are located
directory = 'week2/entities_csv'

# Create an empty dictionary to store dataframes
dataframes = {}

def print_df(name, df):
    print('This is table ' + name)
    num_rows, num_columns = df.shape
    # we only care about num rows right now
    print(f"Number of rows: {num_rows}")


# First I process the entities
for filename in os.listdir(directory):
    if filename.endswith('.csv'):
        # Load each CSV file into a separate dataframe
        df = pd.read_csv(os.path.join(directory, filename))
        
        # Use the filename (without the .csv extension) as the key for the dataframe
        key = os.path.splitext(filename)[0]
        dataframes[key] = df

#get rid of null value rows and remove duplicate for the primary key
for key, df in dataframes.items():
    #print size of df beofre first filtering
    print_df(key, df)
        
    # Remove rows with any null value
    df.dropna(inplace=True)  

    # make sure that those columns are unique    
    df.drop_duplicates(subset=[key+'_id'], inplace=True)
    
    #print sie of df after filtering
    print_df(key, df)


#additionally following 3 constraints:
#character-> player_id, kingdom_id -> if character is referencing a kingdom or player then character does not exist
character_df = dataframes['character']
player_df = dataframes['player']
kingdom_df = dataframes['kingdom']
event_df = dataframes['event']
team_df = dataframes['team']

#Create and apply mask
mask = character_df['player_id'].isin(player_df['player_id']) & character_df['kingdom_id'].isin(kingdom_df['kingdom_id'])
dataframes['character'] = character_df[mask]

#event -> kingdom_id -> if event is referencing a kingdom_id that does not exist -> the event does not exist
mask = event_df['kingdom_id'].isin(kingdom_df['kingdom_id'])
dataframes['event'] = event_df[mask]

#team -> kingdom_id -> same logic for team as event
mask = team_df['kingdom_id'].isin(kingdom_df['kingdom_id'])
dataframes['team'] = team_df[mask]

# Create a SQLAlchemy engine to connect to the database
engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

# Insert the entity DataFrames into the MySQL database

#define order of insertion to avoid anomalies:
order_tables = ['player', 'npc', 'class', 'enemy', 'guild', 'item', 'kingdom', 'quest', 'question', 'team', 'event', 'character']
for table_name in order_tables:
    # Insert each entity into game_db
    df = dataframes[table_name]
    print(df)
    df.to_sql(name=table_name, con=engine, if_exists='append', index=False)
