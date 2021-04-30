import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../static/student.dart';

class C2RPages {
  static const String home = '/home';
  static const String login = '/login';
  static const String signup = '/signup';
  static const String validation = '/validation';
  static const String checkoutContainer = '/checkoutContainer';
  static const String returnContainer = '/returnContainer';
  static const String containerList = '/containerList';
  static const String profile = '/profile';
  static const String changePassword = '/changePassword';
  static const String forgotPassword = '/forgotPassword';
  static const String points = '/points';
}

class NavigationService {
  NavigationService({this.context});

  final BuildContext context;

  void toRoot() {
    Navigator.popUntil(context, (Route<dynamic> route) => route.isFirst);
    Navigator.pop(context);
  }

  Future<void> logout() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('email', null);
    prefs.setString('password', null);
    toRoot();
    goToPage(C2RPages.login, null);
  }

  void goHome(StudentAuth user) {
    toRoot();
    goToPage(C2RPages.home, user);
  }

  void goToPage(String page, dynamic user) {
    Navigator.pushNamed(context, page, arguments: user);
  }
}
