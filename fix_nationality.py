import ast

import pandas as pd

def process_nationality(csv_file):
    # Read CSV file into DataFrame
    df = pd.read_csv(csv_file)

    # Process "Nationality" column

    def process_national_team(nat, country_birth):
        if pd.isna(nat):
            return country_birth
        parts = nat.split(' ')
        for i in range(len(parts)):
            if parts[i].startswith('U') and parts[i][1:].isdigit():
                return ' '.join(parts[:i])
        return nat

    df['Nationality'] = df.apply(lambda row: process_national_team(row['Nationality'], row['Country of Birth']), axis=1)

    # Save the processed DataFrame back to CSV
    processed_csv_file = csv_file.split('.')[0] + '_processed.csv'
    df.to_csv(processed_csv_file, index=False, encoding='utf-8-sig')

    return processed_csv_file

# Example usage:
csv_file = 'all_players_data.csv'  # Replace 'example.csv' with your CSV file
processed_file = process_nationality(csv_file)
print(f'Processed file saved as: {processed_file}')