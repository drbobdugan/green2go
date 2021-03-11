import 'dart:convert';

import '../static/student.dart';
import 'api.dart';

class StudentService {
  static Future<APIResponse> checkoutContainer(
      StudentAuth auth, String qrCode) async {
    final APIResponse resp = await API.postResponse(
        'checkoutContainer',
        jsonEncode(<String, String>{
          'email': auth.email,
          'qrcode': qrCode,
          'status': 'Checked out',
          'auth_token': auth.token,
          'location_qrcode': 'None'
        }));
    return resp;
  }

  static Future<APIResponse> checkLocation(
      StudentAuth auth, String locationqrCode) async {
    final APIResponse resp = await API.postResponse(
        'selectLocation',
        jsonEncode(<String, String>{
          'email': auth.email,
          'qrcode': locationqrCode,
          'auth_token': auth.token,
        }));
    return resp;
  }

  static Future<APIResponse> returnContainer(
      StudentAuth auth, String qrCode, String locationqrCode) async {
    final APIResponse resp = await API.postResponse(
        'checkinContainer',
        jsonEncode(<String, String>{
          'email': auth.email,
          'qrcode': qrCode,
          'status': 'Unverified return',
          'auth_token': auth.token,
          'location_qrcode': locationqrCode
        }));
    return resp;
  }

  static Future<APIResponse> getContainers(StudentAuth auth) async {
    final APIResponse resp = await API.getResponse(
        'getContainersForUser?email=${auth.email}&auth_token=${auth.token}');
    return resp;
  }
}
