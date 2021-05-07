import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import 'package:countdown_flutter/countdown_flutter.dart';

import '../components/font_scale_blocker.dart';
import '../components/reuse_button.dart';
import '../components/reuse_label.dart';
import '../components/reuse_loading.dart';
import '../components/reuse_userBar.dart';
import '../services/api.dart';
import '../services/navigation_service.dart';
import '../services/user_service.dart';
import '../static/container.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';
import '../static/user.dart';

class RewardPage extends StatefulWidget {
  const RewardPage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetUser() async {
    return await UserService.getUser(userAuth);
  }

  @override
  _RewardPageState createState() => _RewardPageState();
}

class _RewardPageState extends State<RewardPage> {
  String timeStamp = DateFormat('MM/dd/yyyy hh:mm a').format(DateTime.now());

  @override
  Widget build(BuildContext context) {
    return FontScaleBlocker(
      child: Scaffold(
        backgroundColor: Colors.white,
        resizeToAvoidBottomInset: true,
        appBar: UserAppBar(userAuth: widget.userAuth),
        body: SingleChildScrollView(
          padding: const EdgeInsets.only(top: 30.0, left: 50.0, right: 50.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.symmetric(
                    vertical: 30.0, horizontal: 10.0),
                child: FittedBox(
                  fit: BoxFit.fitHeight,
                  alignment: Alignment.center,
                  child: ConstrainedBox(
                    constraints:
                        const BoxConstraints(minWidth: 1, minHeight: 1),
                    child: Image.asset(
                      'assets/images/cookie.gif',
                    ),
                  ),
                ),
              ),
              ReuseLabel(
                text: ReuseStrings.redeemedAt,
                textStyle: CustomTheme.primaryLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              ReuseLabel(
                text: timeStamp,
                textStyle: CustomTheme.brightLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              CountdownFormatted(
                duration: const Duration(seconds: 300),
                onFinish: () {
                  NavigationService(context: context).goHome(widget.userAuth);
                },
                builder: (BuildContext context, String remaining) {
                  return ReuseLabel(
                    text: remaining,
                    textStyle: CustomTheme.primaryLabelStyle(fontSize: 35),
                    top: 25,
                    bottom: 15,
                  );
                },
              ),
            ],
          ),
        ),
      ),
    );
  }
}
