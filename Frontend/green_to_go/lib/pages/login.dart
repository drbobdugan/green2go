import 'package:Choose2Reuse/services/navigation_service.dart';
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../components/custom_theme.dart';
import '../components/reuse_button.dart';
import '../components/reuse_errorMessage.dart';
import '../components/reuse_label.dart';
import '../components/reuse_loading.dart';
import '../components/reuse_textField.dart';
import '../services/api.dart';
import '../services/user_service.dart';
import '../static/student.dart';
import '../static/user.dart';

class LoginPage extends StatefulWidget {
  const LoginPage({Key key}) : super(key: key);

  Future<APIResponse> onLogIn(ExistingUser user) async {
    return await UserService.logIn(user);
  }

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final FocusNode emailNode = FocusNode();
  final FocusNode passwordNode = FocusNode();

  ExistingUser user = ExistingUser();
  bool isLoggedIn;
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
    } else {
      setState(() {
        isLoggedIn = false;
      });
    }
  }

  Future<void> handleLogIn(BuildContext context) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    widget.onLogIn(user).then((APIResponse response) {
      if (response.success) {
        if (rememberMe) {
          prefs.setString('email', user.email);
          prefs.setString('password', user.password);
        }

        NavigationService(context: context)
            .goHome(StudentAuth(response.data as Map<String, dynamic>));
      } else {
        setState(() {
          errorMessage = response.message;
        });
      }
    });
  }

  void fieldNextFocus(
      BuildContext context, FocusNode currentFocus, FocusNode nextFocus) {
    currentFocus.unfocus();
    if (nextFocus != null) {
      FocusScope.of(context).requestFocus(nextFocus);
    }
  }

  void handleSignUp(BuildContext context) {
    NavigationService(context: context).goToPage(C2RPages.signup, user);
  }

  @override
  Widget build(BuildContext context) {
    if (isLoggedIn == true) {
      handleLogIn(context);
    }
    if (isLoggedIn != false) {
      return const Scaffold(
          backgroundColor: Colors.white, body: ReuseLoading());
    }
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: AppBar(
        title: const Text('Choose2Reuse'),
      ),
      body: Form(
        child: SingleChildScrollView(
          child: Column(
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.symmetric(
                    vertical: 30.0, horizontal: 10.0),
                child: FittedBox(
                  fit: BoxFit.fitWidth,
                  alignment: Alignment.bottomCenter,
                  child: ConstrainedBox(
                    constraints:
                        const BoxConstraints(minWidth: 1, minHeight: 1), // here
                    child: Image.asset(
                      'assets/images/choose2reuse_logo.jpg',
                    ),
                  ),
                ),
              ),
              Padding(
                padding: const EdgeInsets.only(left: 50.0, right: 50.0),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.stretch,
                  children: <Widget>[
                    ReuseTextField(
                        text: 'Email',
                        node: emailNode,
                        onChanged: (String value) {
                          setState(() {
                            user.email = value;
                          });
                        },
                        autofillHints: const <String>[AutofillHints.email],
                        keyboardType: TextInputType.emailAddress,
                        textInputAction: TextInputAction.next,
                        onFieldSubmitted: () {
                          fieldNextFocus(context, emailNode, passwordNode);
                        }),
                    ReuseTextField(
                        text: 'Password',
                        obscureText: true,
                        onChanged: (String value) {
                          setState(() {
                            user.password = value;
                          });
                        },
                        autofillHints: const <String>[AutofillHints.password],
                        textInputAction: TextInputAction.done,
                        onFieldSubmitted: () {
                          fieldNextFocus(context, passwordNode, null);
                        }),
                    ReuseButton(
                      text: 'Log In',
                      onPressed: () => handleLogIn(context),
                      buttonStyle: CustomTheme.primaryButtonStyle(),
                      top: 10.0,
                    ),
                    Align(
                        alignment: Alignment.bottomRight,
                        child: SizedBox(
                            width: 155.0,
                            height: 40.0,
                            child: Row(children: <Widget>[
                              ReuseLabel(
                                text: 'Remember me',
                                textStyle: CustomTheme.secondaryLabelStyle(),
                                right: 5.0,
                              ),
                              Switch(
                                value: rememberMe,
                                onChanged: (bool value) {
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
                      text: 'Need an account? Sign up here!',
                      onPressed: () => handleSignUp(context),
                      buttonType: 'text',
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
