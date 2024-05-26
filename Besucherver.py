import sqlite3
verbindung = sqlite3.connect("besucherverwaltung.db")
zeiger = verbindung.cursor()

import time



def CreateTables():
    global anzahlBesucher
    anzahlBesucher = 0
    sql_anweisung = """
    CREATE TABLE IF NOT EXISTS besucher (
    besuchernr INT PRIMARY KEY,
    vorname VARCHAR(20), 
    nachname VARCHAR(30)
    );"""

    zeiger.execute(sql_anweisung)


    sql_anweisung = """
    CREATE TABLE IF NOT EXISTS besucherliste (
    besucher VARCHAR(20), 
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
            
        



    print(besuchernr)
    #print(uniqueNumber)
    return besuchernr

CreateTables()
#print(CreateBesuchernr())

# vorname = "Yan"
# nachname= "Fi"

#print(besuchernr)

def BesucherAnlegen(vname,name):
    besuchernr = int(CreateBesuchernr())
    vorname = vname
    nachname = name
    zeiger.execute("INSERT INTO besucher VALUES (?,?,?)", (besuchernr,vorname, nachname))
    verbindung.commit()

BesucherAnlegen("The", "DE")

#Einchecken/Auschecken von Besuchern-----------------------------------------------

def aktuelleZeit():
    zeit = time.strftime("%d.%m.%Y %H:%M:%S", time.localtime())
    print(zeit)
    print(type(zeit))
    return zeit

besucher = 1
ansprechpartner = "Mister x"
aufenthaltsort = "B240"
ezeit= aktuelleZeit()
print( type(aufenthaltsort))

zeiger.executemany("""INSERT INTO besucherliste(besucher,ansprechpartner,aufenthaltsort) 
               VALUES (?,?,?)""", (besucher, ansprechpartner, aufenthaltsort ))
verbindung.commit()




verbindung.close()