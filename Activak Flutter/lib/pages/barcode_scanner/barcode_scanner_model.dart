import '/flutter_flow/flutter_flow_util.dart';
import 'barcode_scanner_widget.dart' show BarcodeScannerWidget;
import 'package:flutter/material.dart';

class BarcodeScannerModel extends FlutterFlowModel<BarcodeScannerWidget> {
  ///  State fields for stateful widgets in this page.

  final unfocusNode = FocusNode();
  var barcodeResult = '';

  /// Initialization and disposal methods.

  @override
  void initState(BuildContext context) {}

  @override
  void dispose() {
    unfocusNode.dispose();
  }

  /// Action blocks are added here.

  /// Additional helper methods are added here.
}
