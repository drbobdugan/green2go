import 'dart:convert';

import '../static/user.dart';
import 'api.dart';

class UserService {
  final api = new API();

  Future<APIResponse> validateCode(NewUser user, String code) async {
    var resp = await api.postResponse(
        "validateCode",
        jsonEncode(<String, String>{
          'email': user.email,
          'code': code,
        }));
    return resp;
  }

  Future<APIResponse> signUp(NewUser user) async {
    var resp = await api.postResponse(
        "addUser",
        jsonEncode(<String, String>{
          'email': user.email,
          'password': user.password,
          'firstName': user.firstName,
          'middleName': user.middleName,
          'lastName': user.lastName,
          'phoneNum': user.phoneNum,
          'classYear': user.classYear,
          'role': "RegularUser"
        }));
    return resp;
  }

  Future<APIResponse> logIn(ExistingUser user) async {
    var resp = await api.postResponse(
        "login",
        jsonEncode(
            <String, String>{'email': user.email, 'password': user.password}));
    return resp;
  }

  dynamic sendCode(Map params) async {
    return null;
  }
}
