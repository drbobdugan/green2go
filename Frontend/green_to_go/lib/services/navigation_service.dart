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
}

class NavigationService {
  NavigationService({this.context});

  final BuildContext context;

  Future<void> logout() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('email', null);
    prefs.setString('password', null);
    Navigator.popUntil(context, (Route<dynamic> route) => route.isFirst);
    Navigator.pop(context);
    goToPage(C2RPages.login, null);
  }

  void goHome(StudentDetails user) {
    Navigator.pop(context);
    goToPage(C2RPages.home, user);
  }

  void goToPage(String page, dynamic user) {
    Navigator.pushNamed(context, page, arguments: user);
  }
}
