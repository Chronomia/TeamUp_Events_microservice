import pandas as pd
from datetime import datetime
import random

# Function to adjust time format and add randomness
def adjust_time(time_str):
    # Remove 'Z' from the end of the string if it's present
    if time_str.endswith('Z'):
        time_str = time_str[:-1]

    # Convert to datetime object
    dt = datetime.fromisoformat(time_str)

    # Ensure the year is 2023 and the time is in full hours (US day time)
    random_hour = random.randint(6, 18)  # US day time hours (6 AM to 6 PM)
    new_dt = dt.replace(year=2023, hour=random_hour, minute=0, second=0, microsecond=0)

    # Convert back to ISO format string
    return new_dt.isoformat()

# Load your CSV file
file_path = 'mock_data.csv'  # Replace with your file path
df = pd.read_csv(file_path)

# Apply the function to the 'time' column
df['time'] = df['time'].apply(adjust_time)

# Now df contains the updated time column
 
updated_file_path = 'mock_data.csv'  
df.to_csv(updated_file_path, index=False)
