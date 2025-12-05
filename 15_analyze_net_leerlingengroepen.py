import pandas as pd
import ast
import re
import sys

def voeg_asis_llngr_samen(asis, vast):
    result = {}
    asis = re.sub(r'\bnan\b', 'None', asis)
    asis = ast.literal_eval(asis)
    vast = re.sub(r'\bnan\b', 'None', vast)
    vast = ast.literal_eval(vast)

    for key, value in asis.items():
        if value != None:
            for llngr, info in value.items():
                if llngr not in result:
                    result[llngr] = info
                else:
                    result[llngr]['inschrijvingen'] += info['inschrijvingen']
                    result[llngr]['uren-leraar'] += info['uren-leraar']

    for key, value in vast.items():
        if value != None:
            for llngr, ul in value.items():
                result[llngr]['uren-leraar'] += ul

    return result

def voeg_tobe_llngr_samen(tobe, vast):
    result = {}
    tobe = re.sub(r'\bnan\b', 'None', tobe)
    tobe = ast.literal_eval(tobe)
    vast = re.sub(r'\bnan\b', 'None', vast)
    vast = ast.literal_eval(vast)

    for llngr, info in tobe.items():
        if llngr not in result:
            result[llngr] = info
        else:
            result[llngr]['inschrijvingen'] += info['inschrijvingen']
            result[llngr]['uren-leraar'] += info['uren-leraar']

    for key, value in vast.items():
        if value != None:
            for llngr, ul in value.items():
                result[llngr]['uren-leraar'] += ul
    
    return result

df = pd.read_excel(f'jaren/{sys.argv[1]}/8a_analyse_units.xlsx')

df = df[['unit_code_so', 'unit_code_SO_actief', 'net', 'llng_asis', 'llng_tobe', 'llngroep_ul_vast']]

df['leerlingengroepen_asis'] = df.apply(lambda row: voeg_asis_llngr_samen(row['llng_asis'], row['llngroep_ul_vast']), axis=1)
df['leerlingengroepen_tobe'] = df.apply(lambda row: voeg_tobe_llngr_samen(row['llng_tobe'], row['llngroep_ul_vast']), axis=1)

df.to_excel(f'jaren/{sys.argv[1]}/15b_unit_net_llngroepen.xlsx', index=False)


rows = []
for idx, row in df.iterrows():
    dict_col1 = row['leerlingengroepen_asis']
    dict_col2 = row['leerlingengroepen_tobe']
    
    if isinstance(dict_col1, dict) and isinstance(dict_col2, dict):
        all_keys = set(dict_col1.keys()) | set(dict_col2.keys())
        
        for key in all_keys:
            new_row = {
                'unit_code_so': row['unit_code_so'],
                'unit_code_SO_actief': row['unit_code_SO_actief'],
                'net': row['net'],
                'leerlingengroep': key,
                'inschrijvingen': dict_col1.get(key, {}).get('inschrijvingen'),
                'uren_leraar_asis': dict_col1.get(key, {}).get('uren-leraar'),
                'uren_leraar_tobe': dict_col2.get(key, {}).get('uren-leraar'),
            }
            rows.append(new_row)

df_exploded = pd.DataFrame(rows)

df_exploded.to_excel(f'jaren/{sys.argv[1]}/15a_analyse_net_llngroepen.xlsx', index=False)