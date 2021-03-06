import 'package:Choose2Reuse/components/reuse_containerCounts.dart';
import 'package:flutter/material.dart';

import '../components/custom_theme.dart';
import '../components/reuse_label.dart';
import '../components/user_appBar.dart';
import '../services/api.dart';
import '../services/student_service.dart';
import '../static/student.dart';

class HomePage extends StatefulWidget {
  const HomePage({Key key, this.user}) : super(key: key);

  final StudentDetails user;

  Future<APIResponse> onGetUser() async {
    return await StudentService.getStudent(user.auth);
  }

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  StudentDetails detailedUser;

  @override
  void initState() {
    super.initState();
    // widget.onGetUser().then((APIResponse response) {
    //   if (response.success) {
    //     print(response.data);
    //     setState(() {
    //       detailedUser = StudentDetails(
    //           response.data as Map<String, dynamic>, widget.user.auth);
    //     });
    //   }
    // });
  }

  int containerCount(String filterBy) {
    if (detailedUser != null && detailedUser.containers != null) {
      return detailedUser.containers
          .where((dynamic c) => c.status == filterBy)
          .toList()
          .length;
    }
    return 0;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: UserAppBar(user: detailedUser),
      body: Padding(
        padding: const EdgeInsets.all(30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            ReuseLabel(
              text: 'My Containers',
              textStyle: CustomTheme.primaryLabelStyle(),
              bottom: 20.0,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                ContainerCounts(
                    text: '${containerCount('Checked out')}',
                    textStyle: CustomTheme.primaryLabelStyle(fontSize: 25.0),
                    backgroundName: 'assets/images/c2r_reuseIcon_attention.jpg',
                    backgroundHeight: 100.0,
                    backgroundWidth: 100.0,
                    right: 10.0,
                    left: 10.0),
                ContainerCounts(
                    text: '${containerCount('Unverified Return')}',
                    textStyle: CustomTheme.primaryLabelStyle(fontSize: 25.0),
                    backgroundName: 'assets/images/c2r_reuseIcon_primary.jpg',
                    backgroundHeight: 100.0,
                    backgroundWidth: 100.0,
                    right: 10.0,
                    left: 10.0),
                ContainerCounts(
                    text: '${containerCount('Verified Return')}',
                    textStyle: CustomTheme.primaryLabelStyle(fontSize: 25.0),
                    backgroundName:
                        'assets/images/c2r_reuseIcon_darkPrimary.jpg',
                    backgroundHeight: 100.0,
                    backgroundWidth: 100.0,
                    right: 10.0,
                    left: 10.0)
              ],
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: <Widget>[
                Flexible(
                  child: ReuseLabel(
                    text: 'Currently Checked Out Containers',
                    textStyle: CustomTheme.secondaryLabelStyle(fontSize: 15.0),
                    top: 15.0,
                    right: 0.0,
                    backgroundWidth: 100,
                  ),
                ),
                Flexible(
                  child: ReuseLabel(
                    text: 'Unverified Returned Containers',
                    textStyle: CustomTheme.secondaryLabelStyle(fontSize: 15.0),
                    top: 15.0,
                    right: 0.0,
                    backgroundWidth: 100,
                  ),
                ),
                Flexible(
                  child: ReuseLabel(
                    text: 'Verified Returned Containers',
                    textStyle: CustomTheme.secondaryLabelStyle(fontSize: 15.0),
                    top: 15.0,
                    right: 0.0,
                    backgroundWidth: 100,
                  ),
                ),
              ],
            )
          ],
        ),
      ),
    );
  }
}
