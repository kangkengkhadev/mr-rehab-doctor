import pyrebase
import firebase_admin 
from firebase_admin import credentials, firestore

# Firebase Admin SDK (for Firestore access)
cred = credentials.Certificate("rehabtesting-9beaf-firebase-adminsdk-xn4fb-c5da403800.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

# Pyrebase (for Auth and Realtime Database access)
config = {
}
firebase = pyrebase.initialize_app(config)
authe = firebase.auth()