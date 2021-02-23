import 'dart:convert';
import 'package:http/http.dart';

import '../static/user.dart';

class UserService {
  Future postResponse(String path, dynamic params) async {
    Response response = await post(
      "http://198.199.77.174:5000/$path",
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: params,
    );
    print(response);
    return response.body;
  }

  Future getResponse(String path, String params) async {
    Response response = await get("http://198.199.77.174:5000/$path$params");
    return response.body;
  }

  Future<bool> validateCode(NewUser user, String code) async {
    var resp = await postResponse(
        "validateCode",
        jsonEncode(<String, String>{
          'email': user.email,
          'code': code,
        }));
    return resp == "Success";
  }

  Future<bool> signUp(NewUser user) async {
    var resp = await postResponse(
        "addUser",
        jsonEncode(<String, String>{
          'email': user.email,
          'password': user.password,
          'firstName': user.firstName,
          'middleName': user.middleName,
          'lastName': user.lastName,
          'phoneNum': user.phoneNum,
          'classYear': user.firstName
        }));
    return resp == "Success";
  }

  Future<bool> logIn(ExistingUser user) async {
    var resp = await postResponse(
        "login",
        jsonEncode(
            <String, String>{'email': user.email, 'password': user.password}));
    return resp == "Success!";
  }

  dynamic sendCode(Map params) async {
    return null;
  }
}
