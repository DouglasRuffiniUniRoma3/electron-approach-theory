# Riconducibilità a Ritmo Sinusoidale (Trasformata di Fourier)
# From prompt: pip install fsspec
import pandas as pd
import numpy as np
from collections import Counter  # Importa la classe Counter

# Funzione per analizzare la ricorsione e le frequenze in b e c
# From prompt: pip install fsspec
import pandas as pd
import numpy as np
from collections import Counter  # Importa la classe Counter

def analisi_ricorsione_frequenze(file_path="D://Documenti//----Numeri//Codice Python//testFile.txt"):
    try:
        df = pd.read_csv(file_path, sep='\s+', header=None)
        b_values = df.iloc[:, 2].tolist()
        c_values = df.iloc[:, 3].tolist()

        conteggio_b = Counter(b_values)
        conteggio_c = Counter(c_values)
        return conteggio_b, conteggio_c
    except FileNotFoundError:
        return "Errore: File non trovato"

# Esegui l'analisi
conteggio_b, conteggio_c = analisi_ricorsione_frequenze()

# Stampa i risultati
print("Frequenza dei valori in b:")
for valore, frequenza in conteggio_b.items():
    print(f"Valore: {valore}, Frequenza: {frequenza}")

print("\nFrequenza dei valori in c:")
for valore, frequenza in conteggio_c.items():
    print(f"Valore: {valore}, Frequenza: {frequenza}")
