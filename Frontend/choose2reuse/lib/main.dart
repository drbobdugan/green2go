import 'package:Choose2Reuse/pages/profile.dart';
import 'package:flutter/material.dart';
import 'package:flutter/services.dart';
import 'package:pusher_beams/pusher_beams.dart';
import 'package:permission_handler/permission_handler.dart';
import 'pages/changePassword.dart';
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
  WidgetsFlutterBinding.ensureInitialized();

  try {
    PusherBeams.start('7032df3e-e5a8-494e-9fc5-3b9f05a68e3c')
        .then((dynamic res) => {
              PusherBeams.addDeviceInterest('hello')
                  .then((dynamic res) => {print('done')})
            });
  } catch (e) {
    print(e);
    print('Failed to connect to Pusher Beams');
  }

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
  }

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
            case '/profile':
              return ProfilePage(userAuth: settings.arguments as StudentAuth);
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
            case '/changePassword':
              return ChangePasswordPage(
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
