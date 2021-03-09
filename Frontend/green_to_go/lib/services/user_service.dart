import 'dart:convert';

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
          'classYear': user.classYear,
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
}
