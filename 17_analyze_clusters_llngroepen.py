import pandas as pd
import ast
import re

df_adres = pd.read_excel('output/16a_analyse_jaren_zelfde_adres.xlsx')
df_straal = pd.read_excel('output/16b_analyse_jaren_100m.xlsx')

def get_llngroepen_aantal(llngroepen):
    result = {}
    llngroepen = re.sub(r'\bnan\b', 'None', llngroepen)
    llngroepen = ast.literal_eval(llngroepen)

    for key, value in llngroepen.items():
        for llngr in value.keys():
            result[llngr] = result.get(llngr, 0) + 1

    return result

def get_exploded_df(df, column_names, aantal_column):
    rows = []
    for idx, row in df.iterrows():
        dict_col = row[aantal_column]
        
        if isinstance(dict_col, dict):
            all_keys = set(dict_col.keys())
            
            for key in all_keys:
                new_row = {}
                for c in column_names:
                    new_row[c] = row[c]
                new_row['leerlingengroep'] = key
                new_row[aantal_column] = dict_col.get(key, 0)
                rows.append(new_row)

    df_exploded = pd.DataFrame(rows)
    return df_exploded

df_adres['llngr_aantallen'] = df_adres['leerlingengroepen'].apply(get_llngroepen_aantal)
df_adres_exploded = get_exploded_df(df_adres, ['cluster', 'jaar'], 'llngr_aantallen')
df_adres_exploded.to_excel('17a_analyse_adres_leerlingengroepen.xlsx', index=False)


df_straal['llngr_aantallen'] = df_straal['leerlingengroepen'].apply(get_llngroepen_aantal)
df_straal_exploded = get_exploded_df(df_straal, ['cluster', 'jaar'], 'llngr_aantallen')
df_straal_exploded.to_excel('output/17b_analyse_straal_100m_leerlingengroepen.xlsx', index=False)