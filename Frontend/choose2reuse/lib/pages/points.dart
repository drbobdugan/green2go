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

class PointsPage extends StatefulWidget {
  const PointsPage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetUser() async {
    return await UserService.getUser(userAuth);
  }

  Future<APIResponse> onClaimReward() async {
    return await StudentService.claimReward(userAuth);
  }

  @override
  _PointsPageState createState() => _PointsPageState();
}

class _PointsPageState extends State<PointsPage> {
  DetailedUser detailedUser;
  bool hasReward;
  Map<String, dynamic> data;

  @override
  void initState() {
    super.initState();

    widget.onGetUser().then((APIResponse response) {
      if (response.success) {
        setState(() {
          detailedUser = DetailedUser(response.data);
          data = response.data as Map<String, dynamic>;
          hasReward = data['rewardCheck'] as bool;
        });
      }
    });
  }

  void claimReward() {
    widget.onClaimReward().then((APIResponse response) {
      if (response.success) {
        NavigationService(context: context)
            .goToPage(C2RPages.reward, widget.userAuth);
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
                text: ReuseStrings.pointsPageTitle,
                textStyle: CustomTheme.primaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: '${detailedUser.points} ${ReuseStrings.myPoints}',
                textStyle: CustomTheme.brightLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              ReuseLabel(
                text: ReuseStrings.badgesPageTitle,
                textStyle: CustomTheme.primaryLabelStyle(),
                bottom: 20.0,
              ),
              ReuseLabel(
                text: '${detailedUser.badges} ${ReuseStrings.myBadges}',
                textStyle: CustomTheme.brightLabelStyle(),
                top: 10.0,
                bottom: 20.0,
              ),
              if (hasReward)
                ReuseLabel(
                  text: ReuseStrings.rewardsPageTitle,
                  textStyle: CustomTheme.primaryLabelStyle(),
                  bottom: 20.0,
                ),
              if (hasReward)
                ReuseLabel(
                  text: ReuseStrings.rewardInstructions,
                  textStyle: CustomTheme.primaryLabelStyle(isBold: false),
                  bottom: 20.0,
                ),
              if (hasReward)
                ReuseButton(
                  text: ReuseStrings.claimReward,
                  onPressed: claimReward,
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
