import smtplib
from datetime import datetime
from email.mime.text import MIMEText
import json
from dotenv import load_dotenv
import os

load_dotenv("password.env") 

def send_email(email, text):
    emailUsername = os.getenv("EmailUsername")
    appPassword =os.getenv("AppPassword")
    smtpserver = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    smtpserver.ehlo()
    smtpserver.login(emailUsername, appPassword)
    sentFrom = emailUsername
    sentTo = email
    emailText = MIMEText(text)
    smtpserver.sendmail(sentFrom, sentTo, emailText.as_string())
    smtpserver.close()

with open("users.json", "r", encoding="utf-8") as file:
    data = json.load(file)

today= datetime.today().date()
#print(today)

#Διάσχιση λίστας των χρηστών
for user in data:
    flag=0 # αρχικοποίηση για κάθε χρήστη
    lista=list() # αρχικοποίηση για κάθε χρήστη, κενή λίστα
    print(data[user]["name"]) 
    for acc in data[user]["accounts"]:           #Διάσχιση λογαριασμών κάθε χρήστη
        print(acc["type"], "expires on:", acc["expireDate"])
        a=datetime.strptime(acc["expireDate"], '%Y-%m-%d').date()
        print((a-today).days)
        if (a-today).days <= 3 and acc["status"]=="Δεν έχει σταλεί":
            print("(πρέπει να σταλεί)")
            flag=1    # αν έστω και ένας λογαριασμός λήγει σύντομα, θα σταλεί email
            lista.append(acc)      #αποθήκευση των λογαριασμών που θα λήξουν σε προσωρινή λίστα
            #stoixeia logariasmou -> sto array
    if flag==1 :
        keimeno = f"Αγαπητέ/ή {data[user]["name"]}, \n"
        for log in lista: # οι λογαριασμοί του user που θα λήξουν σε <= 3 μέρες
            keimeno+= f"Ο λογαριασμός {log["type"]} λήγει στις {log["expireDate"]}. Ποσό: {log["amount"]} ευρώ.\n"
        try:        # έλεγχος σφάλματος ώστε πρώτα να σταλεί το email και μετά να αλλάξει η κατάστση ειδοποίησης
            send_email(data[user]["email"], keimeno)
        except smtplib.SMTPException as e:
            print(f"Σφάλμα: {e}")
        else:
            for log in lista:   # αν δεν υπάρξει σφάλμα, αλλάζει η κατάσταση ειδοποίησης
                log["status"]= "Ειδοποίηση - Στάλθηκε"
            print("στάλθηκε")
        print(keimeno)      # δοκιμή-εμφάνιση κειμένου email για κάθε χρήστη
        
# ενημέρωση του αρχείου json
with open("users.json", "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)  