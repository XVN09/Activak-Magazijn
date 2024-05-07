import 'package:firebase_core/firebase_core.dart';
import 'package:flutter/foundation.dart';

Future initFirebase() async {
  if (kIsWeb) {
    await Firebase.initializeApp(
        options: const FirebaseOptions(
            apiKey: "AIzaSyC6uTdsptYIJ795bYo1KDVyQg2kTePfL30",
            authDomain: "activak-57cf3.firebaseapp.com",
            projectId: "activak-57cf3",
            storageBucket: "activak-57cf3.appspot.com",
            messagingSenderId: "745750044643",
            appId: "1:745750044643:web:651556d8332efa09034ad6",
            measurementId: "G-4G8ZEE86H7"));
  } else {
    await Firebase.initializeApp();
  }
}
