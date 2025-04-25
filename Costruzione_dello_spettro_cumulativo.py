import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

def calcola_spettro_cumulativo(file_path="D://Documenti//----Numeri//Codice Python//testFile.txt"):
    try:
        df = pd.read_csv(file_path, sep='\s+', header=None)
        b = df.iloc[:, 2].values
        c = df.iloc[:, 3].values
        delta_p = b + c

        # Ordina i valori di delta_p
        delta_p_ordinato = np.sort(delta_p)

        # Crea l'asse y per la cumulativa (da 1 a N)
        cumulativa = np.arange(1, len(delta_p_ordinato) + 1)

        return delta_p_ordinato, cumulativa

    except FileNotFoundError:
        return "Errore: File non trovato."

# Calcola lo spettro cumulativo
delta_p_ordinato, cumulativa = calcola_spettro_cumulativo()

# Visualizza lo spettro cumulativo
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

