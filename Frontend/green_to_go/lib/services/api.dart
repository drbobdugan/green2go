import 'dart:convert';

import 'package:http/http.dart';

class API {
  final String baseURL = '198.199.77.174:5000';
  final String localURL = '127.0.0.1:5000';

  Future<APIResponse> postResponse(String path, dynamic params) async {
    Response response = await post(
      "http://$baseURL/$path",
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: params,
    );
    if (response != null && response.body != null) {
      return APIResponse(jsonDecode(response.body));
    }
    return APIResponse({
      'success': false,
      'message': 'An error occured, please try again later.'
    });
  }

  Future getResponse(String path, String params) async {
    Response response = await get("http://$baseURL/$path$params");
    return response.body;
  }
}

class APIResponse {
  bool success;
  String message;

  APIResponse(Map<String, dynamic> value) {
    success = value['success'];
    message = value['message'];
  }
}
