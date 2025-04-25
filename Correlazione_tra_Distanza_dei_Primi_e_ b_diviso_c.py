#From promp: pip install fsspec
import pandas as pd
import numpy as np

def preparaArray(file_content):
    """
    Pre-elabora i dati per gestire la virgola come separatore decimale.

    Args:
        file_content (str): Il contenuto del file di dati.

    Returns:
        list: Una lista di liste, dove ogni sottolista rappresenta una riga
              con i valori convertiti in float.
    """
    array = []
    s = file_content.split("\n")

    for riga in s:
        if riga != '':
            vector = riga.split(" ")
            # Assicurati che ci siano abbastanza elementi prima di accedere agli indici
            if len(vector) >= 4:
                p = vector[1].replace(',', '.')
                b = vector[2].replace(',', '.')
                c = vector[3].replace(',', '.')
                array.append([float(p), float(b), float(c)])
            else:
                print(f"Riga ignorata (meno di 4 elementi): {riga}")  # Messaggio di debug
    return array

def calcola_distanza(p_values):
    """Calcola la distanza tra numeri consecutivi in una lista."""
    return [p_values[i+1] - p_values[i] for i in range(len(p_values) - 1)]

def calcola_correlazione(distanze, b_values, c_values):
    """Calcola la correlazione tra le distanze e le sequenze b e c."""
    if len(distanze) < 1 or len(b_values) < 1 or len(c_values) < 1 or \
       np.var(distanze) == 0 or np.var(b_values) == 0 or np.var(c_values) == 0:
        return None  # Indica che non si può calcolare la correlazione
    return np.corrcoef([distanze, b_values, c_values], rowvar=False)  # rowvar=False!

def elabora_dati(file_path="D://Documenti//----Numeri//Codice Python//testFile.txt"):
    """Elabora i dati del file, calcolando distanze e correlazioni."""

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        data_array = preparaArray(file_content)

        # Ora creiamo un DataFrame pandas da data_array
        df = pd.DataFrame(data_array)

        p_values = df.iloc[:, 0].tolist()  # Colonna 0 (b) come p (??)
        b_values = df.iloc[:, 1].tolist()  # Colonna 1 (c) come b (??)
        c_values = df.iloc[:, 2].tolist()  # Colonna 2 (d) come c (??)

        tutte_le_correlazioni = []

        # Calcola le distanze
        distanze = calcola_distanza(p_values)

        # Calcola e memorizza la correlazione se abbiamo abbastanza dati
        if len(distanze) > 0:
            correlazione = calcola_correlazione(distanze, b_values[:-1], c_values[:-1])
            if correlazione is not None:
                tutte_le_correlazioni.append(correlazione)

        return tutte_le_correlazioni

    except FileNotFoundError:
        return "Errore: File non trovato."
    except Exception as e:
        return f"Errore durante l'elaborazione: {e}"

# Esempio di utilizzo
risultati_correlazione = elabora_dati()

if isinstance(risultati_correlazione, list):
    print("\nCorrelazioni calcolate:")
    for correlazione in risultati_correlazione:
        print(correlazione)
else:
    print(risultati_correlazione)
