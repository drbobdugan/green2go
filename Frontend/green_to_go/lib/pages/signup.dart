import 'package:flutter/material.dart';

import '../components/reuse_button.dart';
import '../components/custom_theme.dart';
import '../components/reuse_textField.dart';
import '../components/reuse_errorMessage.dart';
import '../static/user.dart';
import '../services/api.dart';
import '../services/user_service.dart';
import 'validation.dart';

class SignUpPage extends StatefulWidget {
  SignUpPage({Key key}) : super(key: key);

  final _userService = UserService();
  Future<APIResponse> onSignUp(user) async {
    return await _userService.signUp(user);
  }

  @override
  _SignUpPageState createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  NewUser user = new NewUser();
  String errorMessage = '';

  void handleSignUp(BuildContext context) {
    widget.onSignUp(user).then((response) {
      if (response.success) {
        Navigator.of(context).push(MaterialPageRoute(
            builder: (context) => new ValidationPage(user: user)));
      } else {
        setState(() {
          errorMessage = response.message;
        });
      }
    });
  }

  void handleValidation(BuildContext context) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => new ValidationPage(user: user)));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      resizeToAvoidBottomPadding: false,
      resizeToAvoidBottomInset: true,
      appBar: AppBar(
        title: Text('Choose2Reuse'),
      ),
      body: GestureDetector(
          onTap: () {
            FocusScopeNode currentFocus = FocusScope.of(context);

            if (!currentFocus.hasPrimaryFocus) {
              currentFocus.unfocus();
            }
          },
          child: SingleChildScrollView(
            padding: const EdgeInsets.all(50.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                ReuseTextField(
                    text: "First Name",
                    onChanged: (value) {
                      setState(() {
                        user.firstName = value;
                      });
                    },
                    autofillHints: [AutofillHints.givenName],
                    keyboardType: TextInputType.name),
                ReuseTextField(
                    text: "Middle Name",
                    onChanged: (value) {
                      setState(() {
                        user.middleName = value;
                      });
                    },
                    autofillHints: [AutofillHints.middleName],
                    keyboardType: TextInputType.name),
                ReuseTextField(
                    text: "Last Name",
                    onChanged: (value) {
                      setState(() {
                        user.lastName = value;
                      });
                    },
                    autofillHints: [AutofillHints.familyName],
                    keyboardType: TextInputType.name),
                ReuseTextField(
                    text: "Phone Number",
                    onChanged: (value) {
                      setState(() {
                        user.phoneNum = value;
                      });
                    },
                    autofillHints: [AutofillHints.telephoneNumber],
                    keyboardType: TextInputType.phone),
                ReuseTextField(
                    text: "Email",
                    onChanged: (value) {
                      setState(() {
                        user.email = value;
                      });
                    },
                    autofillHints: [AutofillHints.email],
                    keyboardType: TextInputType.emailAddress),
                ReuseTextField(
                    text: "Class Year",
                    onChanged: (value) {
                      setState(() {
                        user.classYear = value;
                      });
                    },
                    keyboardType: TextInputType.number),
                ReuseTextField(
                    text: "Password",
                    obscureText: true,
                    onChanged: (value) {
                      setState(() {
                        user.password = value;
                      });
                    },
                    autofillHints: [AutofillHints.password],
                    keyboardType: TextInputType.visiblePassword),
                ReuseTextField(
                    text: "Confirm Password",
                    obscureText: true,
                    onChanged: (value) {
                      setState(() {
                        user.confirmPassword = value;
                      });
                    },
                    autofillHints: [AutofillHints.password],
                    keyboardType: TextInputType.visiblePassword),
                ReuseButton(
                  text: "Sign Up",
                  onPressed: () => handleSignUp(context),
                  buttonStyle: CustomTheme.primaryButtonStyle(),
                  top: 20.0,
                ),
                ReuseButton(
                  text: "Have a verification code? Enter it here!",
                  onPressed: () => handleValidation(context),
                  buttonType: "text",
                ),
                ReuseErrorMessage(text: errorMessage),
              ],
            ),
          )),
    );
  }
}
