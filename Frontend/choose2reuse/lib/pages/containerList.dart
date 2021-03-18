import 'package:flutter/material.dart';

import '../components/reuse_loading.dart';
import '../components/reuse_userBar.dart';
import '../services/api.dart';
import '../services/student_service.dart';
import '../static/container.dart';
import '../static/student.dart';

class ContainerListPage extends StatefulWidget {
  const ContainerListPage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetContainers() async {
    return await StudentService.getContainers(userAuth);
  }

  @override
  _ContainerListPageState createState() => _ContainerListPageState();
}

class _ContainerListPageState extends State<ContainerListPage> {
  StudentDetails user;

  @override
  void initState() {
    super.initState();

    user = StudentDetails(widget.userAuth);

    widget.onGetContainers().then((APIResponse response) {
      if (response.success) {
        setState(() {
          user.setContainers(response.data as List<dynamic>);
        });
      }
    });
  }

  ListView getContainerDataLarge() {
    return ListView.builder(
      itemCount: user.containers.length,
      itemBuilder: (BuildContext context, int index) {
        final ReusableContainer container = user.containers[index];
        return Padding(
          padding: const EdgeInsets.only(top: 30.0),
          child: container.dataRow(),
        );
      },
    );
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
            Expanded(
              child: getContainerDataLarge(),
            )
          ],
        ),
      ),
    );
  }
}
