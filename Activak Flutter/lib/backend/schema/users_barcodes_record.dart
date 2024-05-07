import 'dart:async';

import 'package:collection/collection.dart';

import '/backend/schema/util/firestore_util.dart';
import '/backend/schema/util/schema_util.dart';

import 'index.dart';

class UsersBarcodesRecord extends FirestoreRecord {
  UsersBarcodesRecord._(
    super.reference,
    super.data,
  ) {
    _initializeFields();
  }

  // "Email" field.
  String? _email;
  String get email => _email ?? '';
  bool hasEmail() => _email != null;

  // "PhoneNumber" field.
  String? _phoneNumber;
  String get phoneNumber => _phoneNumber ?? '';
  bool hasPhoneNumber() => _phoneNumber != null;

  // "FirstName" field.
  String? _firstName;
  String get firstName => _firstName ?? '';
  bool hasFirstName() => _firstName != null;

  // "LastName" field.
  String? _lastName;
  String get lastName => _lastName ?? '';
  bool hasLastName() => _lastName != null;

  void _initializeFields() {
    _email = snapshotData['Email'] as String?;
    _phoneNumber = snapshotData['PhoneNumber'] as String?;
    _firstName = snapshotData['FirstName'] as String?;
    _lastName = snapshotData['LastName'] as String?;
  }

  static CollectionReference get collection =>
      FirebaseFirestore.instance.collection('UsersBarcodes');

  static Stream<UsersBarcodesRecord> getDocument(DocumentReference ref) =>
      ref.snapshots().map((s) => UsersBarcodesRecord.fromSnapshot(s));

  static Future<UsersBarcodesRecord> getDocumentOnce(DocumentReference ref) =>
      ref.get().then((s) => UsersBarcodesRecord.fromSnapshot(s));

  static UsersBarcodesRecord fromSnapshot(DocumentSnapshot snapshot) =>
      UsersBarcodesRecord._(
        snapshot.reference,
        mapFromFirestore(snapshot.data() as Map<String, dynamic>),
      );

  static UsersBarcodesRecord getDocumentFromData(
    Map<String, dynamic> data,
    DocumentReference reference,
  ) =>
      UsersBarcodesRecord._(reference, mapFromFirestore(data));

  @override
  String toString() =>
      'UsersBarcodesRecord(reference: ${reference.path}, data: $snapshotData)';

  @override
  int get hashCode => reference.path.hashCode;

  @override
  bool operator ==(other) =>
      other is UsersBarcodesRecord &&
      reference.path.hashCode == other.reference.path.hashCode;
}

Map<String, dynamic> createUsersBarcodesRecordData({
  String? email,
  String? phoneNumber,
  String? firstName,
  String? lastName,
}) {
  final firestoreData = mapToFirestore(
    <String, dynamic>{
      'Email': email,
      'PhoneNumber': phoneNumber,
      'FirstName': firstName,
      'LastName': lastName,
    }.withoutNulls,
  );

  return firestoreData;
}

class UsersBarcodesRecordDocumentEquality
    implements Equality<UsersBarcodesRecord> {
  const UsersBarcodesRecordDocumentEquality();

  @override
  bool equals(UsersBarcodesRecord? e1, UsersBarcodesRecord? e2) {
    return e1?.email == e2?.email &&
        e1?.phoneNumber == e2?.phoneNumber &&
        e1?.firstName == e2?.firstName &&
        e1?.lastName == e2?.lastName;
  }

  @override
  int hash(UsersBarcodesRecord? e) => const ListEquality()
      .hash([e?.email, e?.phoneNumber, e?.firstName, e?.lastName]);

  @override
  bool isValidKey(Object? o) => o is UsersBarcodesRecord;
}
