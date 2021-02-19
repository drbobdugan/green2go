import 'package:flutter/material.dart';

import '../components/cool_textField.dart';
import '../services/userService.dart';
import 'validation.dart';

class SignUpPage extends StatefulWidget {
  SignUpPage({Key key}) : super(key: key);

  final _userService = UserService();
  void onSignUp(dynamic state) {
    _userService.signIn({'email': state.email, 'password': state.password});
  }

  @override
  _SignUpPageState createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  dynamic state = {};

  handleSignUp(BuildContext context) {
    if (state.password == state.passwordConfirm) {
      Navigator.of(context).pushReplacement(MaterialPageRoute(
          builder: (context) => new ValidationPage(data: state)));
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
              padding: const EdgeInsets.only(bottom: 10.0),
              child: Text(
                "Sign Up",
                style: TextStyle(
                  fontWeight: FontWeight.bold,
                  fontSize: 20.0,
                ),
              ),
            ),
            CoolTextField(
              text: "First Name",
              onChanged: (value) {
                setState(() {
                  state.firstName = value;
                });
              },
            ),
            Padding(
                padding: const EdgeInsets.only(top: 20.0),
                child: ElevatedButton(
                  child: Text('Sign Up'),
                  onPressed: handleSignUp(context),
                )),
          ],
        ),
      ),
    );
  }
}
