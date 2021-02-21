import 'package:flutter/material.dart';

import '../components/image_banner.dart';
import '../components/cool_textField.dart';
import '../services/userService.dart';
import 'signup.dart';
import 'home.dart';

class LoginPage extends StatefulWidget {
  LoginPage({Key key}) : super(key: key);

  final _userService = UserService();
  void handleSignIn() {
    _userService.getUser('test1@students.stonehill.edu');
  }

  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  void handleSignIn(BuildContext context) {
    widget.handleSignIn();
    Navigator.of(context).pushReplacement(
        MaterialPageRoute(builder: (context) => new HomePage()));
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
                ),
                CoolTextField(
                  text: "Password",
                ),
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
                    child: Text('No existing account? Sign up here'),
                    onPressed: () {
                      Navigator.of(context).push(
                        MaterialPageRoute(
                          builder: (context) => new SignUpPage(),
                        ),
                      );
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

//class MainPage extends StatefulWidget {
// MainPage({Key key, this.title}) : super(key: key);

// final String title;

//@override
///_MainPageState createState() => _MainPageState();
//}

//class _MainPageState extends State<MainPage> {
// @override
// Widget build(BuildContext context) {
//   return Scaffold(
//     appBar: AppBar(
//         title: Text(widget.title),
//       ),
//      body: Center(
//        child: Column(
//           mainAxisAlignment: MainAxisAlignment.center,
//          children: <Widget>[
//            Text(
//              'Welcome!',
//            )
//           ],
//        ),
//      ));
// }
//}
