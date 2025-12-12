import pandas as pd
import os

folder = 'output/jaren'
jaren_folders = [f for f in os.listdir(folder)]

file_zelfde_adres = '7_analyse_clusters_zelfde_adres.xlsx'
file_100m = '14_analyse_clusters_straal_100m.xlsx'
file_master = '5_master_ul_dir.xlsx'
file_units = '8_analyse_units.xlsx'

data_zelfde_adres = []
data_100m = []
data_master = []
data_units = []

for jaar in jaren_folders:
    file_path_zelfde_adres = os.path.join(folder, jaar, file_zelfde_adres)
    df_zelfde_adres = pd.read_excel(file_path_zelfde_adres)
    df_zelfde_adres['jaar'] = str(jaar)
    data_zelfde_adres.append(df_zelfde_adres)

    file_path_100m = os.path.join(folder, jaar, file_100m)
    df_100m = pd.read_excel(file_path_100m)
    df_100m['jaar'] = str(jaar)
    data_100m.append(df_100m)

    file_path_master = os.path.join(folder, jaar, file_master)
    df_master = pd.read_excel(file_path_master)
    df_master['jaar'] = str(jaar)
    data_master.append(df_master)

    file_path_units = os.path.join(folder, jaar, file_units)
    try:
        df_units = pd.read_excel(file_path_units, sheet_name='Analyse')
        df_units['jaar'] = str(jaar)
        data_units.append(df_units)
    except:
        continue

df_alles_zelfde_adres = pd.concat(data_zelfde_adres, ignore_index=True)
df_alles_100m = pd.concat(data_100m, ignore_index=True)
df_alles_master = pd.concat(data_master, ignore_index=True)
df_alles_units = pd.concat(data_units, ignore_index=True)


with pd.ExcelWriter('output/16_jaren_samen.xlsx') as writer:
    df_alles_master.to_excel(writer, sheet_name='Master', index=False)
    df_alles_zelfde_adres.to_excel(writer, sheet_name='Adres', index=False)
    df_alles_100m.to_excel(writer, sheet_name='Straal 100m', index=False)
    df_alles_units.to_excel(writer, sheet_name='Units', index=False)