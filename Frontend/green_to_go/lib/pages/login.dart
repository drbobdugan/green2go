import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../components/custom_theme.dart';
import '../components/reuse_button.dart';
import '../components/reuse_textField.dart';
import '../components/reuse_errorMessage.dart';
import '../components/reuse_label.dart';
import '../services/api.dart';
import '../services/user_service.dart';
import '../static/user.dart';
import '../static/student.dart';
import 'signup.dart';
import 'home.dart';

class LoginPage extends StatefulWidget {
  LoginPage({Key key}) : super(key: key);

  final _userService = UserService();
  Future<APIResponse> onLogIn(user) async {
    return await _userService.logIn(user);
  }

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final FocusNode emailNode = FocusNode();
  final FocusNode passwordNode = FocusNode();

  ExistingUser user = new ExistingUser();
  bool isLoggedIn = false;
  bool rememberMe = false;
  String errorMessage = '';

  @override
  void initState() {
    super.initState();
    autoLogIn();
  }

  void autoLogIn() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String email = prefs.getString('email');
    final String password = prefs.getString('password');

    if (email != null && password != null) {
      setState(() {
        isLoggedIn = true;
        user.email = email;
        user.password = password;
      });
    }
  }

  Future<Null> handleLogIn(BuildContext context) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    widget.onLogIn(user).then((response) {
      if (response.success) {
        if (rememberMe) {
          prefs.setString('email', user.email);
          prefs.setString('password', user.password);
        }
        Navigator.of(context).popUntil((route) => route.isFirst);
        Navigator.of(context).pop();
        Navigator.of(context).push(
          MaterialPageRoute(
            builder: (context) =>
                new HomePage(userAuth: StudentAuth(response.data)),
          ),
        );
      } else {
        setState(() {
          errorMessage = response.message;
        });
      }
    });
  }

  fieldNextFocus(
      BuildContext context, FocusNode currentFocus, FocusNode nextFocus) {
    currentFocus.unfocus();
    if (nextFocus != null) FocusScope.of(context).requestFocus(nextFocus);
  }

  void handleSignUp(BuildContext context) {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => new SignUpPage()));
  }

  @override
  Widget build(BuildContext context) {
    if (isLoggedIn) handleLogIn(context);

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
                padding: EdgeInsets.symmetric(vertical: 30.0, horizontal: 10.0),
                child: FittedBox(
                  fit: BoxFit.fitWidth,
                  alignment: Alignment.bottomCenter,
                  child: ConstrainedBox(
                    constraints:
                        BoxConstraints(minWidth: 1, minHeight: 1), // here
                    child: Image.asset(
                      'assets/images/choose2reuse_logo.jpg',
                    ),
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsets.only(left: 50.0, right: 50.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: <Widget>[
                    ReuseTextField(
                        text: "Email",
                        node: emailNode,
                        onChanged: (value) {
                          setState(() {
                            user.email = value;
                          });
                        },
                        autofillHints: [AutofillHints.email],
                        keyboardType: TextInputType.emailAddress,
                        textInputAction: TextInputAction.next,
                        onFieldSubmitted: (value) {
                          fieldNextFocus(context, emailNode, passwordNode);
                        }),
                    ReuseTextField(
                        text: "Password",
                        obscureText: true,
                        onChanged: (value) {
                          setState(() {
                            user.password = value;
                          });
                        },
                        autofillHints: [AutofillHints.password],
                        textInputAction: TextInputAction.done,
                        onFieldSubmitted: (value) {
                          fieldNextFocus(context, passwordNode, null);
                        }),
                    ReuseButton(
                      text: "Log In",
                      onPressed: () => handleLogIn(context),
                      buttonStyle: CustomTheme.primaryButtonStyle(),
                      top: 10.0,
                    ),
                    Align(
                        alignment: Alignment.bottomRight,
                        child: Container(
                            width: 155.0,
                            height: 40.0,
                            child: Row(children: <Widget>[
                              ReuseLabel(
                                text: "Remember me",
                                textStyle: CustomTheme.secondaryLabelStyle(),
                                right: 5.0,
                              ),
                              Switch(
                                value: rememberMe,
                                onChanged: (value) {
                                  setState(() {
                                    rememberMe = value;
                                  });
                                },
                                activeTrackColor:
                                    CustomTheme.getColor('attention'),
                                activeColor:
                                    CustomTheme.getColor('darkPrimary'),
                              ),
                            ]))),
                    ReuseButton(
                      text: "Need an account? Sign up here!",
                      onPressed: () => handleSignUp(context),
                      buttonType: "text",
                    ),
                    ReuseErrorMessage(text: errorMessage),
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
