import 'package:flutter/material.dart';

import '../components/reuse_button.dart';
import '../components/reuse_containerCounts.dart';
import '../components/reuse_label.dart';
import '../components/reuse_loading.dart';
import '../components/reuse_userBar.dart';
import '../services/api.dart';
import '../services/navigation_service.dart';
import '../services/student_service.dart';
import '../static/container.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';

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

          for (final ContainerStatus status in containerItems) {
            containerCounts[status] = user.containers
                .where((dynamic c) => c.status == containerLabels[status])
                .toList()
                .length;
          }
        });
      }
    });
  }

  List<Widget> getContainerDataSmall() {
    return containerItems.map((ContainerStatus status) {
      return Column(
        mainAxisAlignment: MainAxisAlignment.start,
        crossAxisAlignment: CrossAxisAlignment.center,
        children: <Widget>[
          ContainerCounts(
              text: '${containerCounts[status]}',
              textStyle: CustomTheme.primaryLabelStyle(fontSize: 25.0),
              backgroundName:
                  'assets/images/c2r_reuseIcon_${containerIconColors[status]}.jpg',
              backgroundHeight: 75.0,
              backgroundWidth: 90.0,
              right: 15.0,
              left: 15.0),
          ReuseLabel(
            text: containerLabels[status],
            textStyle: CustomTheme.secondaryLabelStyle(fontSize: 16.0),
            top: 10.0,
            left: 5.0,
            right: 5.0,
            backgroundWidth: 100,
          )
        ],
      );
    }).toList();
  }

  Expanded getContainerDataLarge() {
    return Expanded(
      child: ListView.builder(
        itemCount: user.containers.length > 5 ? 5 : user.containers.length,
        itemBuilder: (BuildContext context, int index) {
          final ReusableContainer container = user.containers[index];
          return Padding(
            padding: const EdgeInsets.only(top: 30.0),
            child: container.dataRow(),
          );
        },
      ),
    );
  }

  void handleViewAll(BuildContext context) {
    NavigationService(context: context)
        .goToPage(C2RPages.containerList, widget.userAuth);
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
          mainAxisAlignment: MainAxisAlignment.spaceAround,
          crossAxisAlignment: CrossAxisAlignment.center,
          children: <Widget>[
            ReuseLabel(
              text: ReuseStrings.homepageTitle,
              textStyle: CustomTheme.primaryLabelStyle(),
              top: 30.0,
              bottom: 30.0,
            ),
            Padding(
              padding: const EdgeInsets.only(bottom: 15.0),
              child: Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                crossAxisAlignment: CrossAxisAlignment.center,
                children: getContainerDataSmall(),
              ),
            ),
            Expanded(
              child: Column(
                  mainAxisAlignment: MainAxisAlignment.spaceAround,
                  children: <Widget>[
                    getContainerDataLarge(),
                    ReuseButton(
                      text: ReuseStrings.viewAllButtonText,
                      onPressed: () => handleViewAll(context),
                      buttonStyle: CustomTheme.primaryButtonStyle(),
                      bottom: MediaQuery.of(context).size.height * 0.06,
                    )
                  ]),
            ),
          ],
        ),
      ),
    );
  }
}
