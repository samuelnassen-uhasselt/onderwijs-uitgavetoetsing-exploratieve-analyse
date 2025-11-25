import pandas as pd
from sklearn.cluster import KMeans
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import ast

df_master = pd.read_excel('output/5_master_ul_dir.xlsx')
df_master = df_master[~df_master['vestigingsplaats_adres'].isna()]
df_schoolnummers = df_master.groupby('schoolnummer')['vestigingsplaats'].count()

def get_aantal_vp_schoolnummers(nummers):
    result = 0
    nummers = [int(n) for n in nummers.split('_')]
    for n in nummers:
        result += df_schoolnummers.loc[n]
    return result/len(nummers)

def get_llngr_percent(row):
    llngr = ast.literal_eval(row['leerlingengroepen_cluster'])
    totaal = row['aantal_leerlingen']

    percentages = {}
    for groep, values in llngr.items():
        percentages[groep] = round(values['inschrijvingen']*100/totaal,2)
    
    return dict(sorted(percentages.items(), key=lambda item: item[0]))


df = pd.read_excel('output/7_analyse_clusters_zelfde_adres.xlsx').rename(
    columns={
        'cluster': 'vestingingsplaatsen'
})

df['vp_per_sn'] = df['schoolnummers'].apply(get_aantal_vp_schoolnummers)


lln_clusters_aantal = 12

kmeans = KMeans(n_clusters=lln_clusters_aantal, random_state=42, n_init=10)
df['cluster_lln'] = kmeans.fit_predict(df[['aantal_leerlingen']])

df['llngr_percent'] = df.apply(get_llngr_percent, axis=1)
percent_df = pd.DataFrame(df['llngr_percent'].tolist()).fillna(0)

for col in percent_df.columns:
    df[f'{col}_pct'] = percent_df[col]

pct_cols = [col for col in df.columns if col.endswith('_pct')]
pct_cols.append('aantal_leerlingen')


results = []
for inschr_cluster in range(lln_clusters_aantal):
    subset = df[df['cluster_lln'] == inschr_cluster].copy()

    if len(subset) < 5:
        subset['cluster_groepen'] = -1
        results.append(subset)
        continue

    X = subset[pct_cols]

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    dbscan = DBSCAN(eps=0.5, min_samples=2)
    subset['cluster_groepen'] = dbscan.fit_predict(X_scaled)

    results.append(subset)

df = pd.concat(results).sort_index()

df = df[['adres', 'schoolnummers', 'vp_per_sn', 'bestuur', 'net', 'aantal_leerlingen', 'llngr_percent', 'cluster_lln', 'cluster_groepen', 
         'aantal_sn', 'llngroepen_diff', 'ul_asis', 'ul_cluster', 'ul_diff', 'directeurs_asis', 'directeur_diff']].rename(
             columns={
                 'cluster_lln': 'c_aantal_leerlingen',
                 'cluster_groepen': 'c_leerlingengroepen',
                 'llngroepen_diff': 'gesplitste_leerlingengroepen',
                 'ul_cluster': 'ul_tobe',
             }
         )

df.to_excel('output/10_vergelijkbare_scholen.xlsx', index=False)