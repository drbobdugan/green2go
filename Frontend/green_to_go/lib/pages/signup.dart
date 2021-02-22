import 'package:flutter/material.dart';

import '../components/cool_textField.dart';
import 'validation.dart';

class SignUpPage extends StatelessWidget {
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
            ),
            CoolTextField(
              text: "Middle Name",
            ),
            CoolTextField(
              text: "Last Name",
            ),
            CoolTextField(
              text: "Graduation Year",
            ),
            CoolTextField(
              text: "School Email",
            ),
            CoolTextField(
              text: "Phone Number",
            ),
            CoolTextField(
              text: "Password",
            ),
            CoolTextField(
              text: "Confirm Password",
            ),
            Padding(
              padding: const EdgeInsets.only(top: 20.0),
              child: ElevatedButton(
                child: Text('Sign Up'),
                onPressed: () {
                  Navigator.of(context).push(MaterialPageRoute(
                      builder: (context) => new ValidationPage()));
                },
              ),
            ),
          ],
        ),
      ),
    );
  }
}
