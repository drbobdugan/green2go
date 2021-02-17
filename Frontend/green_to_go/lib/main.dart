import 'package:flutter/material.dart';

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
      title: 'Green To Go',
      theme: ThemeData(
        primarySwatch: MaterialColor(0xFF2E856E, green),
        visualDensity: VisualDensity.adaptivePlatformDensity,
      ),
      home: MainPage(title: 'Green To Go'),
    );
  }
}

class MainPage extends StatefulWidget {
  MainPage({Key key, this.title}) : super(key: key);

  final String title;

  @override
  _MainPageState createState() => _MainPageState();
}

class _MainPageState extends State<MainPage> {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
        appBar: AppBar(
          title: Text(widget.title),
        ),
        body: Center(
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Text(
                'Welcome!',
              )
            ],
          ),
        ));
  }
}
