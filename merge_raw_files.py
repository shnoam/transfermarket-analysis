import pandas as pd
import json

def merge_raw_batch_files():
    # Define file paths and output filenames
    folder = "scraped_files"
    players_csv_files = [f'{folder}/df_players_batch_{i}.csv' for i in range(1, 6)]
    mv_json_files = [f'{folder}/mv_batch_{i}.json' for i in range(1, 6)]
    transfers_json_files = [f'{folder}/transfers_batch_{i}.json' for i in range(1, 6)]
    output_folder = "scraped_data_combined"
    output_csv = f'{output_folder}/all_players_data.csv'
    output_json_mv = f'{output_folder}/all_mv_data.json'
    output_json_transfers = f'{output_folder}/all_transfers_data.json'

    ## process players_data
    csv_dfs = []
    for csv_file in players_csv_files:
        df_csv = pd.read_csv(csv_file)
        csv_dfs.append(df_csv)
    merged_players_df = pd.concat(csv_dfs, ignore_index=True)

    # Save merged player data to CSV
    merged_players_df.to_csv(output_csv, index=False, encoding='utf-8-sig')

    ## process market value development data

    mv_json_data = []
    for json_file in mv_json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
            mv_json_data.extend(data)
    # Save merged market value development data to JSON
    with open(output_json_mv, 'w') as file:
        json.dump(mv_json_data, file)

    # Load JSON files for transfer history
    transfers_json_data = []
    for json_file in transfers_json_files:
        with open(json_file, 'r') as file:
            data = json.load(file)
            transfers_json_data.extend(data)
    # Save merged transfer history data to JSON
    with open(output_json_transfers, 'w') as file:
        json.dump(transfers_json_data, file)

merge_raw_batch_files()



