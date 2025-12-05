import pandas as pd
import networkx as nx
import sys

# Gebruik inschrijvingen tabel voor adressen
df_vestigingen = pd.read_excel(f'output/jaren/{sys.argv[1]}/3_vestigingsplaatsen_master.xlsx')

# Filter vestgingsplaatsen weg zonder adres
df_vestigingen = df_vestigingen[df_vestigingen['vestigingsplaats_adres'].notna()]

# Maak paren
df_zelfde = pd.merge(df_vestigingen, df_vestigingen, how='inner', on='vestigingsplaats_adres',suffixes=['_1', '_2'])
df_zelfde = df_zelfde[df_zelfde['vestigingsplaats_1'] != df_zelfde['vestigingsplaats_2']]

# Filter paren weg met verschillend bestuur
df_zelfde = df_zelfde[df_zelfde['schoolbestuur_1'] == df_zelfde['schoolbestuur_2']]

df_zelfde.to_excel(f'output/jaren/{sys.argv[1]}/6a_vestigingen_zelfde_adres_bestuur.xlsx', index=False)


# Maak een graaf. Hierbij verbinden we alle paren van scholen die binnen een aftand van 200m van elkaar liggen, zoals eerder bepaald.
G = nx.Graph()
for _, row in df_zelfde.iterrows():
    G.add_edge(row['vestigingsplaats_1'], row['vestigingsplaats_2'])


# Vorm de clusters
clusters = list(nx.connected_components(G))

cluster_data = []
cluster_instellingen = []
for cluster in clusters:
    cluster_data.append(
        '_'.join(map(str, sorted(cluster)))
    )
    instellingen = sorted(list(set([int(str(id)[:-2]) for id in cluster])))
    cluster_instellingen.append(
        '_'.join(map(str, instellingen))
    )

df_clusters = pd.DataFrame(list(zip(cluster_data, cluster_instellingen)), columns=['cluster', 'schoolnummers'])
df_clusters.to_excel(f'output/jaren/{sys.argv[1]}/6b_clusters_zelfde_adres_en_bestuur.xlsx', index=False)