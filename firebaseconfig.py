import pyrebase
import firebase_admin 
from firebase_admin import credentials,firestore
cred = credentials.Certificate("./rehabtesting-9beaf-firebase-adminsdk-xn4fb-c5da403800.json")
firebase_admin.initialize_app(cred)
db = firestore.client()
config = {
  'apiKey': "AIzaSyBPnNnDyGcZmG4Cq-kr3edVwQe5AwthqIE",
  'authDomain': "rehabtesting-9beaf.firebaseapp.com",
  'databaseURL': "https://rehabtesting-9beaf-default-rtdb.asia-southeast1.firebasedatabase.app",
  'projectId': "rehabtesting-9beaf",
  'storageBucket': "rehabtesting-9beaf.appspot.com",
  'messagingSenderId': "737840427844",
  'appId': "1:737840427844:web:4d934ef2d192ac371ddd11",
}
firebase=pyrebase.initialize_app(config)
authe = firebase.auth()