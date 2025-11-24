import pandas as pd
import numpy as np
from sklearn.cluster import DBSCAN
from scipy.spatial.distance import pdist

radius = 100

df = pd.read_excel('5_master_ul_dir.xlsx')
df = df[(df['lx'].notna()) & (df['aantal_inschrijvingen_vp'].notna())]

coords = df[['lx', 'ly']]

clustering = DBSCAN(eps=radius, min_samples=2, metric='euclidean').fit(coords)

df['cluster'] = clustering.labels_

df_clusters = df[df['cluster'] != -1].copy()
df_clusters['coords'] = list(zip(df_clusters['lx'], df_clusters['ly']))
df_clusters = df_clusters.groupby(['cluster', 'schoolbestuur']).agg(
    vestigingsplaatsen = ('vestigingsplaats', lambda vp: '_'.join(vp.astype(str))),
    lx = ('lx', 'mean'),
    ly = ('ly', 'mean'),
    max_afstand = ('coords', lambda c: pdist(np.array(list(c))).max() if len(c) > 1 else 0)
).reset_index()

df_enkel = df[df['cluster'] == -1].rename(
    columns={
        'vestigingsplaats': 'vestigingsplaatsen'
    }
)
df_enkel['vestigingsplaatsen'] = df_enkel['vestigingsplaatsen'].astype(str)

df_clusters = df_clusters[['vestigingsplaatsen', 'lx', 'ly', 'schoolbestuur', 'max_afstand']]
df_enkel = df_enkel[['vestigingsplaatsen', 'lx', 'ly', 'schoolbestuur']]

df_volledig = pd.concat([df_clusters, df_enkel])
df_volledig = df_volledig.rename(
    columns={
        'vestigingsplaatsen': 'cluster'
    }
)
df_volledig.to_excel('13_vestigingsplaatsen_binnen_straal_100m.xlsx', index=False)