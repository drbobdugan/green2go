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
      if (response != null && response.body != null) {
        return APIResponse(jsonDecode(response.body));
      }
      return APIResponse({
        'success': false,
        'message': 'An error occured, please try again later.'
      });
    });
  }

  Future getResponse(String path, String params) async {
    return getURL().then((url) async {
      Response response = await get("http://$url/$path$params");
      return response.body;
    });
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
