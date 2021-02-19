import 'image_banner.dart';
import 'package:flutter/material.dart';
import 'signup.dart';

Map<int, Color> green = {
  50: Color.fromRGBO(46, 133, 110, .1),
  100: Color.fromRGBO(46, 133, 110, .2),
  200: Color.fromRGBO(46, 133, 110, .3),
  300: Color.fromRGBO(46, 133, 110, .4),
  400: Color.fromRGBO(46, 133, 110, .5),
  500: Color.fromRGBO(46, 133, 110, .6),
  600: Color.fromRGBO(46, 133, 110, .7),
  700: Color.fromRGBO(46, 133, 110, .8),
  800: Color.fromRGBO(46, 133, 110, .9),
  900: Color.fromRGBO(46, 133, 110, 1),
};

void main() {
  runApp(GreenToGo());
}

class GreenToGo extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Green2Go',
      theme: ThemeData(
        primarySwatch: MaterialColor(0xFF2E856E, green),
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: Scaffold(
          appBar: AppBar(
            title: Text('Green2Go'),
          ),
          body: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: [
              ImageBanner("assets/images/Green2Gologo.jpg"),
              TextFormField(decoration: InputDecoration(labelText: 'Email')),
              TextFormField(decoration: InputDecoration(labelText: 'Password')),
              ElevatedButton(
                child: Text('Sign In'),
                onPressed: () {},
              ),
              TextButton(
                child: Text('Dont have an account? Sign up now!'),
                onPressed: () {
                  Navigator.push(
                    context,
                    MaterialPageRoute(builder: (context) => SignUp()),
                  );
                },
              )
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
