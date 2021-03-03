import 'dart:convert';
import 'package:device_info/device_info.dart';

import 'package:http/http.dart';

class API {
  final String remoteURL = '198.199.77.174:5000';
  final String localURL = '127.0.0.1:5000';

  Future<String> getURL() async {
    DeviceInfoPlugin deviceInfo = DeviceInfoPlugin();
    try {
      AndroidDeviceInfo androidInfo = await deviceInfo.androidInfo;
      if (androidInfo.isPhysicalDevice) return remoteURL;
      return localURL;
    } catch (error) {
      IosDeviceInfo iosInfo = await deviceInfo.iosInfo;
      if (iosInfo.isPhysicalDevice) return remoteURL;
      return localURL;
    }
  }

  Future<APIResponse> postResponse(String path, dynamic params) async {
    return getURL().then((url) async {
      Response response = await post(
        "http://$url/$path",
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: params,
      );
      return APIResponse(jsonDecode(response.body));
    });
  }

  Future<APIResponse> getResponse(String path) async {
    return getURL().then((url) async {
      Response response = await get("http://$url/$path");
      return APIResponse(jsonDecode(response.body));
    });
  }
}

class APIResponse {
  bool success;
  String message;
  dynamic data;

  APIResponse(Map<String, dynamic> value) {
    success = value['success'];
    message = value['message'];
    data = value['data'];
  }
}

class UserResponse {
  String email;
  String authToken;
  String refreshToken;
  String tokenExpiration;

  UserResponse(Map<String, dynamic> value) {
    email = value['user'];
    authToken = value['auth_token'];
    refreshToken = value['refresh_token'];
    tokenExpiration = value['expires_at'];
  }
}
