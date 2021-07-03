import 'package:flutter/material.dart';

import '../components/font_scale_blocker.dart';
import '../components/reuse_label.dart';
import '../components/reuse_loading.dart';
import '../components/reuse_userBar.dart';
import '../services/api.dart';
import '../services/student_service.dart';
import '../static/container.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';

class ContainerPass extends StatefulWidget {
  const ContainerPass({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetSortedContainers() async {
    return await StudentService.getSortedContainers(userAuth);
  }

  @override
  _ContainerPassState createState() => _ContainerPassState();
}

class _ContainerPassState extends State<ContainerPass> {
  StudentDetails user;
  bool freeContainer;
  String timestamp = '', displayText = ReuseStrings.noContainers;

  @override
  void initState() {
    super.initState();

    user = StudentDetails(widget.userAuth);

    widget.onGetSortedContainers().then((APIResponse response) {
      if (response.success) {
        setState(() {
          user.sortedContainers =
              SortedReusableContainers(response.data as Map<String, dynamic>);
          user.sortedContainers.checkedOut.length <= 2
              ? freeContainer = true
              : freeContainer = false;
          if (user.sortedContainers.checkedOut.isNotEmpty) {
            timestamp = user.sortedContainers.checkedOut.first.dataRowText2();
            freeContainer
                ? displayText = ReuseStrings.freeContainer
                : displayText = ReuseStrings.paidContainer;
          }
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (freeContainer == null) {
      return const Scaffold(
        backgroundColor: Colors.white,
        body: ReuseLoading(),
      );
    }

    return FontScaleBlocker(
      child: Scaffold(
        backgroundColor: Colors.white,
        appBar: UserAppBar(userAuth: widget.userAuth),
        body: SizedBox(
          width: MediaQuery.of(context).size.width,
          height: MediaQuery.of(context).size.height,
          child: Column(
            children: <Widget>[
              ReuseLabel(
                text: ReuseStrings.containerPassPageTitle,
                textStyle: CustomTheme.primaryLabelStyle(),
                top: 30,
              ),
              const Image(
                image: AssetImage('assets/images/containerPassGif.gif'),
              ),
              Container(
                width: MediaQuery.of(context).size.width * .8,
                height: MediaQuery.of(context).size.height * .5,
                color: freeContainer
                    ? CustomTheme.getColor('primary')
                    : Colors.red,
                child: Column(
                  mainAxisAlignment: MainAxisAlignment.center,
                  children: <Widget>[
                    ReuseLabel(
                      text: displayText,
                      textStyle: CustomTheme.primaryLabelStyle(fontSize: 23),
                      left: 10,
                      right: 10,
                      bottom: 15,
                    ),
                    ReuseLabel(
                      text: timestamp,
                      textStyle: CustomTheme.primaryLabelStyle(fontSize: 25),
                      left: 10,
                      right: 10,
                    )
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
