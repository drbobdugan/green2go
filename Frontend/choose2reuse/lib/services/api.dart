import 'dart:convert';
import 'package:device_info/device_info.dart';

import 'package:http/http.dart';

class APIResponse {
  APIResponse(Map<String, dynamic> value) {
    success = value['success'] as bool;
    message = value['message'] as String;
    data = value['data'];
  }

  bool success;
  String message;
  dynamic data;
}

class API {
  static Future<String> getURL() async {
    const String remoteURL = '198.199.77.174:5000';
    const String localURL = '127.0.0.1:5000';
    const String localAndroidURL = '10.0.2.2:5000';

    final DeviceInfoPlugin deviceInfo = DeviceInfoPlugin();
    try {
      final AndroidDeviceInfo androidInfo = await deviceInfo.androidInfo;
      if (androidInfo.isPhysicalDevice) {
        return remoteURL;
      }
      return localAndroidURL;
    } catch (error) {
      final IosDeviceInfo iosInfo = await deviceInfo.iosInfo;
      if (iosInfo.isPhysicalDevice) {
        return remoteURL;
      }
      return localURL;
    }
  }

  static Future<APIResponse> postResponse(String path, dynamic params) async {
    return getURL().then((String url) async {
      final Response response = await post(
        'http://$url/$path',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: params,
      );
      return formatResponse(response);
    });
  }

  static Future<APIResponse> patchResponse(String path, dynamic params) async {
    return getURL().then((String url) async {
      final Response response = await patch(
        'http://$url/$path',
        headers: <String, String>{
          'Content-Type': 'application/json; charset=UTF-8',
        },
        body: params,
      );
      return formatResponse(response);
    });
  }

  static Future<APIResponse> getResponse(String path) async {
    return getURL().then((String url) async {
      final Response response = await get('http://$url/$path');
      return formatResponse(response);
    });
  }

  static APIResponse formatResponse(Response response) {
    switch (response.statusCode) {
      case 200:
        return APIResponse(jsonDecode(response.body) as Map<String, dynamic>);
      case 400:
        return APIResponse(<String, dynamic>{
          'success': false,
          'message':
              '** 400: Bad Request Exception **' + response.body.toString()
        });
      case 401:
      case 403:
        return APIResponse(<String, dynamic>{
          'success': false,
          'message':
              '** 401/403: Unauthorized Exception **' + response.body.toString()
        });
      case 500:
      default:
        throw APIResponse(<String, dynamic>{
          'success': false,
          'message':
              '** Fetch Data Exception - Error occured while Communication with Server with StatusCode: ${response.statusCode}'
        });
    }
  }
}
