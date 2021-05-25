import 'package:flutter/material.dart';

import '../components/font_scale_blocker.dart';
import '../components/reuse_button.dart';
import '../components/reuse_label.dart';
import '../components/reuse_loading.dart';
import '../components/reuse_userBar.dart';
import '../services/api.dart';
import '../services/navigation_service.dart';
import '../services/student_service.dart';
import '../services/user_service.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';
import '../static/user.dart';

class ContactUsPage extends StatefulWidget {
  const ContactUsPage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetUser() async {
    return await UserService.getUser(userAuth);
  }

  @override
  _ContactUsPageState createState() => _ContactUsPageState();
}

class _ContactUsPageState extends State<ContactUsPage> {
  DetailedUser detailedUser;

  @override
  void initState() {
    super.initState();

    widget.onGetUser().then((APIResponse response) {
      if (response.success) {
        setState(() {
          detailedUser = DetailedUser(response.data);
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (detailedUser == null) {
      return const Scaffold(
        backgroundColor: Colors.white,
        body: ReuseLoading(),
      );
    }

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
              ReuseLabel(
                text: ReuseStrings.contactUsPageTitle,
                textStyle: CustomTheme.primaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.contactUsMessage,
                textStyle: CustomTheme.brightLabelStyle(fontSize: 18),
                bottom: 20.0,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
