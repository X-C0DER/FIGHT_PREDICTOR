import pandas as pd
import json

def load_data(fighter1, fighter2):
    # Load data from "fighter1_data.json"
    filename1 = f"{fighter1}_data.json"
    with open(filename1) as f1:
        data1 = json.load(f1)

    filename2 = f"{fighter2}_data.json"
    with open(filename2) as f2:
        data2 = json.load(f2)

    if 'H2H' in data1 and any(data1['H2H']) and 'H2H' in data2 and any(data2['H2H']):
        # Remove empty dictionaries from 'H2H'
        data1['H2H'] = [item for item in data1['H2H'] if item]
        
        data2['H2H'] = [item for item in data2['H2H'] if item]

        detail=data1['Fighter_Detail']
        detail2=data2['Fighter_Detail']

        df1 = {"Fighter_Detail":detail,fighter1+'_H2H': serialize_data(data1)}
        df2 = {"Fighter_Detail_2":detail2,fighter2+'_H2H': serialize_data(data2)}

        # Save the combined data to a JSON file
        output_filename = f"{fighter1}_vs_{fighter2}.json"
        with open(output_filename, 'w') as outfile:
            json.dump({**df1, **df2}, outfile, indent=4)

        print(f"Combined data saved to {output_filename}")
    else:
        print(f"No non-empty H2H data available for {fighter1} and/or {fighter2}.")

def serialize_data(data):
    df = pd.json_normalize(data, record_path=['H2H'])

    # Extract the second entry in the 'FIGHTER' and 'EVENT' sections
    df['FIGHTER_1_RESULT'] = df['W/L'].apply(lambda x: x[0])
    df['FIGHTER_1'] = df['FIGHTER'].apply(lambda x: x[0])
    df['FIGHTER_2'] = df['FIGHTER'].apply(lambda x: x[1])

    # Check if the 'EVENT' column contains float values
    if df['EVENT'].apply(lambda x: isinstance(x, float)).any():
        df['EVENT_DATE'] = df['EVENT'].apply(lambda x: x[1] if isinstance(x, list) and len(x) > 1 else None)
        df['EVENT_NAME'] = df['EVENT'].apply(lambda x: x[0] if isinstance(x, list) and len(x) > 0 else None)
    else:
        df['EVENT_DATE'] = df['EVENT'].apply(lambda x: x[1])
        df['EVENT_NAME'] = df['EVENT'].apply(lambda x: x[0])

    df['ROUND'] = df['ROUND'].apply(lambda x: x[0])
    df['TIME'] = df['TIME'].apply(lambda x: x[0])
    df['WIN_METHOD'] = df['METHOD'].apply(lambda x: x[0])

    for feature in ['KD', 'STR', 'TD', 'SUB']:
        df[f'{feature}_FIGHTER_1'] = df.apply(lambda row: row[feature][0] if isinstance(row[feature], list) and len(row[feature]) > 0 else None, axis=1)
        df[f'{feature}_FIGHTER_2'] = df.apply(lambda row: row[feature][1] if isinstance(row[feature], list) and len(row[feature]) > 1 else None, axis=1)

    df2 = df[['FIGHTER_1_RESULT', 'FIGHTER_1', 'FIGHTER_2', 'EVENT_NAME', 'EVENT_DATE', 'KD_FIGHTER_1', 'KD_FIGHTER_2', 'STR_FIGHTER_1', 'STR_FIGHTER_2', 'TD_FIGHTER_1', 'TD_FIGHTER_2', 'SUB_FIGHTER_1', 'SUB_FIGHTER_2', 'WIN_METHOD', 'ROUND', 'TIME']].astype(str)

    df_dict = df2.to_dict(orient='records')

    return df_dict

# Get fighter names as input
fighter1 = "Ketlen Vieira"
fighter2 = "Johnny Walker"

load_data(fighter1, fighter2)
