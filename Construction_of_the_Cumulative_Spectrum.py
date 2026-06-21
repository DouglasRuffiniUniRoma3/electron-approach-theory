import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calcola_spettro_cumulativo(file_path="testFile.txt"):
    try:
        df = pd.read_csv(file_path, sep='\s+', header=None)
        b = df.iloc[:, 2].values
        c = df.iloc[:, 3].values
        delta_p = b + c

        delta_p_ordinato = np.sort(delta_p)

        cumulativa = np.arange(1, len(delta_p_ordinato) + 1)

        return delta_p_ordinato, cumulativa

    except FileNotFoundError:
        return "Error: File Not Found."

delta_p_ordinato, cumulativa = calcola_spettro_cumulativo()

if isinstance(delta_p_ordinato, np.ndarray):
    plt.figure(figsize=(10, 6))
    plt.plot(delta_p_ordinato, cumulativa)
    plt.title('Spettro Cumulativo di Δp = b + c')
    plt.xlabel('Valore di Δp')
    plt.ylabel('Numero Cumulativo di Occorrenze')
    plt.grid(True)
    plt.show()
else:
    print(delta_p_ordinato)
