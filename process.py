import subprocess
import time
import os
from utils import *


def scan(t,path,  output_file):

    naps2Path = os.path.join(path,"naps2\\App\\naps2.console")
    cmd = "{} -o {} -f".format(naps2Path, output_file)
    response = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    out, err = response.communicate()

    return {"status":out.decode("utf-8")}


def process(data, t):
    path = os.path.dirname(__file__)
    pdfName = t.replace(".", ":").replace(" ", "_").replace(':','-')
    output_file = os.path.join(path,FOLDER_NAME + "\\" + "{}.pdf".format(pdfName))
    try:
        firebase = pyrebase.initialize_app(firebaseConfig)

        auth = firebase.auth()
        creds = readCred()
        # Log the user in
        user = auth.sign_in_with_email_and_password(creds['email'], creds['pwd'])
        db = firebase.database()
        store = firebase.storage()
    except:
        return INTERNET_PROBLEM

    t1 = time.time()
    NotYetScanned = True
    while NotYetScanned:
        t2 =  time.time()
        response = scan(t,path, output_file)
        if (not (response == NO_PAPER_FOUND)) or abs(t2-t1) > TIME_TO_WAIT:
            NotYetScanned = False
        time.sleep(1)
        if response in [SUCCESS_SCAN, PAPER_JAM]:
            saveDataSuccess(data, t)
            results = db.child(creds["pc"]).push(data, user['idToken'])
            if response == SUCCESS_SCAN:
                store.child(creds["pc"]+"/"+pdfName).put(output_file, user['idToken'])

    return response
