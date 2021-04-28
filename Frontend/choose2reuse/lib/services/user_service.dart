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
        }));
    return resp;
  }

  static Future<APIResponse> signUp(NewUser user) async {
    print('entering');
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
        print('here in reponse');
        print(resp);
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

  static Future<APIResponse> getUser(StudentAuth auth) async {
    final APIResponse resp = await API
        .getResponse('getUser?email=${auth.email}&auth_token=${auth.token}');
    return resp;
  }

  static Future<APIResponse> updateUser(
      StudentAuth auth, DetailedUser user) async {
    final APIResponse resp = await API.patchResponse(
        'updateUser',
        jsonEncode(<String, String>{
          'email': auth.email,
          'firstName': user.firstName,
          'middleName': user.middleName,
          'lastName': user.lastName,
          'phoneNum': user.phoneNum,
          'auth_token': auth.token,
        }));
    return resp;
  }

  static Future<APIResponse> changePassword(
      StudentAuth auth, String oldPass, String newPass) async {
    final APIResponse resp = await API.patchResponse(
        'changePassword',
        jsonEncode(<String, String>{
          'email': auth.email,
          'oldPass': oldPass,
          'newPass': newPass,
          'auth_token': auth.token,
        }));
    return resp;
  }
}
