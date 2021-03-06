import 'package:Choose2Reuse/components/reuse_containerCounts.dart';
import 'package:flutter/material.dart';

import '../components/custom_theme.dart';
import '../components/reuse_label.dart';
import '../components/user_appBar.dart';
import '../services/api.dart';
import '../services/student_service.dart';
import '../static/student.dart';

enum ContainerStatus { CheckedOut, Verified, Unverified }

const List<ContainerStatus> items = <ContainerStatus>[
  ContainerStatus.CheckedOut,
  ContainerStatus.Verified,
  ContainerStatus.Unverified,
];

const Map<ContainerStatus, String> iconColor = <ContainerStatus, String>{
  ContainerStatus.CheckedOut: 'attention',
  ContainerStatus.Verified: 'primary',
  ContainerStatus.Unverified: 'darkPrimary',
};

const Map<ContainerStatus, String> labels = <ContainerStatus, String>{
  ContainerStatus.CheckedOut: 'Checked Out',
  ContainerStatus.Verified: 'Pending Return',
  ContainerStatus.Unverified: 'Verified Return',
};

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

  // @override
  // void initState() {
  //   super.initState();
  //   widget.onGetUser().then((APIResponse response) {
  //     if (response.success) {
  //       print(response.data);
  //       setState(() {
  //         detailedUser = StudentDetails(
  //             response.data as Map<String, dynamic>, widget.user.auth);
  //       });
  //     }
  //   });
  // }

  List<Widget> getContainerDataSmall() {
    return items.map((ContainerStatus status) {
      return Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            ContainerCounts(
                text: '0',
                textStyle: CustomTheme.primaryLabelStyle(fontSize: 25.0),
                backgroundName:
                    'assets/images/c2r_reuseIcon_${iconColor[status]}.jpg',
                backgroundHeight: 100.0,
                backgroundWidth: 100.0,
                right: 12.0,
                left: 12.0),
            ReuseLabel(
              text: labels[status],
              textStyle: CustomTheme.secondaryLabelStyle(fontSize: 16.0),
              top: 15.0,
              left: 8.0,
              right: 8.0,
              backgroundWidth: 100,
            )
          ]);
    }).toList();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: UserAppBar(user: detailedUser),
      body: Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          ReuseLabel(
            text: 'My Containers',
            textStyle: CustomTheme.primaryLabelStyle(),
            top: 20.0,
            bottom: 20.0,
          ),
          Row(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.center,
            children: getContainerDataSmall(),
          ),
        ],
      ),
    );
  }
}
