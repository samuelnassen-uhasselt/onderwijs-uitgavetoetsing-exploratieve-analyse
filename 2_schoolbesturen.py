import pandas as pd

df = pd.read_excel('Brondata\\Omkadering\\omkadering_generiek_2024-2025.xlsx')

# Zoek alle paren van schoolbestuur naam en nummer
df = df[['nummer_im', 'naam_im']].drop_duplicates()

df.to_excel('2a_besturen.xlsx', index=False)

# Zijn er namen die meerdere nummers hebben?
df = df.groupby('naam_im').count().reset_index()
df.to_excel('2b_test_besturen.xlsx', index=False)