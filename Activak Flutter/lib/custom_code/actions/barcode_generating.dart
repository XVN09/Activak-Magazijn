// Automatic FlutterFlow imports
import '/backend/backend.dart';
import '/actions/actions.dart' as action_blocks;
import '/flutter_flow/flutter_flow_theme.dart';
import '/flutter_flow/flutter_flow_util.dart';
import 'index.dart'; // Imports other custom actions
import 'package:flutter/material.dart';
// Begin custom action code
// DO NOT REMOVE OR MODIFY THE CODE ABOVE!

import 'package:cloud_firestore/cloud_firestore.dart';
import 'dart:math';

// Define the custom action function
Future<void> barcodeGenerating(String uid) async {
  try {
    // Generate a random 17-digit string
    String randomString = generateRandomString();

    // Access Firestore instance
    FirebaseFirestore firestore = FirebaseFirestore.instance;

    // Specify the path where you want to store the random string data
    DocumentReference userDocRef = firestore.collection('Users').doc(uid);

    // Update the user document with the random string barcode
    await userDocRef.update({
      'userBarcode': randomString,
    });

    // Show a success message or perform any other actions
    print('Barcode generated and uploaded successfully: $randomString');
  } catch (e) {
    // Handle errors
    print('Error generating and uploading barcode: $e');
  }
}

// Function to generate a random 17-digit string
String generateRandomString() {
  Random random = Random();
  String randomString = '';
  for (int i = 0; i < 17; i++) {
    randomString += random.nextInt(10).toString();
  }
  return randomString;
}

// Set your action name, define your arguments and return parameter,
// and then add the boilerplate code using the green button on the right!
