import 'package:flutter/material.dart';

import '../components/cool_textField.dart';
import '../components/cool_errorMessage.dart';
import '../services/api.dart';
import '../services/user_service.dart';
import '../services/student_service.dart';
import '../static/user.dart';
import '../static/student.dart';
import 'signup.dart';
import 'home.dart';

class LoginPage extends StatefulWidget {
  LoginPage({Key key}) : super(key: key);

  final _userService = UserService();
  final _studentService = StudentService();
  Future<APIResponse> onLogIn(user) async {
    return await _userService.logIn(user);
  }

  Future<Student> onGetUser(user) async {
    return await _studentService.getStudent(user.email);
  }

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  ExistingUser user = new ExistingUser();
  String errorMessage = '';

  void handleLogIn(BuildContext context) {
    widget.onLogIn(user).then((response) {
      if (response.success) {
        handleNavigateHome(context);
      } else {
        setState(() {
          errorMessage = response.message;
        });
      }
    });
  }

  void handleNavigateHome(BuildContext context) {
    widget.onGetUser(user).then((response) {
      if (response != null) {
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (context) => new HomePage(user: response),
          ),
        );
      }
    });
  }

  void handleSignUp(BuildContext context) {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => new SignUpPage()));
  }

  @override
  Widget build(BuildContext context) {
    final node = FocusScope.of(context);
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: Text('Choose2Reuse'),
      ),
      body: Form(
        child: SingleChildScrollView(
          child: Column(
            children: [
              Padding(
                  padding: EdgeInsets.only(top: 50.0, bottom: 30.0),
                  child: FittedBox(
              fit: BoxFit.fitWidth,
              alignment: Alignment.bottomCenter,
              child: ConstrainedBox(
                constraints: BoxConstraints(minWidth: 1, minHeight: 1), // here
                child: Image.asset(
                  'assets/images/choose2reuse_logo.jpg',
                ),
              ),
            ),),
              Padding(
                padding: EdgeInsets.only(left: 50.0, right: 50.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: <Widget>[
                    CoolTextField(
                        text: "Email",
                        onChanged: (value) {
                          setState(() {
                            user.email = value;
                          });
                        },
                        autofillHints: [AutofillHints.email],
                        keyboardType: TextInputType.emailAddress,
                        onFieldSubmitted: (value) {
                          node.nextFocus();
                        }),
                    CoolTextField(
                        text: "Password",
                        obscureText: true,
                        onChanged: (value) {
                          setState(() {
                            user.password = value;
                          });
                        },
                        autofillHints: [AutofillHints.password],
                        onFieldSubmitted: (value) {
                          node.nextFocus();
                        }),
                    Padding(
                      padding: const EdgeInsets.only(top: 15.0),
                      child: ElevatedButton(
                        child: Text('Log In'),
                        onPressed: () {
                          handleLogIn(context);
                        },
                      ),
                    ),
                    Padding(
                      padding: const EdgeInsets.only(top: 0.0),
                      child: TextButton(
                        child: Text('Need an account? Sign up here!'),
                        onPressed: () {
                          handleSignUp(context);
                        },
                      ),
                    ),
                    CoolErrorMessage(text: errorMessage),
                  ],
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }
}
