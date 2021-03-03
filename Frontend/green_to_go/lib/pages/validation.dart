import 'package:flutter/material.dart';

import '../services/api.dart';
import '../services/user_service.dart';
import '../components/cool_button.dart';
import '../components/custom_theme.dart';
import '../components/cool_label.dart';
import '../components/cool_textField.dart';
import '../components/cool_errorMessage.dart';
import '../static/user.dart';
import 'home.dart';

class ValidationPage extends StatefulWidget {
  final dynamic user;

  ValidationPage({Key key, @required this.user}) : super(key: key);

  final _userService = UserService();
  Future<APIResponse> onVerify(email, code) async {
    return await _userService.validateCode(email, code);
  }

  Future<bool> onSendCode() async {
    return await _userService.sendCode(user);
  }

  NewUser getUser() => user;

  @override
  _ValidationPageState createState() => _ValidationPageState();
}

class _ValidationPageState extends State<ValidationPage> {
  String email = '';
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

  void handleVerify(BuildContext context) {
    if (isValidCode()) {
      widget.onVerify(email, code).then((response) {
        if (response.success) {
          Navigator.of(context).popUntil((route) => route.isFirst);
          Navigator.of(context).pop();
          Navigator.of(context).push(
            MaterialPageRoute(
              builder: (context) => new HomePage(),
            ),
          );
        } else {
          setState(() {
            errorMessage = response.message;
          });
        }
      });
    }
  }

  void handleNewCode(BuildContext context) {
    Navigator.of(context).pop();
  }

  @override
  Widget build(BuildContext context) {
    email = widget.user.email;

    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text('Choose2Reuse'),
      ),
      body: Padding(
        padding: const EdgeInsets.all(50.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            CoolLabel(
              text: "Welcome!",
              textStyle: CustomTheme.primaryLabelStyle(),
              bottom: 15.0,
            ),
            CoolLabel(
              text:
                  "Thank you for signing up for the Green to Go App! We’ve sent a code to the email that you’ve provided. Please enter the code to verify your email address. The code will expire in 5 minutes.",
              textStyle: CustomTheme.primaryLabelStyle(isBold: false),
              bottom: 15.0,
            ),
            CoolTextField(
                visible: widget.user.email == '',
                text: "Email",
                onChanged: (value) {
                  setState(() {
                    email = value;
                  });
                },
                autofillHints: [AutofillHints.email],
                keyboardType: TextInputType.emailAddress),
            CoolTextField(
                text: "Enter code here",
                onChanged: (value) {
                  setState(() {
                    code = value;
                  });
                }),
            CoolButton(
              text: "Submit",
              onPressed: () => handleVerify(context),
              buttonStyle: CustomTheme.primaryButtonStyle(),
              top: 15.0,
            ),
            CoolButton(
              text: "Request a new code",
              onPressed: () => handleNewCode(context),
              buttonType: "text",
            ),
            CoolErrorMessage(text: errorMessage),
          ],
        ),
      ),
    );
  }
}
