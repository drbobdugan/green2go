import 'package:Choose2Reuse/components/reuse_containerCounts.dart';
import 'package:flutter/material.dart';
import '../components/custom_theme.dart';
import '../components/reuse_label.dart';
import '../services/student_service.dart';
import '../components/user_appBar.dart';
import '../static/student.dart';
import '../services/api.dart';

class HomePage extends StatefulWidget {
  final StudentAuth userAuth;

  HomePage({Key key, this.userAuth}) : super(key: key);

  final _studentService = StudentService();
  Future<APIResponse> onGetUser() async {
    return await _studentService.getStudent(userAuth);
  }

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  StudentDetails user = new StudentDetails();

  @override
  void initState() {
    widget.onGetUser().then((response) {
      if (response.success) {
        setState(() {
          user = StudentDetails(response.data);
          user.authToken = widget.userAuth.authToken;
          user.refreshToken = widget.userAuth.refreshToken;
          user.tokenExpiration = widget.userAuth.tokenExpiration;
        });
      }
    });
    super.initState();
  }

  int containerCount(String filterBy) {
    if (user.containers != null) {
      return user.containers.where((c) => c.status == filterBy).toList().length;
    }
    return 0;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: UserAppBar(auth: widget.userAuth),
      body: Padding(
        padding: const EdgeInsets.all(30.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: [
            ReuseLabel(
              text: "My Containers",
              textStyle: CustomTheme.primaryLabelStyle(),
              bottom: 20.0,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: [
                ContainerCounts(
                    text: "${containerCount("Checked out")}",
                    textStyle: CustomTheme.primaryLabelStyle(fontSize: 25.0),
                    backgroundName: 'assets/images/c2r_reuseIcon_attention.jpg',
                    backgroundHeight: 100.0,
                    backgroundWidth: 100.0,
                    right: 10.0,
                    left: 10.0),
                ContainerCounts(
                    text: "${containerCount("Unverified Return")}",
                    textStyle: CustomTheme.primaryLabelStyle(fontSize: 25.0),
                    backgroundName: 'assets/images/c2r_reuseIcon_primary.jpg',
                    backgroundHeight: 100.0,
                    backgroundWidth: 100.0,
                    right: 10.0,
                    left: 10.0),
                ContainerCounts(
                    text: "${containerCount("Verified Return")}",
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
              children: [
                Flexible(
                  child: ReuseLabel(
                    text: "Currently Checked Out Containers",
                    textStyle: CustomTheme.secondaryLabelStyle(fontSize: 15.0),
                    top: 15.0,
                    right: 0.0,
                    backgroundWidth: 100,
                  ),
                ),
                Flexible(
                  child: ReuseLabel(
                    text: "Unverified Returned Containers",
                    textStyle: CustomTheme.secondaryLabelStyle(fontSize: 15.0),
                    top: 15.0,
                    right: 0.0,
                    backgroundWidth: 100,
                  ),
                ),
                Flexible(
                  child: ReuseLabel(
                    text: "Verified Returned Containers",
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
