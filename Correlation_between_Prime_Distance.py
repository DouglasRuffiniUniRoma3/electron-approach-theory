#From promp: pip install fsspec
import pandas as pd
import numpy as np

def preparaArray(file_content):
    array = []
    s = file_content.split("\n")

    for riga in s:
        if riga != '':
            vector = riga.split(" ")
            if len(vector) >= 4:
                p = vector[1].replace(',', '.')
                b = vector[2].replace(',', '.')
                c = vector[3].replace(',', '.')
                array.append([float(p), float(b), float(c)])
            else:
                print(f"Ignored line (less than 4 items):{riga}")  
    return array

def calcola_distanza(p_values):
    return [p_values[i+1] - p_values[i] for i in range(len(p_values) - 1)]

def calcola_correlazione(distanze, b_values, c_values):
    if len(distanze) < 1 or len(b_values) < 1 or len(c_values) < 1 or \
       np.var(distanze) == 0 or np.var(b_values) == 0 or np.var(c_values) == 0:
        return None  
    return np.corrcoef([distanze, b_values, c_values], rowvar=False)  
# rowvar=False!

def elabora_dati(file_path="testFile.txt"):

    try:
        with open(file_path, 'r') as file:
            file_content = file.read()

        data_array = preparaArray(file_content)

        df = pd.DataFrame(data_array)

        p_values = df.iloc[:, 0].tolist()  # Colonna 0 (b) come p (??)
        b_values = df.iloc[:, 1].tolist()  # Colonna 1 (c) come b (??)
        c_values = df.iloc[:, 2].tolist()  # Colonna 2 (d) come c (??)

        tutte_le_correlazioni = []

        distanze = calcola_distanza(p_values)

        if len(distanze) > 0:
            correlazione = calcola_correlazione(distanze, b_values[:-1], c_values[:-1])
            if correlazione is not None:
                tutte_le_correlazioni.append(correlazione)

        return tutte_le_correlazioni

    except FileNotFoundError:
        return "Error: File Not Found."
    except Exception as e:
        return f"Error while processing: {e}"

risultati_correlazione = elabora_dati()

if isinstance(risultati_correlazione, list):
    print("\nCalculated correlations:")
    for correlazione in risultati_correlazione:
        print(correlazione)
else:
    print(risultati_correlazione)
