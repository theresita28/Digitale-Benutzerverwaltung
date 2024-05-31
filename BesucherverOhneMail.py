import sqlite3
import datetime

verbindung = sqlite3.connect("besucherverwaltung.db")
zeiger = verbindung.cursor()





def CreateTables():
    global anzahlBesucher
    anzahlBesucher = 0
    sql_anweisung = """
    CREATE TABLE IF NOT EXISTS besucher (
    besuchernr INT PRIMARY KEY,
    vorname VARCHAR(20), 
    nachname VARCHAR(30),
    Rolle VARCHAR(20)
    );"""

    zeiger.execute(sql_anweisung)


    sql_anweisung = """
    CREATE TABLE IF NOT EXISTS besucherliste (
    besucher INT, 
    eincheckzeit VARCHAR(50),
    auscheckzeit VARCHAR(50),
    ansprechpartner VARCHAR(50),
    Aufenthaltsort VARCHAR(50),
    FOREIGN KEY (besucher)
     REFERENCES besucher (besuchernr) 
    );"""
    #  FOREIGN KEY (besucher)
    #    REFERENCES besucher (besuchernr) 
    zeiger.execute(sql_anweisung)
    verbindung.commit()

def proofUniqueNumber(proofedNumber,counts):
    uniqueNumber = True
    for i in range(counts):
        if proofedNumber == inhalt[i][0]:
            uniqueNumber = 0
        
    return uniqueNumber

def CreateBesuchernr():
    zeiger.execute("SELECT COUNT(*) FROM besucher")
    anzahl = zeiger.fetchone()
    # """ print(inhalt)
    # print(inhalt[0]) """
    besuchernr = anzahl[0] +1 
    # #print(besuchernr)

    #besuchernr = 1

    zeiger.execute("SELECT besuchernr FROM besucher")
    global inhalt
    inhalt = zeiger.fetchall()
    #print(inhalt)
    #print(inhalt[0][0])




    while True:
        if proofUniqueNumber(besuchernr, anzahl[0]) == 1:
             break
        else:
            besuchernr += 1
            
        



    #print(besuchernr)
    #print(uniqueNumber)
    return besuchernr

# Für Test-----------------------
#print(CreateBesuchernr())
# vorname = "Yan"
# nachname= "Fi"
#print(besuchernr)

def BesucherAnlegen(vname,name,rolle):
    besuchernr = int(CreateBesuchernr())
    print("Der Besucher bekommt die Nummer: " + str(besuchernr))
    vorname = vname
    nachname = name
    zeiger.execute("INSERT INTO besucher VALUES (?,?,?,?)", (besuchernr,vorname, nachname,rolle))
    verbindung.commit()

CreateTables()   # muss
#BesucherAnlegen("The","DE", "Bewerber")

#Einchecken/Auschecken von Besuchern-----------------------------------------------

def aktuelleZeit():
    zeit = datetime.strftime("%d.%m.%Y %H:%M:%S", datetime.now())
    #print(zeit)
    #print(type(zeit))
    return zeit

def proofBesuchernr(besuchernr):
    zeiger.execute("SELECT besuchernr FROM besucher WHERE besuchernr= ?", (besuchernr,))
    
    if (zeiger.fetchone() != None):
        proofed = True
    else:
        proofed = False
    
    return proofed

def einchecken(besuchernr, ansprechpartner, aufenthaltsort):
    ezeit= aktuelleZeit()
    besucher = besuchernr
    if(proofBesuchernr(besuchernr)):
        besucher = besuchernr
        zeiger.execute("INSERT INTO besucherliste(besucher,eincheckzeit, ansprechpartner,aufenthaltsort) VALUES (?,?,?,?)", (besucher,ezeit, ansprechpartner, aufenthaltsort ))
        verbindung.commit()
    else:
        print("Besuchernummer gibt es nicht.")

def auschecken(besucher):
    azeit = aktuelleZeit()
    if(proofBesuchernr(besucher)):
        zeiger.execute("UPDATE besucherliste SET auscheckzeit=? WHERE besucher=?", (azeit, besucher))
        verbindung.commit()
    else:
        print("Besuchernummer gibt es nicht.")



besucher = 3
ansprechpartner = "Mister x"
aufenthaltsort = "B240"

#print( type(besucher))        für Test


#einchecken(besucher,ansprechpartner, aufenthaltsort)
#auschecken(besucher)

#Abfrage der aktuellen Besucheranzahl----------------------------------------------------------------
def AbfrageAktBesucheranzahl():
    zeiger.execute("SELECT COUNT(*) FROM besucherliste WHERE auscheckzeit IS NULL")
    anzahl = zeiger.fetchone()
    print(anzahl[0])
    return anzahl[0]

#anzahl = AbfrageAktBesucheranzahl()
#print("Die aktuelle Besucheranzahl ist " + str(anzahl))

#Abfrage Besucheranzahl zu bestimmten Datum-----------------------------------------------------
#zeitpunkt = datetime.datetime(2023, 5, 30)     für Test Datentyp Date
zeitpunkt = "30.05.2024"

def AbfrageBesucheranzahl(zeitpunkt):
    zeiger.execute("SELECT COUNT(*) FROM besucherliste WHERE auscheckzeit LIKE ? OR eincheckzeit LIKE ?",(zeitpunkt + '%',zeitpunkt + '%'))
    anzahl = zeiger.fetchone()
    #print(anzahl[0])

    zeiger.execute("""SELECT b1.besucher, b2.vorname, b2.nachname, b2.Rolle, b1.eincheckzeit, b1.auscheckzeit, b1.ansprechpartner, b1.Aufenthaltsort
                FROM besucherliste b1, besucher b2 
                WHERE (auscheckzeit LIKE ? OR eincheckzeit LIKE ?) and b1.besucher = b2.besuchernr""",(zeitpunkt + '%',zeitpunkt + '%'))
    inhalt = zeiger.fetchall()
    #print(inhalt)
    print("Es wurden " + str(anzahl[0]) + " Besucher zum angegebenen Zeitpunkt gefunden: " + str(inhalt))

#AbfrageBesucheranzahl(zeitpunkt)

#Aktualisieren/Löschen der Besucherdaten---------------------------------------------------
#Aktualisieren von Nachname oder Rolle

def UpdateBesucher(besucher, updatedValue):

    #Update Besuchernachname-----------------
    """ if(proofBesuchernr(besucher)):
        zeiger.execute("UPDATE besucher SET nachname=? WHERE besuchernr=?", (updatedValue, besucher))
        verbindung.commit()
    else:
        print("Besuchernummer gibt es nicht.") """
    #Update Rolle--------------------------------
    if(proofBesuchernr(besucher)):
        zeiger.execute("UPDATE besucher SET Rolle=? WHERE besuchernr=?", (updatedValue, besucher))
        verbindung.commit()
    else:
        print("Besuchernummer gibt es nicht.")

#UpdateBesucher(1,"Handwerker")

#Löschen von Besucher-------------

besucher = 4
def DeleteBesucher(besuchernr):
    zeiger.execute("DELETE FROM besucher WHERE besuchernr=?", (besuchernr,))
    zeiger.execute("DELETE FROM besucherliste WHERE besucher=?", (besuchernr,))
    verbindung.commit()

DeleteBesucher(besucher)




verbindung.close()