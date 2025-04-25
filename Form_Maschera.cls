VERSION 1.0 CLASS
BEGIN
  MultiUse = -1  'True
END
Attribute VB_Name = "Form_Maschera"
Attribute VB_GlobalNameSpace = False
Attribute VB_Creatable = True
Attribute VB_PredeclaredId = True
Attribute VB_Exposed = False
Option Compare Database

Private Sub Comando1_Click()
On Error GoTo Err_Comando1_Click
Dim dbs As DAO.Database
Set dbs = CurrentDb
Dim Record_set As DAO.Recordset
Dim I As Long
Dim msg, style, Response, title

If Me.Testo1 > 0 Then
Set Record_set = dbs.OpenRecordset("SELECT primo FROM Primi ORDER BY primo;", dbOpenDynaset, dbSeeChanges, dbOptimistic)
 If Record_set.RecordCount = 0 Then
  'Se la tabella è vuota allora inserisco i valori di partenza
  Record_set.Close
  dbs.Execute "Delete * From Primi"
  dbs.Execute "Delete * From UltimiPrimi"
  dbs.Execute "INSERT INTO Primi (Primo) Values (1) ;", dbSeeChanges
  dbs.Execute "INSERT INTO Primi (Primo) Values (3) ;", dbSeeChanges
  dbs.Execute "INSERT INTO UltimiPrimi (Primo_Trovato, UltimoPrimo, NP_1, NP_2) Values (3 , 1, 1, 1) ;", dbSeeChanges
 Else
  'Se la tabella contiene dati muovo all'ultimo
  Record_set.MoveLast
  If Record_set!Primo > 3 Then
   msg = "Vuoi continuare ad aggiungere primi, all'ultimo primo trovato '" & Record_set!Primo & "' ?"
   style = vbYesNo + vbQuestion + vbDefaultButton2
   Response = MsgBox(msg, style, title)
   If Response = vbNo Then
    'Allora cancello tutto e ricomincio
    dbs.Execute "Delete * From Primi"
    dbs.Execute "Delete * From UltimiPrimi"
    dbs.Execute "INSERT INTO Primi (Primo) Values (1) ;", dbSeeChanges
    dbs.Execute "INSERT INTO Primi (Primo) Values (3) ;", dbSeeChanges
    dbs.Execute "INSERT INTO UltimiPrimi (Primo_Trovato, UltimoPrimo, NP_1, NP_2) Values (3 , 1, 1, 1) ;", dbSeeChanges
   End If
  End If
  Record_set.Close
 End If
 'Comunque scrivo da 3 a il numero di numeri voluto
 For I = 3 To Me.Testo1
  'Chiamo la funzione che trova i primi
  ContatorePrimi
 Next
 MsgBox "Operazione terminata!", vbInformation
Else
 MsgBox "Inserire il numero di quanti numeri primi si vuole trovare!"
End If
dbs.Close

Exit_Comando1_Click:
    Exit Sub
Err_Comando1_Click:
    MsgBox Err.Description
    Resume Exit_Comando1_Click

End Sub
