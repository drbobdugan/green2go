import 'dart:convert';

import '../static/student.dart';
import 'api.dart';

class StudentService {
  final api = new API();

  Future<APIResponse> addContainer(Student user, String qrCode) async {
    var resp = await api.postResponse(
        "addContainer",
        jsonEncode(<String, String>{
          'email': user.email,
          'qrcode': qrCode,
          'status': 'Checked out',
          'statusUpdateTime': DateTime.now().toString()
        }));
    return resp;
  }

  Future<Student> getStudent(String email) async {
    Student student = new Student();
    var resp = await api.getResponse('getUser?email=${email}');
    Map json = jsonDecode(resp);
    student.jsonToStudent(json['data']);
    return student;
  }
}
