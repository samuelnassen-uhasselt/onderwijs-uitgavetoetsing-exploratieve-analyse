import pandas as pd

def cluster_in_unit(cluster, units):
    cluster_vps = cluster.split('_')

    for u in units:
        unit = u.replace('SO_', '')
        unit_vps = unit.split('_')

        if all(item in unit_vps for item in cluster_vps):
            return u

def is_in_unit(unit):
    if pd.notna(unit):
        return True
    return False

df_units = pd.read_excel('output/jaren/2024-2025/8a_analyse_units.xlsx')

df_clusters_100m = pd.read_excel('output/16b_analyse_jaren_100m.xlsx')
df_clusters_100m = df_clusters_100m[['cluster', 'jaar', 'aantal_sn', 'llngroepen_diff']]
df_clusters_100m['unit_code_so'] = df_clusters_100m.apply(lambda row: cluster_in_unit(row['cluster'], df_units['unit_code_so'].values), axis=1)
df_clusters_100m['is_in_unit'] = df_clusters_100m['unit_code_so'].apply(is_in_unit)

df_clusters_adres = pd.read_excel('output/16a_analyse_jaren_zelfde_adres.xlsx')
df_clusters_adres = df_clusters_adres[['cluster', 'jaar', 'aantal_sn', 'llngroepen_diff']]
df_clusters_adres['unit_code_so'] = df_clusters_adres.apply(lambda row: cluster_in_unit(row['cluster'], df_units['unit_code_so'].values), axis=1)
df_clusters_adres['is_in_unit'] = df_clusters_adres['unit_code_so'].apply(is_in_unit)

with pd.ExcelWriter('output/20_clusters_in_units.xlsx') as writer:
    df_clusters_100m.to_excel(writer, sheet_name='STRAAL 100M', index=False)
    df_clusters_adres.to_excel(writer, sheet_name='ADRES', index=False)