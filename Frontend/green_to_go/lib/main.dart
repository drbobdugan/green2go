import 'package:flutter/material.dart';

import 'pages/login.dart';

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
  runApp(
    Green2GoApp(),
  );
}

class Green2GoApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Green2Go',
      theme: ThemeData(
          primarySwatch: MaterialColor(0xFF2E856E, green),
          visualDensity: VisualDensity.adaptivePlatformDensity,
          fontFamily: 'Raleway'),
      home: LoginPage(),
    );
  }
}
