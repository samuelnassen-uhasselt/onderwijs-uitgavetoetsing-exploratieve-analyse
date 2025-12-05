import pandas as pd
import ast
import numpy as np
import degressieve_ul_llngroepen as dul
import sys

df_clusters = pd.read_excel(f'jaren/{sys.argv[1]}/13_vestigingsplaatsen_binnen_straal_100m.xlsx')
df_vestigingen = pd.read_excel(f'jaren/{sys.argv[1]}/5_master_ul_dir.xlsx')
df_vp_index = df_vestigingen.set_index('vestigingsplaats')
df_inschrijvingen_adres = pd.read_excel(f'jaren/{sys.argv[1]}/1a_inschrijvingen_vestigingsplaatsen_llngroepen_aantal.xlsx')
df_inschrijvingen_index = df_inschrijvingen_adres.set_index('vestigingsplaats')

def get_schoolnummers(vps):
    sns = list(set([vp[:-2] for vp in vps.split('_')]))
    return '_'.join(sns)

def get_net(vps):
    result = []
    for vp in vps.split('_'):
        try:
            net = df_vp_index.loc[int(vp), 'net']
            result.append(net)
        except:
            result.append(np.nan)
    result = [i for i in result if pd.notna(i)]
    result = list(set(result))
    if len(result) == 1:
        return result[0]
    return result

def get_aantal_vp(cluster):
    return len(cluster.split('_'))

def get_llngroep_inst_for_vestingsplaatsen(vps):
    result = {}
    for vp in vps.split('_'):
        try:
            llngroep = df_vp_index.loc[int(vp), 'ul_llngroepen']
            if pd.notna(llngroep):
                llngroep = ast.literal_eval(llngroep)
            result[vp] = (llngroep)
        except:
            result[vp] = np.nan

    return result

def get_totaal_llngroepen(llngroepen):
    result = []
    for key, value in llngroepen.items():
        if pd.notna(value):
            result.append(value.keys())
    result = [llngr for groepen in result for llngr in groepen]
    return len(result)

def get_unieke_llngroepen(llngroepen):
    result = set()
    for key, value in llngroepen.items():
        if pd.notna(value):
            result.update(value.keys())
    return len(result)

def get_llngroepen_tobe(llngroepen_asis):
    result = {}
    for vp, llng in llngroepen_asis.items():
        if pd.notna(llng):
            for key, value in llng.items():
                if key not in result:
                    result[key] = {'inschrijvingen': 0}
                result[key]['inschrijvingen'] += value['inschrijvingen']

    for key, value in result.items():
        result[key]['uren-leraar'] = dul.get_degressieve_uren_leraar(key, value['inschrijvingen'])
    return result

def get_aantal_leerlingen(llngroepen):
    result = 0
    for key, value in llngroepen.items():
        result += value['inschrijvingen']
    return result

def get_vaste_ul(vps):
    result = 0
    for vp in vps.split('_'):
        try:
            vul = df_vp_index.loc[int(vp), 'vaste_ul']
            result += vul
        except:
            result += 0
    return result

def ul_asis(llngroepen):
    result = 0
    for vp, llng in llngroepen.items():
        if pd.notna(llng):
            for key, val in llng.items():
                result += val['uren-leraar']
    return result

def ul_tobe(llngroepen):
    result = 0
    for key, value in llngroepen.items():
        result += value['uren-leraar']
    return result

def get_directeurs(vps):
    result = 0
    for vp in vps.split('_'):
        try:
            directeur = df_vp_index.loc[int(vp), 'directeur_vp']
            if pd.notna(directeur):
                result += directeur
        except:
            result += 0
    return result

df_clusters['schoolnummers'] = df_clusters['cluster'].apply(get_schoolnummers)

# Zoek net op voor alle clusters
df_clusters['net'] = df_clusters['cluster'].apply(get_net)

# Tel aantal vestigingsplaatsen en schoolnummers
df_clusters['aantal_vp'] = df_clusters.apply(lambda row: len(row['cluster'].split('_')), axis=1)
df_clusters['aantal_sn'] = df_clusters.apply(lambda row: len(row['schoolnummers'].split('_')), axis=1)

# Zoek alle leerlingengroepen op (as-is)
df_clusters['leerlingengroepen'] = df_clusters['cluster'].apply(get_llngroep_inst_for_vestingsplaatsen)

# Bereken het verschil in aantal leerlingengroepen (as-is) tegenover unieke leerlingengroepen (to-be)
df_clusters['totaal_llngroepen'] = df_clusters['leerlingengroepen'].apply(get_totaal_llngroepen)
df_clusters['unieke_llngroepen'] = df_clusters['leerlingengroepen'].apply(get_unieke_llngroepen)
df_clusters['llngroepen_diff'] = df_clusters['totaal_llngroepen'] - df_clusters['unieke_llngroepen']

# Voeg leerlingengroepen samen (to-be)
df_clusters['leerlingengroepen_cluster'] = df_clusters['leerlingengroepen'].apply(get_llngroepen_tobe)

# Bereken aantal leerlingen in cluster
df_clusters['aantal_leerlingen'] = df_clusters['leerlingengroepen_cluster'].apply(get_aantal_leerlingen)

# Bereken uren-leraar as-is/to-be en verschil
df_clusters['ul_vast'] = df_clusters['cluster'].apply(get_vaste_ul)
df_clusters['ul_asis'] = df_clusters['leerlingengroepen'].apply(ul_asis)
df_clusters['ul_cluster'] = df_clusters['leerlingengroepen_cluster'].apply(ul_tobe)
df_clusters['ul_diff'] = df_clusters['ul_cluster'] - df_clusters['ul_asis']

df_clusters['ul_per_lln_asis'] = (df_clusters['ul_asis'] + df_clusters['ul_vast'])/df_clusters['aantal_leerlingen']
df_clusters['ul_per_lln_cluster'] = (df_clusters['ul_cluster'] + df_clusters['ul_vast'])/df_clusters['aantal_leerlingen']

# Bereken directeurs as-is/to-be en verschil
df_clusters['directeurs_asis'] = df_clusters['cluster'].apply(get_directeurs)
df_clusters['directeur_cluster'] = df_clusters.apply(lambda row: 1 if row['aantal_leerlingen'] > 0 else 0, axis=1)
df_clusters['directeur_diff'] = df_clusters['directeur_cluster'] - df_clusters['directeurs_asis']

df_clusters['lln_per_dir_asis'] = df_clusters['aantal_leerlingen']/df_clusters['directeurs_asis']
df_clusters['lln_per_dir_cluster'] = df_clusters['aantal_leerlingen']/df_clusters['directeur_cluster']

df_clusters.to_excel(f'jaren/{sys.argv[1]}/14_analyse_clusters_straal_100m.xlsx', index=False)