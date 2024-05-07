import 'package:flutter/material.dart';

class FFAppState extends ChangeNotifier {
  static FFAppState _instance = FFAppState._internal();

  factory FFAppState() {
    return _instance;
  }

  FFAppState._internal();

  static void reset() {
    _instance = FFAppState._internal();
  }

  Future initializePersistedState() async {}

  void update(VoidCallback callback) {
    callback();
    notifyListeners();
  }

  bool _searchActive = false;
  bool get searchActive => _searchActive;
  set searchActive(bool value) {
    _searchActive = value;
  }

  String _scannedBarcode = '0';
  String get scannedBarcode => _scannedBarcode;
  set scannedBarcode(String value) {
    _scannedBarcode = value;
  }

  bool _isUserAuthenticated = true;
  bool get isUserAuthenticated => _isUserAuthenticated;
  set isUserAuthenticated(bool value) {
    _isUserAuthenticated = value;
  }

  String _clickedItem = '';
  String get clickedItem => _clickedItem;
  set clickedItem(String value) {
    _clickedItem = value;
  }
}
