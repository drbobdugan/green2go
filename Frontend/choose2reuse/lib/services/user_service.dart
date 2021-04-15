import 'dart:convert';

import '../static/student.dart';
import '../static/user.dart';
import 'api.dart';

class UserService {
  static Future<APIResponse> validateCode(String email, String code) async {
    final APIResponse resp = await API.postResponse(
        'validateCode',
        jsonEncode(<String, String>{
          'email': email,
          'code': code,
        }));
    return resp;
  }

  static Future<APIResponse> resendCode(String email) async {
    final APIResponse resp = await API.postResponse(
        'resendAuthCode',
        jsonEncode(<String, String>{
          'email': email,
          'auth_token': 'None',
        }));
    return resp;
  }

  static Future<APIResponse> signUp(NewUser user) async {
    final APIResponse resp = await API.postResponse(
        'addUser',
        jsonEncode(<String, String>{
          'email': user.email,
          'password': user.password,
          'firstName': user.firstName,
          'middleName': user.middleName,
          'lastName': user.lastName,
          'phoneNum': user.phoneNum,
          'role': 'RegularUser'
        }));
    return resp;
  }

  static Future<APIResponse> logIn(ExistingUser user) async {
    final APIResponse resp = await API.postResponse(
        'login',
        jsonEncode(
            <String, String>{'email': user.email, 'password': user.password}));
    return resp;
  }

  static dynamic sendCode(dynamic params) async {
    return null;
  }

  static Future<APIResponse> getUser(
      ExistingUser user, StudentAuth auth) async {
    final APIResponse resp = await API
        .getResponse('getUser?email=${user.email}&auth_token=${auth.token}');
    return resp;
  }
}
