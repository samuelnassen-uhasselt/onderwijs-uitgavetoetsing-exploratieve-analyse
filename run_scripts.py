import os
import subprocess

folder = 'output/jaren'
jaren_folders = [f for f in os.listdir(folder)]
# scripts = [
# '0_vestigingsplaatsen_nummer.py', '1_inschrijvingen_vestigingen.py', '2_schoolbesturen.py',
# '3_master_file.py', '4_ul_dir_inschrijvingen_scholen.py', '5_master_ul_dir.py',
# '6_zelfde_adres.py', '7_analyze_zelfde_adres.py', '8_analyze_units_llngroepen.py', '9_analyze_bestuur_net.py', 
# '10_vergelijkingsanalyse.py', '11_analyse_clusters_vergelijkbaar.py', '12_sn_in_meerdere_hoofdstruct.py',
# '13_straal.py', '14_analyze_straal.py', '15_analyze_net_leerlingengroepen.py'
# ]
scripts = [
    '1_inschrijvingen_vestigingen.py','5_master_ul_dir.py'
]

for jaar in jaren_folders:
    for script in scripts:
        subprocess.run(['python', script, jaar])