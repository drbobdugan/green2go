import 'dart:convert';

import '../static/student.dart';
import 'api.dart';

class StudentService {
  final api = new API();

  Future<APIResponse> addContainer(StudentDetails user, String qrCode) async {
    var resp = await api.postResponse(
        "addContainer",
        jsonEncode(<String, String>{
          'email': user.email,
          'qrcode': qrCode,
          'status': 'Checked out',
          'statusUpdateTime': DateTime.now().toString(),
          'auth_token': user.authToken
        }));
    return resp;
  }

  Future<APIResponse> getStudent(StudentAuth userResponse) async {
    var resp = await api.getResponse(
        'getUser?email=${userResponse.email}&auth_token=${userResponse.authToken}');
    return resp;
  }
}
