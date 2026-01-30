import pandas as pd
import ast
import degressieve_ul_llngroepen as dul

def get_schijven_aantallen(llngr, aantal):
    try:
        schijven = dul.degressieve_ul[llngr]['lln']
        return [min(aantal, schijven[0]), 
                max(min(aantal, schijven[1]) - schijven[0], 0),
                max(min(aantal, schijven[2]) - schijven[1], 0),
                max(aantal - schijven[2], 0)]
    except:
        return [0,0,0,0]

df_units = pd.read_excel('output\\jaren\\2024-2025\\8_analyse_units.xlsx')
df_inst = pd.read_excel('output\\jaren\\2024-2025\\4_schoolnummers_llngroepen_ul_inschrijvingen.xlsx')

asis = df_inst['leerlingengroepen']
tobe = df_units['llng_tobe']

result = {}

for groep in asis:
    groep = ast.literal_eval(groep)
    for llngr, gr_info in groep.items():
        if llngr not in result:
            result[llngr] = {'leerlingengroep': llngr, 'aantal_lln': 0,
                             'lln_schijven_asis': [0,0,0,0], 'lln_schijven_tobe': [0,0,0,0],
                             'ul_asis': 0, 'ul_tobe': 0}
        result[llngr]['aantal_lln'] += gr_info['inschrijvingen']
        lln_schijven = get_schijven_aantallen(llngr, gr_info['inschrijvingen'])
        result[llngr]['lln_schijven_asis'] = [x + y for x, y in zip(result[llngr]['lln_schijven_asis'], lln_schijven)]
        result[llngr]['ul_asis'] += gr_info['uren-leraar']

for groep in tobe:
    groep = ast.literal_eval(groep)
    for llngr, gr_info in groep.items():
        lln_schijven = get_schijven_aantallen(llngr, gr_info['inschrijvingen'])
        result[llngr]['lln_schijven_tobe'] = [x + y for x, y in zip(result[llngr]['lln_schijven_tobe'], lln_schijven)]
        result[llngr]['ul_tobe'] += gr_info['ul']

df = pd.DataFrame.from_dict(result, orient='index')
df['ul_verlies'] = df['ul_asis'] - df['ul_tobe']

max_verl = df['ul_verlies'].max()

df['verlies_tov_max'] = df.apply(lambda row: max(0, row['ul_verlies']/max_verl), axis=1)
som_verlies_tov_max = df['verlies_tov_max'].sum()
df['herverdeling_percent'] = df['verlies_tov_max']/som_verlies_tov_max

df = df[['leerlingengroep', 'aantal_lln', 'lln_schijven_asis', 'lln_schijven_tobe', 'ul_asis', 'ul_tobe', 
         'ul_verlies', 'herverdeling_percent']]

df.to_excel('output\\ul_herwerking.xlsx', index=False)