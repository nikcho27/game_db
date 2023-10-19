import subprocess

#create new database !MAKE SURE TO CONFIGURE YOUR SETTINGS IN THE SCRIPT
result = subprocess.run(["python", "week2\create_database.py"])
 
if result.returncode == 0:
    print("Database created successfully.")

#use bat script to clean the folder with csv files when 
result = subprocess.run(["week2\entities_csv\clean_folder.bat"], shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print("Script executed successfully.")
    print("Output:")
    print(result.stdout)
    
#use bat script to clean the events_folder with csv files when 
result = subprocess.run(["week2\events_csv\clean_folder.bat"], shell=True, capture_output=True, text=True)

if result.returncode == 0:
    print("Script executed successfully.")
    print("Output:")
    print(result.stdout)

#run the generate_data script 3 times, each time we 'read' the data with data_reader2.py
# and append the appropriate values into a correct csv file stored entities_csv dir
for i in range(3):
    result = subprocess.run(["python", "week2\generate_data.py"])
    if result.returncode == 0:
        print("Data generation executed successfully: " + str(i+1) + " time(s)")
    result = subprocess.run(["python", "week2\data_reader2.py"])
    if result.returncode == 0:
        print("Data reading executed successfully: " + str(i+1) + " time(s)")

#we load the 'read' data into the database by using pandas dataframes and simultaneously handling null values, duplicates,
#foreign key constraints while being mindful of the order of insertion
result = subprocess.run(["python", "week2\data_process.py"])
if result.returncode == 0:
    print("Data has been read into the database successfully")
