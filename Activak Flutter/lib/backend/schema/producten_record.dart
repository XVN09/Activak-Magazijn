import 'dart:async';

import 'package:collection/collection.dart';

import '/backend/schema/util/firestore_util.dart';
import '/backend/schema/util/schema_util.dart';

import 'index.dart';

class ProductenRecord extends FirestoreRecord {
  ProductenRecord._(
    super.reference,
    super.data,
  ) {
    _initializeFields();
  }

  // "Barcode" field.
  String? _barcode;
  String get barcode => _barcode ?? '';
  bool hasBarcode() => _barcode != null;

  // "Category" field.
  String? _category;
  String get category => _category ?? '';
  bool hasCategory() => _category != null;

  // "Description" field.
  String? _description;
  String get description => _description ?? '';
  bool hasDescription() => _description != null;

  // "Image" field.
  String? _image;
  String get image => _image ?? '';
  bool hasImage() => _image != null;

  // "Place" field.
  String? _place;
  String get place => _place ?? '';
  bool hasPlace() => _place != null;

  // "Title" field.
  String? _title;
  String get title => _title ?? '';
  bool hasTitle() => _title != null;

  // "isTracked" field.
  bool? _isTracked;
  bool get isTracked => _isTracked ?? false;
  bool hasIsTracked() => _isTracked != null;

  // "isTracking" field.
  bool? _isTracking;
  bool get isTracking => _isTracking ?? false;
  bool hasIsTracking() => _isTracking != null;

  // "Price" field.
  String? _price;
  String get price => _price ?? '';
  bool hasPrice() => _price != null;

  // "BasisStock" field.
  String? _basisStock;
  String get basisStock => _basisStock ?? '';
  bool hasBasisStock() => _basisStock != null;

  void _initializeFields() {
    _barcode = snapshotData['Barcode'] as String?;
    _category = snapshotData['Category'] as String?;
    _description = snapshotData['Description'] as String?;
    _image = snapshotData['Image'] as String?;
    _place = snapshotData['Place'] as String?;
    _title = snapshotData['Title'] as String?;
    _isTracked = snapshotData['isTracked'] as bool?;
    _isTracking = snapshotData['isTracking'] as bool?;
    _price = snapshotData['Price'] as String?;
    _basisStock = snapshotData['BasisStock'] as String?;
  }

  static CollectionReference get collection =>
      FirebaseFirestore.instance.collection('Producten');

  static Stream<ProductenRecord> getDocument(DocumentReference ref) =>
      ref.snapshots().map((s) => ProductenRecord.fromSnapshot(s));

  static Future<ProductenRecord> getDocumentOnce(DocumentReference ref) =>
      ref.get().then((s) => ProductenRecord.fromSnapshot(s));

  static ProductenRecord fromSnapshot(DocumentSnapshot snapshot) =>
      ProductenRecord._(
        snapshot.reference,
        mapFromFirestore(snapshot.data() as Map<String, dynamic>),
      );

  static ProductenRecord getDocumentFromData(
    Map<String, dynamic> data,
    DocumentReference reference,
  ) =>
      ProductenRecord._(reference, mapFromFirestore(data));

  @override
  String toString() =>
      'ProductenRecord(reference: ${reference.path}, data: $snapshotData)';

  @override
  int get hashCode => reference.path.hashCode;

  @override
  bool operator ==(other) =>
      other is ProductenRecord &&
      reference.path.hashCode == other.reference.path.hashCode;
}

Map<String, dynamic> createProductenRecordData({
  String? barcode,
  String? category,
  String? description,
  String? image,
  String? place,
  String? title,
  bool? isTracked,
  bool? isTracking,
  String? price,
  String? basisStock,
}) {
  final firestoreData = mapToFirestore(
    <String, dynamic>{
      'Barcode': barcode,
      'Category': category,
      'Description': description,
      'Image': image,
      'Place': place,
      'Title': title,
      'isTracked': isTracked,
      'isTracking': isTracking,
      'Price': price,
      'BasisStock': basisStock,
    }.withoutNulls,
  );

  return firestoreData;
}

class ProductenRecordDocumentEquality implements Equality<ProductenRecord> {
  const ProductenRecordDocumentEquality();

  @override
  bool equals(ProductenRecord? e1, ProductenRecord? e2) {
    return e1?.barcode == e2?.barcode &&
        e1?.category == e2?.category &&
        e1?.description == e2?.description &&
        e1?.image == e2?.image &&
        e1?.place == e2?.place &&
        e1?.title == e2?.title &&
        e1?.isTracked == e2?.isTracked &&
        e1?.isTracking == e2?.isTracking &&
        e1?.price == e2?.price &&
        e1?.basisStock == e2?.basisStock;
  }

  @override
  int hash(ProductenRecord? e) => const ListEquality().hash([
        e?.barcode,
        e?.category,
        e?.description,
        e?.image,
        e?.place,
        e?.title,
        e?.isTracked,
        e?.isTracking,
        e?.price,
        e?.basisStock
      ]);

  @override
  bool isValidKey(Object? o) => o is ProductenRecord;
}
