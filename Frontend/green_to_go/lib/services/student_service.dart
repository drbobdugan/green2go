import 'dart:convert';

import '../static/student.dart';
import 'api.dart';

class StudentService {
  final api = new API();

  Future<bool> addContainer(Student user, String qrCode) async {
    var resp = await api.postResponse(
        "addContainer",
        jsonEncode(<String, String>{
          'email': user.email,
          'qrcode': qrCode,
          'status': 'Checked out',
          'statusUpdateTime': DateTime.now().toString()
        }));
    return resp == "Success";
  }
}
