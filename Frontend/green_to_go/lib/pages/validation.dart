import 'package:flutter/material.dart';

import '../services/userService.dart';
import '../components/cool_textField.dart';
import '../components/cool_errorMessage.dart';
import '../static/user.dart';
import 'home.dart';

class ValidationPage extends StatefulWidget {
  final dynamic user;

  ValidationPage({Key key, @required this.user}) : super(key: key);

  final _userService = UserService();
  Future<bool> onVerify(code) async {
    return await _userService.validateCode(user, code);
  }

  Future<bool> onSignUp() async {
    return await _userService.signUp(user);
  }

  Future<bool> onSendCode() async {
    return await _userService.sendCode(user);
  }

  NewUser getUser() => user;

  @override
  _ValidationPageState createState() => _ValidationPageState();
}

class _ValidationPageState extends State<ValidationPage> {
  String code = '';
  String errorMessage = '';

  bool isValidCode() {
    if (code == '') {
      setState(() {
        errorMessage = 'Please enter a valid code.';
      });
      return false;
    }
    return true;
  }

  handleVerify(BuildContext context) {
    if (isValidCode()) {
      widget.onVerify(code).then((response) {
        if (response) {
          handleSignUp(context);
        } else {
          setState(() {
            errorMessage = 'Invalid code.';
          });
        }
      });
    }
  }

  handleSignUp(BuildContext context) {
    widget.onSignUp().then((response) {
      if (response) {
        Navigator.of(context).popUntil((route) => route.isFirst);
        Navigator.of(context).pop();
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (context) => new HomePage(),
          ),
        );
      } else {
        setState(() {
          errorMessage = 'An error occured, please try again later.';
        });
      }
    });
  }

  handleNewCode(BuildContext context) {
    //var response = widget.onSendCode();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
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
              child: Text(
                "Welcome!",
                textAlign: TextAlign.center,
                style: TextStyle(fontWeight: FontWeight.bold, fontSize: 20.0),
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(bottom: 10.0),
              child: Text(
                "Thank you for signing up for the Green to Go App! We’ve sent a code to the email that you’ve provided. Please enter the code to verify your email address. The code will expire in 5 minutes.",
                style: TextStyle(fontSize: 20.0),
              ),
            ),
            CoolTextField(text: "Enter code here"),
            Padding(
              padding: const EdgeInsets.only(top: 15.0),
              child: ElevatedButton(
                child: Text('Submit'),
                onPressed: () {
                  handleVerify(context);
                },
              ),
            ),
            Padding(
              padding: const EdgeInsets.only(top: 10.0),
              child: TextButton(
                child: Text('Request a new code'),
                onPressed: () {
                  handleNewCode(context);
                },
              ),
            ),
            CoolErrorMessage(text: errorMessage),
          ],
        ),
      ),
    );
  }
}
