import pandas as pd
import numpy as np
import dea_implementaties as dea
import dea_plots as dp
import matplotlib.pyplot as plt

df_units = pd.read_excel('output/18_units_dea_master.xlsx')
df_units = df_units[df_units['aantal_studietrajecten'] > 10]
df_units = df_units[df_units['leerlingen_laatste_jaar'] > 0]
df_units = df_units[df_units['opgenomen_studiepunten'] > 0]
df_units_2022 = df_units[df_units['jaar_afgestudeerd_so'] == '2022-2023'].copy()
df_units_2022['ul_per_leerling_laatste'] =df_units_2022['uren-leraar_laatste_jaar']/df_units_2022['leerlingen_laatste_jaar']

input = {
    'kolom': 'ul_per_leerling_laatste',
    'label' : 'Uren-leraar per leerling'
}

output = {
    'kolom': 'studierendement',
    'label' : 'Studierendement'
}

X = df_units_2022[[input['kolom']]].values
Y = df_units_2022[[output['kolom']]].values

df_units_2022['efficiency_score_crs'] = dea.dea_input_oriented_crs(X,Y)
df_units_2022['efficiency_score_vrs'] = dea.dea_input_oriented_vrs(X,Y)

fig = dp.plot_in_out_analysis_interactive(X, Y, df_units_2022['efficiency_score_crs'].values, 
                              input_label=input['label'],
                              output_label=output['label'],
                              school_ids=df_units_2022['unit_code_so'].values)

fig.show()

df_units_2022.to_excel('output/19a_dea.xlsx', index=False)
