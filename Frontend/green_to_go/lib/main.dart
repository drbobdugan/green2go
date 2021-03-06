import 'package:flutter/material.dart';

import 'components/custom_theme.dart';
import 'pages/checkoutContainer.dart';
import 'pages/home.dart';
import 'pages/login.dart';
import 'pages/returnContainer.dart';
import 'pages/signup.dart';
import 'pages/validation.dart';
import 'static/student.dart';
import 'static/user.dart';

void main() {
  runApp(
    const Choose2ReuseApp(),
  );
}

class Choose2ReuseApp extends StatefulWidget {
  const Choose2ReuseApp({Key key}) : super(key: key);

  @override
  _Choose2ReuseAppState createState() => _Choose2ReuseAppState();
}

class _Choose2ReuseAppState extends State<Choose2ReuseApp> {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Choose2Reuse',
      theme: CustomTheme.appTheme(),
      home: const LoginPage(),
      onGenerateRoute: (RouteSettings settings) {
        return MaterialPageRoute<dynamic>(builder: (BuildContext context) {
          switch (settings.name) {
            case '/home':
              return HomePage(user: settings.arguments as StudentDetails);
            case '/login':
              return const LoginPage();
            case '/signup':
              return const SignUpPage();
            case '/validation':
              return ValidationPage(user: settings.arguments as NewUser);
            case '/checkoutContainer':
              return CheckoutContainerPage(
                  user: settings.arguments as StudentDetails);
            case '/returnContainer':
              return ReturnContainerPage(
                  user: settings.arguments as StudentDetails);
            default:
              break;
          }
          return const LoginPage();
        });
      },
    );
  }
}
