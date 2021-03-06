import 'dart:convert';

import '../static/student.dart';
import 'api.dart';

class StudentService {
  static Future<APIResponse> addContainer(
      StudentDetails user, String qrCode) async {
    final APIResponse resp = await API.postResponse(
        'addContainer',
        jsonEncode(<String, String>{
          'email': user.email,
          'qrcode': qrCode,
          'status': 'Checked out',
          'statusUpdateTime': DateTime.now().toString(),
          'auth_token': user.auth.token
        }));
    return resp;
  }

  static Future<APIResponse> getStudent(StudentAuth userResponse) async {
    final APIResponse resp = await API.getResponse(
        'getUser?email=${userResponse.email}&auth_token=${userResponse.token}');
    return resp;
  }
}
