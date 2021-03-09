import 'package:flutter/material.dart';
import 'package:intl/intl.dart';

import '../components/custom_theme.dart';
import '../components/reuse_containerCounts.dart';
import '../components/reuse_label.dart';
import '../components/reuse_listItem.dart';
import '../components/reuse_loading.dart';
import '../components/reuse_strings.dart';
import '../components/user_appBar.dart';
import '../services/api.dart';
import '../services/student_service.dart';
import '../static/container.dart';
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
  ContainerStatus.CheckedOut: 'Checked out',
  ContainerStatus.Verified: 'Pending Return',
  ContainerStatus.Unverified: 'Verified Return',
};

class HomePage extends StatefulWidget {
  const HomePage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetContainers() async {
    return await StudentService.getContainers(userAuth);
  }

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  StudentDetails user;

  Map<ContainerStatus, int> containerCounts = <ContainerStatus, int>{
    ContainerStatus.CheckedOut: 0,
    ContainerStatus.Verified: 0,
    ContainerStatus.Unverified: 0,
  };

  @override
  void initState() {
    super.initState();

    user = StudentDetails(widget.userAuth);

    widget.onGetContainers().then((APIResponse response) {
      if (response.success) {
        setState(() {
          user.setContainers(response.data as List<dynamic>);

          for (final ContainerStatus status in items) {
            containerCounts[status] = user.containers
                .where((dynamic c) => c.status == labels[status])
                .toList()
                .length;
          }
        });
      }
    });
  }

  List<Widget> getContainerDataSmall() {
    return items.map((ContainerStatus status) {
      return Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          ContainerCounts(
              text: '${containerCounts[status]}',
              textStyle: CustomTheme.primaryLabelStyle(fontSize: 25.0),
              backgroundName: 'assets/images/c2r_reuseIcon_attention.jpg',
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
        ],
      );
    }).toList();
  }

  ListView getContainerDataLarge() {
    return ListView.builder(
      itemCount: user.containers.length,
      itemBuilder: (BuildContext context, int index) {
        final ReusableContainer container = user.containers[index];
        return Padding(
          padding: const EdgeInsets.only(top: 30.0),
          child: ListItem(
            text1: '${container.status}\n#${container.qrCode}',
            text2:
                '${formatDate(container.statusUpdateTime)}\n${container.statusLocation}',
            textStyle: CustomTheme.rightListStyle(),
          ),
        );
      },
    );
  }

  String formatDate(String date) {
    final DateTime inputDate = DateFormat('yyyy-MM-dd HH:mm:ss').parse(date);
    return DateFormat('MM/dd/yyyy hh:mm a').format(inputDate);
  }

  @override
  Widget build(BuildContext context) {
    if (user.containers == null) {
      return const Scaffold(
        backgroundColor: Colors.white,
        body: ReuseLoading(),
      );
    }

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: UserAppBar(userAuth: widget.userAuth),
      body: SizedBox(
        width: MediaQuery.of(context).size.width,
        height: MediaQuery.of(context).size.height,
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            ReuseLabel(
              text: ReuseStrings.homepageTitle(),
              textStyle: CustomTheme.primaryLabelStyle(),
              top: 20.0,
              bottom: 20.0,
            ),
            Row(
              mainAxisAlignment: MainAxisAlignment.center,
              crossAxisAlignment: CrossAxisAlignment.center,
              children: getContainerDataSmall(),
            ),
            Expanded(
              child: getContainerDataLarge(),
            )
          ],
        ),
      ),
    );
  }
}
