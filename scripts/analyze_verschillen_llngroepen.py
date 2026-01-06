import pandas as pd
import ast
import degressieve_ul_llngroepen as dul

def get_niet_gefinancieerd(llngr, aantal):
    try:
        cutoff = dul.degressieve_ul[llngr]['lln'][-1]
    except:
        cutoff = aantal
    return max(aantal - cutoff, 0)

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
                             'niet_gefinancieerd_asis': 0, 'niet_gefinancieerd_tobe': 0,
                             'ul_asis': 0, 'ul_tobe': 0}
        result[llngr]['aantal_lln'] += gr_info['inschrijvingen']
        result[llngr]['niet_gefinancieerd_asis'] += get_niet_gefinancieerd(llngr, gr_info['inschrijvingen'])
        result[llngr]['ul_asis'] += gr_info['uren-leraar']

for groep in tobe:
    groep = ast.literal_eval(groep)
    for llngr, gr_info in groep.items():
        result[llngr]['niet_gefinancieerd_tobe'] += get_niet_gefinancieerd(llngr, gr_info['inschrijvingen'])
        result[llngr]['ul_tobe'] += gr_info['ul']

df = pd.DataFrame.from_dict(result, orient='index')
df.to_excel('test.xlsx', index=False)