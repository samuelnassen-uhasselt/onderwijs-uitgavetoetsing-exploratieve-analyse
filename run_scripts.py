import os
import re
import subprocess

folder = './output/jaren'
os.makedirs(folder, exist_ok=True)

pattern = r'(\d{4}-\d{4})'

jaren = []
for filename in os.listdir('./Brondata/Inschrijvingen'):
    match = re.search(pattern, filename)
    if match:
        jaar_inschr = match.group(1)
        os.makedirs(f'./output/jaren/{jaar_inschr}', exist_ok=True)
        jaren.append(jaar_inschr)

# scripts = [
# '0_vestigingsplaatsen_nummer.py', '1_inschrijvingen_vestigingen.py', '2_schoolbesturen.py',
# '3_master_file.py', '4_ul_dir_inschrijvingen_scholen.py', '5_master_ul_dir.py',
# '6_zelfde_adres.py', '7_analyze_zelfde_adres.py', '8_analyze_units_llngroepen.py', '9_analyze_bestuur_net.py', 
# '10_vergelijkingsanalyse.py', '11_analyse_clusters_vergelijkbaar.py', '12_sn_in_meerdere_hoofdstruct.py',
# '13_straal.py', '14_analyze_straal.py', '15_analyze_net_leerlingengroepen.py', '21_analyze_instellingen.py', 
# ]
scripts = [
    '8_analyze_units_llngroepen.py', '21_analyze_instellingen.py'
]

# others = [
# '16_jaren_samen.py', '17_analyze_clusters_llngroepen.py', '18_dea_master.py', '19_dea.py',
# '20_vergelijk_clusters_units.py'
# ]
others = [
    '16_jaren_samen.py', '18_dea_master.py'
]


for jaar in jaren:
    for script in scripts:
        subprocess.run(['python', f'scripts/{script}', jaar])
        print(f'Finished running {script} for {jaar}.')

for script in others:
    subprocess.run(['python', f'scripts/{script}'])
    print(f'Finished running {script}.')