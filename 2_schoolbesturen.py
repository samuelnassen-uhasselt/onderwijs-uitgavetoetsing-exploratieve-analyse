import pandas as pd
import sys

df = pd.read_excel('Brondata\\Omkadering\\omkadering_generiek_2024-2025.xlsx')

# Zoek alle paren van schoolbestuur naam en nummer
df = df[['nummer_im', 'naam_im']].drop_duplicates()

df.to_excel(f'output/jaren/{sys.argv[1]}/2_besturen.xlsx', index=False)