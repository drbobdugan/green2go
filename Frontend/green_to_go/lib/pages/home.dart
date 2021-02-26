import 'package:flutter/material.dart';

import '../services/student_service.dart';
import '../components/user_appBar.dart';
import '../static/student.dart';

class HomePage extends StatefulWidget {
  final String email;

  HomePage({Key key, this.email}) : super(key: key);

  final _studentService = StudentService();
  Future<Student> getStudent() async {
    return await _studentService.getStudent(email);
  }

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  Student user = new Student();

  buildStudent() {
    widget.getStudent().then((student) {
      user = student;
    });
  }

  @override
  Widget build(BuildContext context) {
    buildStudent();

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
                child: Text('Hello ${user.firstName}!',
                    textAlign: TextAlign.center,
                    style: TextStyle(
                        fontWeight: FontWeight.bold, fontSize: 20.0))),
          ],
        ),
      ),
    );
  }
}
