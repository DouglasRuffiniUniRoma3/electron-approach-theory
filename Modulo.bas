Attribute VB_Name = "Modulo"
Option Compare Database

Public Sub ContatorePrimi()
On Error GoTo Err_ContatorePrimi
Dim dbs As DAO.Database
Set dbs = CurrentDb
Dim Record_set1 As DAO.Recordset
Dim Record_set3 As DAO.Recordset
Dim Record_set2 As DAO.Recordset
Dim Primo As Long
Dim UP As Long
Dim NP_2 As Long
Dim Controllo As Double
UP = 0
Primo = 0
Set Record_set1 = dbs.OpenRecordset("SELECT primo FROM Primi ORDER BY primo;", dbOpenDynaset, dbSeeChanges, dbOptimistic)
If Record_set1.RecordCount = 0 Then
 Record_set1.Close
Else
 Record_set1.MoveLast
 UP = Record_set1!Primo
 Record_set1.MoveFirst
 Set Record_set2 = dbs.OpenRecordset("SELECT primo FROM Primi ORDER BY primo;", dbOpenDynaset, dbSeeChanges, dbOptimistic)
 '**************************************
 Record_set2.MoveFirst
 NP_2 = Record_set2!Primo
 Do Until Record_set2.EOF
  Do Until Record_set1.EOF
   Primo = UP + (NP_2 + Record_set1!Primo)
   Set Record_set3 = dbs.OpenRecordset("SELECT primo FROM Primi WHERE primo <> 1 ORDER BY primo;", dbOpenDynaset, dbSeeChanges, dbOptimistic)
   If Record_set3.RecordCount = 0 Then
    Record_set3.Close
   Else
    Record_set3.MoveFirst
    Do Until Record_set3.EOF
     Controllo = (Primo Mod Record_set3!Primo)
     If Controllo = 0 Then
      'Non è primo,
      'ritorno al secondo anello nidificato (salto), perché si tratta
      'di un reductio ad absurdum, dato che ancora non ho
      'scritto tale presunto numero primo nella tabella Primi
      GoTo SaltaPrimo
     End If
     Record_set3.MoveNext
    Loop
    Record_set3.Close
    'Avendo esaurito i primi ascritti nella tabella primi è rimasto 'solo se stesso.
    'Controllo se esistono numeri primi minori, tra il nuovo primo
    'trovato e l'ultimo primo ascritto.
     If Controlla_Primo_Minore(Primo, UP) = False Then
      'Scrivo nella tabella Primi il numero primo trovato
      dbs.Execute "INSERT INTO Primi (Primo) Values ('" & Primo & "') ;", dbSeeChanges
      dbs.Execute "INSERT INTO UltimiPrimi (Primo_Trovato, UltimoPrimo, NP_1, NP_2) " _
      & "Values ('" & Primo & "', '" & UP & "', '" & NP_2 & "','" & Record_set1!Primo & "') ;", dbSeeChanges
     End If
     '------------------------------------
     GoTo esci
   End If
SaltaPrimo:
   Record_set1.MoveNext
  Loop
  'Si può notare come, a ogni ciclo completo dell'anello interno,
  'l'anello esterno avanzi di un primo.
  Record_set1.MoveFirst
  Record_set2.MoveNext
  NP_2 = Record_set2!Primo
 Loop
 Record_set2.Close
 Record_set1.Close
End If
esci:
dbs.Close

Exit_ContatorePrimi:
    Exit Sub
Err_ContatorePrimi:
    MsgBox Err.Description
    Resume Exit_ContatorePrimi
End Sub

Public Function Controlla_Primo_Minore(ByVal Primo As Long, ByVal UP As Long) As Boolean
On Error GoTo Err_Controlla_Primo_Minore
Dim dbs As DAO.Database
Set dbs = CurrentDb
Dim Record_set_4 As DAO.Recordset
Dim Controllo As Double
Dim I As Long
Dim K As Long

I = 0
K = 0
Controlla_Primo_Minore = False
'Ammetto che la condizione in entrata sia Falsa: non esistono
'primi tra l'ultimo primo trovato e quello presente
K = UP + 2
'Genero il primo numero dispari maggiore
'del primo precedentemente trovato
If K = Primo Then
 GoTo esci_Controlla_Primo_Minore
End If
For I = K To Primo Step 2
'Ovviamente l'accertamento del numero dispari come numero primo,
'prevederà una nuova sequenza di controllo, con gli stessi
'parametri di quella presente nella primitiva chiamante.
 Set Record_set_4 = dbs.OpenRecordset("SELECT primo FROM Primi WHERE primo <> 1 ORDER BY primo;", dbOpenDynaset, dbSeeChanges, dbOptimistic)
 If Record_set_4.RecordCount = 0 Then
  Record_set_4.Close
 Else
  Record_set_4.MoveFirst
  Do Until Record_set_4.EOF
   Controllo = (I Mod Record_set_4!Primo)
   If Controllo = 0 Then
    'No primo
     GoTo SaltaControllo
   End If
   Record_set_4.MoveNext
  Loop
  If I = Primo Then
   GoTo esci_Controlla_Primo_Minore
  End If
  'Ovviamente se il divisore primo non è ascritto devo verificare
  If Verifica_Dispari(I, UP) = False Then
   Controlla_Primo_Minore = True
   GoTo esci_Controlla_Primo_Minore
  End If
SaltaControllo:
  Record_set_4.Close
 End If
Next
esci_Controlla_Primo_Minore:
dbs.Close

Exit_Controlla_Primo_Minore:

    Exit Function
Err_Controlla_Primo_Minore:
    MsgBox Err.Description
    Resume Exit_Controlla_Primo_Minore

End Function

Public Function Verifica_Dispari(ByVal Primo As Long, ByVal UP As Long) As Boolean
On Error GoTo Err_Verifica_Dispari
Dim dbs As DAO.Database
Set dbs = CurrentDb
Dim Record_set_5 As DAO.Recordset
Dim Record_set_6 As DAO.Recordset
Dim N_pari As Long
Dim NP As Long
Dim ND As Long

N_pari = 0
NP = 0
ND = 0

Verifica_Dispari = True
Set Record_set_5 = dbs.OpenRecordset("SELECT primo FROM Primi ORDER BY primo;", dbOpenDynaset, dbSeeChanges, dbOptimistic)
If Record_set_5.RecordCount = 0 Then
 Record_set_5.Close
Else
 N_pari = (Primo - UP)
 Record_set_5.MoveFirst
 Set Record_set_6 = dbs.OpenRecordset("SELECT primo FROM Primi  ORDER BY primo;", dbOpenDynaset, dbSeeChanges, dbOptimistic)
 Record_set_6.MoveFirst
 NP = Record_set_6!Primo
 Do Until Record_set_6.EOF
  Do Until Record_set_5.EOF
   ND = N_pari - (NP + Record_set_5!Primo)
   If ND = 0 Then
    Verifica_Dispari = False
    dbs.Execute "INSERT INTO Primi (Primo) Values ('" & Primo & "') ;", dbSeeChanges
    dbs.Execute "INSERT INTO UltimiPrimi (Primo_Trovato, UltimoPrimo, NP_1, NP_2) " _
    & " Values ('" & Primo & "', '" & UP & "', '" & NP & "','" & Record_set_5!Primo & "');", dbSeeChanges
    GoTo esci_Verifica_Dispari
   End If
  Record_set_5.MoveNext
  Loop
  Record_set_5.MoveFirst
  Record_set_6.MoveNext
  NP = Record_set_6!Primo
 Loop
 Record_set_6.Close
 Record_set_5.Close
End If
esci_Verifica_Dispari:
dbs.Close

Exit_Verifica_Dispari:

    Exit Function
Err_Verifica_Dispari:
    MsgBox Err.Description
    Resume Exit_Verifica_Dispari
    
End Function

