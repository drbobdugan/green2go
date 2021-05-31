import 'dart:convert';
import 'dart:io' show Platform;
import 'package:package_info/package_info.dart';
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

  static Future<APIResponse> forgotPassword(
      String authCode, String email, String password) async {
    final APIResponse resp = await API.patchResponse(
        'forgetPassword',
        jsonEncode(<String, String>{
          'code': authCode,
          'email': email,
          'newPass': password,
          'auth_token': 'None'
        }));
    return resp;
  }

  //Returns True if users version is correct, if not returns False
  static Future<APIResponse> versionCheck() async {
    String host = '';
    if (Platform.isAndroid) {
      host = 'Android';
    } else if (Platform.isIOS) {
      host = 'iOS';
    }

    PackageInfo packageInfo = await PackageInfo.fromPlatform();

    String version = packageInfo.version;

    final APIResponse resp =
        await API.getResponse('getVersion?host=${host}&version=${version}');

    if (version == resp.data) {
      return resp;
    } else {
      resp.data = "Not correct version";
      return resp;
    }
  }
}
