import 'package:flutter/material.dart';

import '../components/image_banner.dart';
import 'signup.dart';

class LoginPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: Text('Green2Go'),
      ),
      body: Padding(
          padding: const EdgeInsets.all(50.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              ImageBanner("assets/images/Green2Gologo.jpg"),
              TextFormField(decoration: InputDecoration(labelText: 'Email')),
              TextFormField(decoration: InputDecoration(labelText: 'Password')),
              Padding(
                  padding: const EdgeInsets.only(top: 20.0),
                  child: ElevatedButton(
                    child: Text('Sign In'),
                    onPressed: () {},
                  )),
              Padding(
                  padding: const EdgeInsets.only(top: 10.0),
                  child: TextButton(
                    child: Text('Dont have an account? Sign up now!'),
                    onPressed: () {
                      Navigator.of(context).push(MaterialPageRoute(
                          builder: (context) => new SignUpPage()));
                    },
                  ))
            ],
          )),
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
