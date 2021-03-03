import 'package:flutter/material.dart';

import '../services/student_service.dart';
import '../components/user_appBar.dart';
import '../static/student.dart';

class HomePage extends StatefulWidget {
  final Student user;

  HomePage({Key key, this.user}) : super(key: key);

  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
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
                'Hello ${widget.user.firstName}!',
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
