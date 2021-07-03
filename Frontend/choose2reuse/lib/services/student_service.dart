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
          'status': 'Checked Out',
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
          'status': 'Pending Return',
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

  static Future<APIResponse> getSortedContainers(StudentAuth auth) async {
    final APIResponse resp = await API.getResponse(
        'getSortedContainers?email=${auth.email}&auth_token=${auth.token}');
    return resp;
  }

  static Future<APIResponse> reportContainer(
      StudentAuth auth, String qrCode, String description) async {
    final APIResponse resp = await API.postResponse(
        'reportContainer',
        jsonEncode(<String, String>{
          'email': auth.email,
          'qrcode': qrCode,
          'status': 'Damaged Lost',
          'auth_token': auth.token,
          'description': description
        }));
    return resp;
  }

  static Future<APIResponse> undoReportContainer(
      StudentAuth auth, String qrCode) async {
    final APIResponse resp = await API.postResponse(
        'undoReportContainer',
        jsonEncode(<String, String>{
          'email': auth.email,
          'qrcode': qrCode,
          'auth_token': auth.token,
        }));
    return resp;
  }

  static Future<APIResponse> claimReward(StudentAuth auth) async {
    final APIResponse resp = await API.postResponse(
        'claimReward',
        jsonEncode(<String, String>{
          'email': auth.email,
          'auth_token': auth.token,
        }));
    return resp;
  }
}
