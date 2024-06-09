import sqlite3
from datetime import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import sys

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


    try:
     zeiger.execute(sql_anweisung)
    except:
        print("Creating Table failed")

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
    

    try:
     zeiger.execute(sql_anweisung)
    except:
        print("Creating Table failed")
    verbindung.commit()

def proofUniqueNumber(proofedNumber,counts):
    uniqueNumber = True
    for i in range(counts):
        if proofedNumber == inhalt[i][0]:
            uniqueNumber = 0
        
    return uniqueNumber

def CreateBesuchernr():

    try:
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
    except:
        print("Error: Creating Besuchernr")



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
def SendMail():
    sender_email = "firmaxy@example.com"
    receiver_email = "besucher@example.com"
    subject = "Bestätigungsmail"
    body = """Sehr geehrter Besucher,\n wir bitten sie die im Anhang beigefügte Datenschutzerklärung  zuzustimmen, um sie in unser Besucherverwaltungssystem aufnehmen zu können. 
    Im Folgenden finden sie die Sicherheitsunterweisungen, die sie bis zu ihrem Aufenthalt in 
    unserer Firma durchgeführt haben müssen: 


    Mit freundlichen Grüßen
    Empfang Firma xy"""

    # E-Mail-Nachricht erstellen
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject

    # Nachrichtentext hinzufügen
    message.attach(MIMEText(body, "plain"))

    # Nachricht drucken (anstatt sie wirklich zu versenden)
    print("E-Mail von:", sender_email)
    print("E-Mail an:", receiver_email)
    print("Betreff:", subject)
    print("Nachricht:")
    print(body)


def BesucherAnlegen(vname,name,rolle):
    besuchernr = int(CreateBesuchernr())
    print("Der Besucher bekommt die Nummer: " + str(besuchernr))
    vorname = vname
    nachname = name

    try:
     zeiger.execute("INSERT INTO besucher VALUES (?,?,?,?)", (besuchernr,vorname, nachname,rolle))
    except:
        print("Error: Besucher anlegen")
    verbindung.commit()
    SendMail()

CreateTables()   # muss
#BesucherAnlegen("Theresia","Deubert", "Handwerker")


#Einchecken/Auschecken von Besuchern-----------------------------------------------

def aktuelleZeit():
    currtime= datetime.now()
    zeit = currtime.strftime("%d.%m.%Y %H:%M:%S", )
    #print(zeit)
    #print(type(zeit))
    return zeit

def proofBesuchernr(besuchernr):
    try:
        zeiger.execute("SELECT besuchernr FROM besucher WHERE besuchernr= ?", (besuchernr,))
        
        if (zeiger.fetchone() != None):
            proofed = True
        else:
            proofed = False
    except:
        print("Error: proofBesuchernumber")

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
    try:
        zeiger.execute("SELECT COUNT(*) FROM besucherliste WHERE auscheckzeit IS NULL")
        anzahl = zeiger.fetchone()
        #print(anzahl[0])
    except:
        print("Error: Abfrage aktuelle Besucheranzahl")
    return anzahl[0]

#anzahl = AbfrageAktBesucheranzahl()
#print("Die aktuelle Besucheranzahl ist " + str(anzahl))

#Abfrage Besucheranzahl zu bestimmten Datum-----------------------------------------------------
#zeitpunkt = datetime.datetime(2023, 5, 30)     für Test Datentyp Date
zeitpunkt = "30.05.2024"

def AbfrageBesucheranzahl(zeitpunkt):
    try:
        zeiger.execute("SELECT COUNT(*) FROM besucherliste WHERE auscheckzeit LIKE ? OR eincheckzeit LIKE ?",(zeitpunkt + '%',zeitpunkt + '%'))
        anzahl = zeiger.fetchone()
        #print(anzahl[0])

        zeiger.execute("""SELECT b1.besucher, b2.vorname, b2.nachname, b2.Rolle, b1.eincheckzeit, b1.auscheckzeit, b1.ansprechpartner, b1.Aufenthaltsort
                    FROM besucherliste b1, besucher b2 
                    WHERE (auscheckzeit LIKE ? OR eincheckzeit LIKE ?) and b1.besucher = b2.besuchernr""",(zeitpunkt + '%',zeitpunkt + '%'))
        inhalt = zeiger.fetchall()
        #print(inhalt)
        print("Es wurden " + str(anzahl[0]) + " Besucher zum angegebenen Zeitpunkt gefunden: " + str(inhalt))
    except:
        print("Error: Abfrage Besucheranzahl")
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

#UpdateBesucher(3,"Handwerker")

#Löschen von Besucher-------------

besucher = 4
def DeleteBesucher(besuchernr):
    try:
        zeiger.execute("DELETE FROM besucher WHERE besuchernr=?", (besuchernr,))
        zeiger.execute("DELETE FROM besucherliste WHERE besucher=?", (besuchernr,))
        verbindung.commit()
    except:
        print("Error: Delete Besucher")
#DeleteBesucher(besucher)

def function():
    print("Hello World")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
        if function_name == "function":
            print(AbfrageAktBesucheranzahl())
        else:
            print("Unknown function")
    else:
        print("No function specified")


verbindung.close()