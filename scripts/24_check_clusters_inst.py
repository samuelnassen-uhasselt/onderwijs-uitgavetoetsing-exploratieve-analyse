import pandas as pd

df_clusters_100m = pd.read_excel('output\\20_clusters_in_units.xlsx', sheet_name='Straal 100m')
df_clusters_adres = pd.read_excel('output\\20_clusters_in_units.xlsx', sheet_name='Adres')

def get_inst(cluster):
    return '_'.join([vp[:-2] for vp in cluster.split('_')])

def get_analyse(df_in):
    df = df_in[df_in['jaar'] == '2024-2025'].copy()
    df['inst'] = df['cluster'].apply(get_inst)

    def inst_in_ander_cluster(row):
        df_zonder_row = df[df['cluster'] != row['cluster']]
        andere_inst = '_'.join(df_zonder_row['inst'])
        for i in row['inst'].split('_'):
            if i in andere_inst:
                return True
        return False

    df['deelt_inst_ander_cluster'] = df.apply(lambda row: inst_in_ander_cluster(row), axis=1)
    return df

df_clusters_100m = get_analyse(df_clusters_100m)
df_clusters_adres = get_analyse(df_clusters_adres)

with pd.ExcelWriter('output/24_clusters_in_units_inst_check.xlsx') as writer:
    df_clusters_100m.to_excel(writer, sheet_name='Straal 100m', index=False)
    df_clusters_adres.to_excel(writer, sheet_name='Adres', index=False)