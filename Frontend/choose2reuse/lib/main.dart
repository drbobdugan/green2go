import 'package:Choose2Reuse/pages/containerPass.dart';
import 'package:flutter/material.dart';
import 'package:pusher_beams/pusher_beams.dart';

import 'pages/appError.dart';
import 'pages/changePassword.dart';
import 'pages/checkoutContainer.dart';
import 'pages/containerList.dart';
import 'pages/forgotPassword.dart';
import 'pages/home.dart';
import 'pages/login.dart';
import 'pages/points.dart';
import 'pages/profile.dart';
import 'pages/returnConfirmation.dart';
import 'pages/returnContainer.dart';
import 'pages/reward.dart';
import 'pages/signup.dart';
import 'pages/validation.dart';
import 'services/api.dart';
import 'services/navigation_service.dart';
import 'services/user_service.dart';
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

  Future<APIResponse> onVersionCheck() async {
    return await UserService.versionCheck();
  }

  @override
  _Choose2ReuseAppState createState() => _Choose2ReuseAppState();
}

class _Choose2ReuseAppState extends State<Choose2ReuseApp> {
  bool isVersionLatest = true;

  @override
  void initState() {
    super.initState();
    checkVersion();
  }

  void checkVersion() {
    widget.onVersionCheck().then((APIResponse resp) {
      //isVersionLatest = resp.data['isVersionGood'] as bool;
      isVersionLatest = true;
    });
  }

  @override
  Widget build(BuildContext context) {
    if (!isVersionLatest) {
      return MaterialApp(
          title: ReuseStrings.appName,
          theme: CustomTheme.appTheme(),
          home: const AppErrorPage());
    }

    return MaterialApp(
      title: ReuseStrings.appName,
      theme: CustomTheme.appTheme(),
      home: const LoginPage(),
      onGenerateRoute: (RouteSettings settings) {
        return MaterialPageRoute<dynamic>(builder: (BuildContext context) {
          switch (settings.name) {
            case C2RPages.home:
              return HomePage(userAuth: settings.arguments as StudentAuth);
            case C2RPages.profile:
              return ProfilePage(userAuth: settings.arguments as StudentAuth);
            case C2RPages.login:
              return const LoginPage();
            case C2RPages.signup:
              return const SignUpPage();
            case C2RPages.validation:
              return ValidationPage(user: settings.arguments as NewUser);
            case C2RPages.checkoutContainer:
              return CheckoutContainerPage(
                  userAuth: settings.arguments as StudentAuth);
            case C2RPages.returnContainer:
              return ReturnContainerPage(
                  userAuth: settings.arguments as StudentAuth);
            case C2RPages.containerList:
              return ContainerListPage(
                  userAuth: settings.arguments as StudentAuth);
            case C2RPages.changePassword:
              return ChangePasswordPage(
                  userAuth: settings.arguments as StudentAuth);
            case C2RPages.forgotPassword:
              return const ForgotPasswordPage();
            case C2RPages.points:
              return PointsPage(userAuth: settings.arguments as StudentAuth);
            case C2RPages.returnConfirmation:
              final NavArguments args = settings.arguments as NavArguments;
              return ReturnConfirmationPage(
                  userAuth: args.user,
                  points: args.points,
                  earnedBadge: args.earnedBadge);
            case C2RPages.reward:
              return RewardPage(userAuth: settings.arguments as StudentAuth);
            case C2RPages.containerPass:
              return ContainerPass(userAuth: settings.arguments as StudentAuth);
            default:
              break;
          }
          return const LoginPage();
        });
      },
    );
  }
}
