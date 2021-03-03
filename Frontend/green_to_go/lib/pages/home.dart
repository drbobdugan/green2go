import 'package:flutter/material.dart';

import '../services/student_service.dart';
import '../components/user_appBar.dart';
import '../static/student.dart';
import '../services/student_service.dart';
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
  StudentDetails user = new StudentDetails({});

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

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: UserAppBar(),
      body: Padding(
        padding: const EdgeInsets.all(50.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            Padding(
              padding: const EdgeInsets.only(bottom: 10.0),
              child: Text(
                'Hello ${user.firstName}!',
                textAlign: TextAlign.center,
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20.0),
              ),
            ),
          ],
        ),
      ),
    );
  }
}
