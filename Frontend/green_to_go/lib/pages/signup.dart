import 'package:email_validator/email_validator.dart';
import 'package:flutter/material.dart';

import '../components/cool_textField.dart';
import '../components/cool_errorMessage.dart';
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

  bool isSignUpValid() {
    if (user.firstName == '' || user.lastName == '') {
      setState(() {
        errorMessage = 'Please enter a first and last name.';
      });
      return false;
    }
    if (user.email == '') {
      setState(() {
        errorMessage = 'Please enter an email.';
      });
      return false;
    }
    if (!EmailValidator.validate(user.email)) {
      setState(() {
        errorMessage = 'Please enter a valid email.';
      });
      return false;
    }
    if (user.password != user.confirmPassword) {
      setState(() {
        errorMessage = 'Please enter passwords that match.';
      });
      return false;
    }
    return true;
  }

  handleSignUp(BuildContext context) {
    if (isSignUpValid()) {
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
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
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
                autofillHints: [AutofillHints.givenName],
                keyboardType: TextInputType.name),
            CoolTextField(
                text: "Middle Name",
                onChanged: (value) {
                  setState(() {
                    user.middleName = value;
                  });
                },
                autofillHints: [AutofillHints.middleName],
                keyboardType: TextInputType.name),
            CoolTextField(
                text: "Last Name",
                onChanged: (value) {
                  setState(() {
                    user.lastName = value;
                  });
                },
                autofillHints: [AutofillHints.familyName],
                keyboardType: TextInputType.name),
            CoolTextField(
                text: "Phone Number",
                onChanged: (value) {
                  setState(() {
                    user.phoneNum = value;
                  });
                },
                autofillHints: [AutofillHints.telephoneNumber],
                keyboardType: TextInputType.phone),
            CoolTextField(
                text: "Email",
                onChanged: (value) {
                  setState(() {
                    user.email = value;
                  });
                },
                autofillHints: [AutofillHints.email],
                keyboardType: TextInputType.emailAddress),
            CoolTextField(
                text: "Class Year",
                onChanged: (value) {
                  setState(() {
                    user.classYear = int.parse(value);
                  });
                },
                keyboardType: TextInputType.number),
            CoolTextField(
                text: "Password",
                onChanged: (value) {
                  setState(() {
                    user.password = value;
                  });
                },
                autofillHints: [AutofillHints.password],
                keyboardType: TextInputType.visiblePassword),
            CoolTextField(
                text: "Confirm Password",
                onChanged: (value) {
                  setState(() {
                    user.confirmPassword = value;
                  });
                },
                autofillHints: [AutofillHints.password],
                keyboardType: TextInputType.visiblePassword),
            Padding(
                padding: const EdgeInsets.only(top: 20.0),
                child: ElevatedButton(
                  child: Text('Sign Up'),
                  onPressed: () {
                    handleSignUp(context);
                  },
                )),
            CoolErrorMessage(text: errorMessage),
          ],
        ),
      ),
    );
  }
}
