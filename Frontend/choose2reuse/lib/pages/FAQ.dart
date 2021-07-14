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

class FAQPage extends StatefulWidget {
  const FAQPage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetUser() async {
    return await UserService.getUser(userAuth);
  }

  @override
  _FAQPageState createState() => _FAQPageState();
}

class _FAQPageState extends State<FAQPage> {
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
                text: ReuseStrings.faqPageTitle,
                textStyle: CustomTheme.primaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqSectionContainers,
                textStyle: CustomTheme.brightLabelStyle(fontSize: 18),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqQuestion3,
                textStyle: CustomTheme.secondaryDarkLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqAnswer3,
                textStyle: CustomTheme.secondaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqQuestion4,
                textStyle: CustomTheme.secondaryDarkLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqAnswer4,
                textStyle: CustomTheme.secondaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqQuestion8,
                textStyle: CustomTheme.secondaryDarkLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqAnswer8,
                textStyle: CustomTheme.secondaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqQuestion5,
                textStyle: CustomTheme.secondaryDarkLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqAnswer5,
                textStyle: CustomTheme.secondaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqQuestion6,
                textStyle: CustomTheme.secondaryDarkLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqAnswer6,
                textStyle: CustomTheme.secondaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqQuestion7,
                textStyle: CustomTheme.secondaryDarkLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqAnswer7,
                textStyle: CustomTheme.secondaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqSectionPoints,
                textStyle: CustomTheme.brightLabelStyle(fontSize: 18),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqQuestion1,
                textStyle: CustomTheme.secondaryDarkLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqAnswer1,
                textStyle: CustomTheme.secondaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqQuestion2,
                textStyle: CustomTheme.secondaryDarkLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.faqAnswer2,
                textStyle: CustomTheme.secondaryLabelStyle(),
                bottom: 20.0,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
