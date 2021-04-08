import 'package:flutter/material.dart';

import '../components/reuse_listItem.dart';
import '../components/reuse_loading.dart';
import '../services/api.dart';
import '../services/student_service.dart';
import '../static/container.dart';
import '../static/student.dart';

class ReuseContainerList extends StatefulWidget {
  const ReuseContainerList(
      {Key key, @required this.userAuth, @required this.containers})
      : super(key: key);

  final StudentAuth userAuth;
  final List<ReusableContainer> containers;

  Future<APIResponse> onSubmitReport(String qrCode, String report) async {
    return await StudentService.reportContainer(userAuth, qrCode, report);
  }

  @override
  _ReuseContainerListState createState() => _ReuseContainerListState();
}

class _ReuseContainerListState extends State<ReuseContainerList> {
  void handleSubmitReport(int index, String message) {
    widget.containers[index].status = ContainerStatus.DamagedLost;
    widget.onSubmitReport(widget.containers[index].qrCode, message);
  }

  @override
  Widget build(BuildContext context) {
    if (widget.containers == null) {
      return const Scaffold(
        backgroundColor: Colors.white,
        body: ReuseLoading(),
      );
    }

    final ScrollController scrollController = ScrollController();
    return Expanded(
      child: Scrollbar(
        isAlwaysShown: true,
        controller: scrollController,
        child: ListView.builder(
          controller: scrollController,
          itemCount: widget.containers.length,
          itemBuilder: (BuildContext context, int index) {
            final ReusableContainer container = widget.containers[index];
            return Padding(
              padding: const EdgeInsets.only(top: 30.0),
              child: ListItem(
                  text1: container.dataRowText1(),
                  text2: container.dataRowText2(),
                  text3: container.dataRowText3(),
                  colorID: container.dataRowColorID(),
                  onSubmitDialog: (String message) =>
                      handleSubmitReport(index, message)),
            );
          },
        ),
      ),
    );
  }
}
