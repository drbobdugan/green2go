import 'package:flutter/material.dart';

import '../components/cool_textField.dart';
import '../static/user.dart';
import 'validation.dart';

class SignUpPage extends StatefulWidget {
  SignUpPage({Key key}) : super(key: key);

  @override
  _SignUpPageState createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  NewUser user = new NewUser();

  handleSignUp(BuildContext context) {
    user.consoleLog();
    if (user.firstName != '' &&
        user.lastName != '' &&
        user.email != '' &&
        user.password == user.confirmPassword) {
      Navigator.of(context).push(MaterialPageRoute(
          builder: (context) => new ValidationPage(user: user)));
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      resizeToAvoidBottomPadding: false,
      appBar: AppBar(
        title: Text('Green2Go'),
      ),
      body: SingleChildScrollView(
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
                  user.firstName = value;
                });
              },
            ),
            CoolTextField(
              text: "Middle Name",
              onChanged: (value) {
                setState(() {
                  user.middleName = value;
                });
              },
            ),
            CoolTextField(
              text: "Last Name",
              onChanged: (value) {
                setState(() {
                  user.lastName = value;
                });
              },
            ),
            CoolTextField(
              text: "Phone Number",
              onChanged: (value) {
                setState(() {
                  user.phoneNum = value;
                });
              },
            ),
            CoolTextField(
              text: "Email",
              onChanged: (value) {
                setState(() {
                  user.email = value;
                });
              },
            ),
            CoolTextField(
              text: "Class Year",
              onChanged: (value) {
                setState(() {
                  user.classYear = int.parse(value);
                });
              },
            ),
            CoolTextField(
              text: "Password",
              onChanged: (value) {
                setState(() {
                  user.password = value;
                });
              },
            ),
            CoolTextField(
              text: "Confirm Password",
              onChanged: (value) {
                setState(() {
                  user.confirmPassword = value;
                });
              },
            ),
            Padding(
                padding: const EdgeInsets.only(top: 20.0),
                child: ElevatedButton(
                  child: Text('Sign Up'),
                  onPressed: () {
                    handleSignUp(context);
                  },
                )),
          ],
        ),
      ),
    );
  }
}
