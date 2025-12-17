import pandas as pd
import dea_implementaties as dea
import dea_plots as dp

df_units = pd.read_excel('output/18_units_dea_master.xlsx')
df_units = df_units[df_units['leerlingen_laatste_jaar_aso'] > 0]
df_units = df_units[df_units['opgenomen_studiepunten'] > 0]
df_units_2022 = df_units[df_units['jaar_afgestudeerd_so'] == '2022-2023'].copy()

df_units_2022['kost_laatste_jaar_aso'] = (
    df_units_2022['directeurs_laatste_jaar_aso']*112776 +
    df_units_2022['uren-leraar_laatste_jaar_aso'] * 0.9657 * 69073 / 21.23
)

df_units_2022['kost_per_leerling_laatste_aso'] = df_units_2022[
    'kost_laatste_jaar_aso']/df_units_2022['leerlingen_laatste_jaar_aso']
df_units_2022['doorstroom_percentage'] = 1 -(df_units_2022['niet_HO']/df_units_2022['loopbanen_HO'])

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


df_units_2022.to_excel('output/19_dea.xlsx', index=False)
