import pandas as pd

df = pd.read_csv('data/processed/dataset.csv')
print(f"Total muestras: {len(df)}")
print(f"\nDistribución por clase:")
print(df['label'].value_counts().sort_values())
print(f"\nClases con solo 1 muestra:")
problematic = df['label'].value_counts()[df['label'].value_counts() == 1]
if len(problematic) > 0:
    print(problematic)
else:
    print("Ninguna clase tiene solo 1 muestra")
