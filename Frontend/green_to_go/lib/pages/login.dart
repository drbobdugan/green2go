import 'package:flutter/material.dart';
import 'package:email_validator/email_validator.dart';

import '../components/image_banner.dart';
import '../components/cool_textField.dart';
import '../services/userService.dart';
import '../static/user.dart';
import 'signup.dart';
import 'home.dart';

class LoginPage extends StatefulWidget {
  LoginPage({Key key}) : super(key: key);

  final _userService = UserService();
  Future<String> onLogIn(user) async {
    return await _userService.logIn(user);
  }

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  ExistingUser user = new ExistingUser();
  String errorMessage = '';

  bool isValidLogin() {
    if (user.email == '' || user.password == '') {
      setState(() {
        errorMessage = 'Please enter an email and password.';
      });
      return false;
    }
    if (!EmailValidator.validate(user.email)) {
      setState(() {
        errorMessage = 'Please enter a valid email.';
      });
      return false;
    }
    return true;
  }

  handleLogIn(BuildContext context) {
    widget.onLogIn(user).then((response) {
      print(response);
      // if (response) {
      //   Navigator.of(context)
      //       .push(MaterialPageRoute(builder: (context) => new HomePage()));
      // } else {
      //   setState(() {
      //     errorMessage = 'An error occured, please try again later.';
      //   });
      // }
    });
  }

  handleSignUp(BuildContext context) {
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => new SignUpPage()));
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Green2Go'),
      ),
      body: Column(
        children: [
          ImageBanner("assets/images/green2go_logo.jpg"),
          Padding(
            padding: const EdgeInsets.only(left: 50.0, right: 50.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                CoolTextField(
                    text: "Email",
                    onChanged: (value) {
                      setState(() {
                        user.email = value;
                      });
                    }),
                CoolTextField(
                    text: "Password",
                    obscureText: true,
                    onChanged: (value) {
                      setState(() {
                        user.password = value;
                      });
                    }),
                Padding(
                  padding: const EdgeInsets.only(top: 15.0),
                  child: ElevatedButton(
                    child: Text('Sign In'),
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
                Padding(
                  padding: const EdgeInsets.only(top: 10.0),
                  child: Center(
                      child: Text(errorMessage,
                          style: TextStyle(
                              fontStyle: FontStyle.italic,
                              color: Color(0xffff0000)))),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}
