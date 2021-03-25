import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:pusher_beams/pusher_beams.dart';

import 'pages/checkoutContainer.dart';
import 'pages/containerList.dart';
import 'pages/home.dart';
import 'pages/login.dart';
import 'pages/returnContainer.dart';
import 'pages/signup.dart';
import 'pages/validation.dart';
import 'static/custom_theme.dart';
import 'static/strings.dart';
import 'static/student.dart';
import 'static/user.dart';

void main() async {
  /*WidgetsFlutterBinding.ensureInitialized();

  try {
    await PusherBeams.start('7032df3e-e5a8-494e-9fc5-3b9f05a68e3c');
  } on FormatException {
    print('Failed to connect to Pusher Beams');
  }*/

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
  void initState() {
    super.initState();
    //initInterests();
  }

  /*Future<void> initInterests() async {
    try {
      await PusherBeams.addDeviceInterest('hello');
      await PusherBeams.addDeviceInterest('debug-hello');

      final interests = await PusherBeams.getDeviceInterests();

      print(interests);
    } on PlatformException {
      print('Encountered PlatformException');
    }
  }*/

  Widget build(BuildContext context) {
    return MaterialApp(
      title: ReuseStrings.appName,
      theme: CustomTheme.appTheme(),
      home: const LoginPage(),
      onGenerateRoute: (RouteSettings settings) {
        return MaterialPageRoute<dynamic>(builder: (BuildContext context) {
          switch (settings.name) {
            case '/home':
              return HomePage(userAuth: settings.arguments as StudentAuth);
            case '/login':
              return const LoginPage();
            case '/signup':
              return const SignUpPage();
            case '/validation':
              return ValidationPage(user: settings.arguments as NewUser);
            case '/checkoutContainer':
              return CheckoutContainerPage(
                  userAuth: settings.arguments as StudentAuth);
            case '/returnContainer':
              return ReturnContainerPage(
                  userAuth: settings.arguments as StudentAuth);
            case '/containerList':
              return ContainerListPage(
                  userAuth: settings.arguments as StudentAuth);
            default:
              break;
          }
          return const LoginPage();
        });
      },
    );
  }
}
