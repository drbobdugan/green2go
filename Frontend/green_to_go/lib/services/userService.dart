import 'dart:convert';
import 'package:http/http.dart';

import '../static/user.dart';

class UserService {
  Future postResponse(String path, dynamic params) async {
    Response response = await post(
      "http://198.199.77.174:5000/${path}",
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: params,
    );
    print(response);
    return response.body;
  }

  Future getResponse(String path, String params) async {
    Response response =
        await get("http://198.199.77.174:5000/${path}${params}");
    return response.body;
  }

  dynamic signUp(Map params) async {
    return await postResponse("addUser", params);
  }

  Future<String> logIn(ExistingUser params) async {
    return await postResponse(
        "login",
        jsonEncode(<String, String>{
          'email': params.email,
          'password': params.password
        }));
  }

  dynamic sendCode(Map params) async {
    return null;
  }
}
