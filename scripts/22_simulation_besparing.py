from openpyxl import load_workbook
import pandas as pd
import degressieve_ul_llngroepen as dul
import ast
import re

wb = load_workbook('Brondata\\simulatie_input.xlsx', data_only=True)
ws = wb['input']


def get_llngroepen_alt(llngroepen, herwerkt, d):
    llngroepen = ast.literal_eval(re.sub(r'\bnan\b', 'None', llngroepen))
    result = {}
    for vp, llng in llngroepen.items():
        if pd.notna(llng):
            for key, value in llng.items():
                if key not in result:
                    result[key] = {'inschrijvingen': 0}
                result[key]['inschrijvingen'] += value['inschrijvingen']

    for key, value in result.items():
        result[key]['ul'] = dul.get_degressieve_uren_leraar(key, value['inschrijvingen'], herwerkt, d)
    return result

def ul_alt(llngroepen):
    result = 0
    for key, value in llngroepen.items():
        result += value['ul']
    return result

df_ul_nul = pd.read_excel('output\\oefening_ul_herwerking.xlsx')

ul_besparing_nul = ws['B4'].value
ul_besparing_alt = ws['B7'].value

ul_besp_perc = 1-(ul_besparing_alt/ul_besparing_nul)

df_ul_nul['coef_alt'] = df_ul_nul['verlies_per_niet_gefinancieerde_lln_tobe'] * ul_besp_perc
df_ul_alt = df_ul_nul[['leerlingengroep', 'coef_alt']]
d = {'DEEL' : dict(zip(df_ul_alt['leerlingengroep'], df_ul_alt['coef_alt']))}

df_units = pd.read_excel('output\\jaren\\2024-2025\\8_analyse_units.xlsx')
df_units['llngr_ul_alt'] = df_units.apply(lambda row: get_llngroepen_alt(row['llng_asis'], 'DEEL', d), axis=1)
df_units['ul_alt'] = df_units['llngr_ul_alt'].apply(ul_alt)

df_units.to_excel('test.xlsx', index=False)

agg_cols = ['ul_asis', 'ul_alt']