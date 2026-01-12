import pandas as pd
import numpy as np
import dea_implementaties as dea
import dea_plots as dp
import subprocess

df_units = pd.read_excel('output/18_dea_master.xlsx', sheet_name='Units')
df_units = df_units[df_units['leerlingen_laatste_jaar_aso'] > 0]
df_units = df_units[df_units['opgenomen_studiepunten'] > 0]
df_units_2022 = df_units[df_units['jaar_afgestudeerd_so'] == '2022-2023'].copy()
df_units_2022 = df_units_2022[df_units_2022['finaliteit'] == 'Volledig aso']

df_units_2022['kost_laatste_jaar_aso'] = (
    df_units_2022['directeurs_laatste_jaar_aso']*112776 +
    (df_units_2022['vaste_uren-leraar_laatste_jaar_aso'] + 
     df_units_2022['deg_uren-leraar_laatste_jaar_aso_asis']) * 0.9657 * 69073 / 21.23
)

df_units_2022['kost_per_leerling_laatste_aso'] = df_units_2022[
    'kost_laatste_jaar_aso']/df_units_2022['leerlingen_laatste_jaar_aso']
df_units_2022['doorstroom_percentage'] = df_units_2022['rechtstreeks_HO']/df_units_2022['loopbanen_HO']

input = {
    'kolom': 'kost_per_leerling_laatste_aso',
    'label' : 'Kost in euro per leerling - ASO'
}

output = {
    'kolom': 'studierendement',
    'label' : 'Studierendement - ASO'
}

X = df_units_2022[[input['kolom']]].values
Y = df_units_2022[[output['kolom']]].values

df_units_2022['efficiency_score_crs_studierendement'] = dea.dea_input_oriented_crs(X,Y)

fig = dp.plot_in_out_analysis_interactive(X, Y, df_units_2022['efficiency_score_crs_studierendement'].values, 
                              input_label=input['label'],
                              output_label=output['label'],
                              school_ids=df_units_2022['unit_code_so'].values)

fig.show()


input = {
    'kolom': 'kost_per_leerling_laatste_aso',
    'label' : 'Kost in euro per leerling - ASO'
}

output = {
    'kolom': 'doorstroom_percentage',
    'label' : 'Percenatge Doorstroom HO - ASO'
}

X = df_units_2022[[input['kolom']]].values
Y = df_units_2022[[output['kolom']]].values

df_units_2022['efficiency_score_crs_doostroom_percent'] = dea.dea_input_oriented_crs(X,Y)

fig = dp.plot_in_out_analysis_interactive(X, Y, df_units_2022['efficiency_score_crs_doostroom_percent'].values, 
                              input_label=input['label'],
                              output_label=output['label'],
                              school_ids=df_units_2022['unit_code_so'].values)

fig.show()


# stoned_x = df_units_2022[input['kolom']]
# stoned_y = df_units_2022[output['kolom']]

# stoned_eff = dea.stoned(stoned_x, stoned_y)
# print(stoned_eff)
# df_units_2022['efficiency_score_stoned_studierendement'] = stoned_eff


df_units_2022.to_excel('output/19_dea.xlsx', index=False)


r_path = "C:\\Program Files\\R\\R-4.5.2\\bin\\Rscript.exe"
script = "C:\\Users\\lucp14223\\Files\\programmeren\\onderwijs\\analyse\\scripts\\mergoni_dea.r"

dea_file = "output\\19_dea.xlsx"
input_col = 'kost_per_leerling_laatste_aso'
output_col = 'studierendement'
conditioneel_col = 'gemiddelde_oki'
col_name = 'mergoni_dea'

res = subprocess.call([r_path, script, dea_file, input_col, output_col, conditioneel_col, col_name])