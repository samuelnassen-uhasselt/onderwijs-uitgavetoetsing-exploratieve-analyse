import ast
import pandas as pd
import degressieve_ul_llngroepen as dul

# Leerlingengroepen
def merge_llngroep_dictionaries(string_dicts):

    # Som van inschrijvingen per leerlingengroep
    inschr = {}
    for s in string_dicts:
        if pd.notna(s):
            d = ast.literal_eval(s)
            if isinstance(d, dict):
                for key, value in d.items():
                    inschr[key] = inschr.get(key, 0) + value
    
    # Uren-leraar op basis van inschrijvingen per leerlingengroep
    result = {}
    for key, value in inschr.items():
        ul = dul.get_degressieve_uren_leraar(key, value)
        result[key] = {
            'inschrijvingen': value,
            'uren-leraar': ul
        }

    return result

def merge_llngroup_vul(string_dicts):
    result = {}
    for s in string_dicts:
        if pd.notna(s):
            d = ast.literal_eval(s)
            if isinstance(d, dict):
                for key, value in d.items():
                    result[key] = result.get(key, 0) + value

    return result

def get_directeur_vol_half(llngr, aantal):
    for g in llngr.keys():
        if not '1e graad' in g and not '2e graad' in g and not 'okan' in g:
            if aantal >= 83:
                return 1
            return 0.5
    if aantal >= 120:
        return 1
    return 0.5

df_vestigingen = pd.read_excel("output/3_vestigingsplaatsen_master.xlsx")

# Groepeer per schoolnummer en bereken leerlingengroepen
df_schoolnummers = df_vestigingen.groupby('schoolnummer', dropna=False).agg({
    'leerlingengroepen': merge_llngroep_dictionaries,
    'leerlingengroepen_vaste_ul': merge_llngroup_vul,
    'vaste_ul': 'sum',
    'aantal_inschrijvingen': 'sum'
}).reset_index()
df_schoolnummers['directeurs'] = df_schoolnummers.apply(lambda row: get_directeur_vol_half(row['leerlingengroepen'], row['aantal_inschrijvingen']), axis=1)

df_schoolnummers.to_excel('output/4_schoolnummers_llngroepen_ul_inschrijvingen.xlsx', index=False)