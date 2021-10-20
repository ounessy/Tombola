import json
import pyrebase
import requests


## variables
NO_DEVICE_FOUND = {'status': 'The selected scanner is offline.\r\nNo scanned pages to export.\r\n'}
NO_PAPER_FOUND = {'status': 'No scanned pages to export.\r\n'}
PAPER_JAM = {'status': 'The scanner has a paper jam.\r\nNo scanned pages to export.\r\n'}
SUCCESS = {"status": "success"}
FOLDER_NAME = "scans"
TIME_TO_WAIT = 20
INTERNET_PROBLEM = {"status": "Internet problem"}
SUCCESS_SCAN = {'status': ''}

## Functions



firebaseConfig = {
  "apiKey": "AIzaSyC-NiIRFTl2fip6BakLYkR2Vw-qag3ASxM",
  "authDomain": "omotombola.firebaseapp.com",
  "databaseURL": "https://omotombola-default-rtdb.firebaseio.com",
  "projectId": "omotombola",
  "storageBucket": "omotombola.appspot.com",
  "messagingSenderId": "604483029163",
  "appId": "1:604483029163:web:a20df8ca43b8dcdf24cfee",
  "measurementId": "G-4W6Y8GN838"
}

def sendSMS(num):
    apiLink = 'http://www.nihitech.org/'
    r = requests.post(apiLink, data={'phone': num})

    return r


def saveToFB(data):
    try:
        firebase = pyrebase.initialize_app(firebaseConfig)

        auth = firebase.auth()
        creds = readCred()
        # Log the user in
        user = auth.sign_in_with_email_and_password(creds['email'], creds['pwd'])

        # Get a reference to the database service
        db = firebase.database()


        # Pass the user's idToken to the push method
        results = db.child(creds["pc"]).push(data, user['idToken'])
        return True

    except:
        return INTERNET_PROBLEM

def saveData(data, time):
    if type(data) == dict and len(data) >0:
        data["time"] = time
        with open("operations.txt", "a") as f:
            f.write(str(data))
            f.write("\n")
        return True
    else:
        return False

def saveDataSuccess(data, time):
    if type(data) == dict and len(data) >0:
        data["time"] = time
        with open("operations_success.txt", "a") as f:
            f.write(str(data))
            f.write("\n")
        return True
    else:
        return False

def readCred(filePath= "creds.json"):
    with open(filePath, "r") as f:
        data = json.loads(f.read())
    return data