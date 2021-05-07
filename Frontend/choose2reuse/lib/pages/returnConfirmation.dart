import 'package:Choose2Reuse/components/font_scale_blocker.dart';
import 'package:flutter/material.dart';

import '../components/reuse_button.dart';
import '../components/reuse_label.dart';
import '../components/reuse_userBar.dart';
import '../services/navigation_service.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';

class ReturnConfirmationPage extends StatefulWidget {
  const ReturnConfirmationPage(
      {Key key, @required this.userAuth, this.points, this.earnedBadge})
      : super(key: key);

  final StudentAuth userAuth;
  final int points;
  final bool earnedBadge;

  @override
  _ReturnConfirmationPageState createState() => _ReturnConfirmationPageState();
}

class _ReturnConfirmationPageState extends State<ReturnConfirmationPage> {
  int points;
  bool earnedBadge;

  @override
  void initState() {
    super.initState();

    points = widget.points;
    earnedBadge = widget.earnedBadge;
  }

  void onDone() {
    NavigationService(context: context).goHome(widget.userAuth);
  }

  @override
  Widget build(BuildContext context) {
    return FontScaleBlocker(
      child: Scaffold(
        backgroundColor: Colors.white,
        appBar: UserAppBar(userAuth: widget.userAuth),
        body: Padding(
          padding: const EdgeInsets.all(50.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              ReuseLabel(
                text: ReuseStrings.returnConfirmationTitle,
                textStyle: CustomTheme.primaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: points == 15
                    ? ReuseStrings.returnConfirmation15PointsText
                    : ReuseStrings.returnConfirmation5PointsText,
                textStyle: CustomTheme.primaryLabelStyle(isBold: false),
                bottom: 15.0,
              ),
              if (earnedBadge)
                ReuseLabel(
                  text: ReuseStrings.earnedBadgeText,
                  textStyle: CustomTheme.primaryLabelStyle(isBold: false),
                  bottom: 15.0,
                ),
              ReuseButton(
                text: ReuseStrings.done,
                onPressed: () => onDone(),
                buttonStyle: CustomTheme.primaryButtonStyle(),
                top: 20.0,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
