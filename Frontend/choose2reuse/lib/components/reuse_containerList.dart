import 'package:Choose2Reuse/components/font_scale_blocker.dart';
import 'package:flutter/material.dart';

import '../components/reuse_label.dart';
import '../components/reuse_listItem.dart';
import '../components/reuse_loading.dart';
import '../services/api.dart';
import '../services/student_service.dart';
import '../static/container.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';

class ReuseContainerList extends StatelessWidget {
  const ReuseContainerList(
      {Key key,
      @required this.userAuth,
      @required this.containers,
      @required this.submitReport})
      : super(key: key);

  final StudentAuth userAuth;
  final List<ReusableContainer> containers;
  final dynamic submitReport;

  @override
  Widget build(BuildContext context) {
    if (containers == null) {
      return const Scaffold(
        backgroundColor: Colors.white,
        body: ReuseLoading(),
      );
    }

    if (containers.isEmpty) {
      return ReuseLabel(
        text: ReuseStrings.noContainers,
        textStyle: CustomTheme.primaryLabelStyle(fontSize: 16.0),
        top: 10.0,
        left: 5.0,
        right: 5.0,
        backgroundWidth: 100,
      );
    }

    final ScrollController scrollController = ScrollController();
    return Expanded(
      child: Scrollbar(
        isAlwaysShown: true,
        controller: scrollController,
        child: ListView.builder(
          controller: scrollController,
          itemCount: containers.length,
          itemBuilder: (BuildContext context, int index) {
            final ReusableContainer container = containers[index];
            return Padding(
              padding: const EdgeInsets.only(top: 30.0),
              child: ListItem(
                  text1: container.dataRowText1(),
                  text2: container.dataRowText2(),
                  text3: container.dataRowText3(),
                  colorID: container.dataRowColorID(),
                  status: container.status,
                  onSubmitDialog: (String message) =>
                      submitReport(index, message)),
            );
          },
        ),
      ),
    );
  }
}
