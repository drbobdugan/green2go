import 'package:flutter/material.dart';

import '../components/image_banner.dart';
import '../components/cool_textField.dart';
import '../services/userService.dart';
import 'signup.dart';
import 'home.dart';

class LoginPage extends StatefulWidget {
  LoginPage({Key key}) : super(key: key);

  final _userService = UserService();
  void onSignIn(String email, String password) {
    _userService.signIn({'email': email, 'password': password});
  }

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  String email;
  String password;

  handleSignIn(BuildContext context) {
    widget.onSignIn(email, password);
    Navigator.of(context)
        .push(MaterialPageRoute(builder: (context) => new HomePage()));
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
                        email = value;
                      });
                    }),
                CoolTextField(
                    text: "Password",
                    onChanged: (value) {
                      setState(() {
                        password = value;
                      });
                    }),
                Padding(
                  padding: const EdgeInsets.only(top: 15.0),
                  child: ElevatedButton(
                    child: Text('Sign In'),
                    onPressed: () {
                      handleSignIn(context);
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
              ],
            ),
          ),
        ],
      ),
    );
  }
}
