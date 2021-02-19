import 'package:flutter/material.dart';

import '../components/cool_textField.dart';
import '../services/userService.dart';
import 'home.dart';

class ValidationPage extends StatefulWidget {
  final dynamic data;

  ValidationPage({Key key, @required this.data}) : super(key: key);

  final _userService = UserService();
  bool onVerify() {
    print(data);
    return _userService
        .signUp({'email': data.email, 'password': data.password});
  }

  @override
  _ValidationPageState createState() => _ValidationPageState();
}

class _ValidationPageState extends State<ValidationPage> {
  handleVerify(BuildContext context) {
    var response = widget.onVerify();
    if (response) {
      Navigator.of(context).pushReplacement(
          MaterialPageRoute(builder: (context) => new HomePage()));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text('Green2Go'),
        ),
        body: Padding(
            padding: const EdgeInsets.all(50.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                Padding(
                    padding: const EdgeInsets.only(bottom: 20.0),
                    child: Text("Welcome!",
                        textAlign: TextAlign.center,
                        style: TextStyle(
                            fontWeight: FontWeight.bold, fontSize: 20.0))),
                Padding(
                    padding: const EdgeInsets.only(bottom: 10.0),
                    child: Text(
                        "Thank you for signing up for the Green to Go App! We’ve sent a code to the email that you’ve provided. Please enter the code to verify your email address. The code will expire in 5 minutes.",
                        style: TextStyle(fontSize: 18.0))),
                TextFormField(
                    decoration: InputDecoration(labelText: 'Enter code here')),
                Padding(
                    padding: const EdgeInsets.only(top: 20.0),
                    child: ElevatedButton(
                      child: Text('Submit'),
                      onPressed: handleVerify(context),
                    )),
                Padding(
                    padding: const EdgeInsets.only(top: 10.0),
                    child: TextButton(
                      child: Text('Request a new code'),
                      onPressed: () {},
                    ))
              ],
            )));
  }
}
