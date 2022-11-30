import pyrebase

firebaseConfig = {
  "apiKey": "AIzaSyA_P3tiYVvyNJstCE8r883Qy_J_s0ba5z4",
  "authDomain": "homeauto-57275.firebaseapp.com",
  "databaseURL": "https://homeauto-57275-default-rtdb.firebaseio.com",
  "projectId": "homeauto-57275",
  "storageBucket": "homeauto-57275.appspot.com",
  "messagingSenderId": "366173104513",
  "appId": "1:366173104513:web:60142bf408ae72f040e080",
  "measurementId": "G-09FXMSFZSV"
};

firebase=pyrebase.initialize_app(firebaseConfig)