# From prompt: pip install fsspec
import pandas as pd
import numpy as np
from collections import Counter  # Importa la classe Counter

def analisi_ricorsione_frequenze(file_path="testFile.txt"):
    try:
        df = pd.read_csv(file_path, sep='\s+', header=None)
        b_values = df.iloc[:, 2].tolist()
        c_values = df.iloc[:, 3].tolist()

        conteggio_b = Counter(b_values)
        conteggio_c = Counter(c_values)
        return conteggio_b, conteggio_c
    except FileNotFoundError:
        return "Error: File Not Found"

conteggio_b, conteggio_c = analisi_ricorsione_frequenze()

print("Frequency of values in b:")
for valore, frequenza in conteggio_b.items():
    print(f"Value: {valore}, Frequency: {frequenza}")

print("\n Frequency of values in c:")
for valore, frequenza in conteggio_c.items():
    print(f"Value: {valore}, Frequency: {frequenza}")
