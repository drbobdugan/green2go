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
  runApp(SignUp());
}

class SignUp extends StatelessWidget {
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
              Text("Sign Up"),
              TextFormField(
                  decoration: InputDecoration(labelText: 'First Name')),
              TextFormField(
                  decoration: InputDecoration(labelText: 'Last Name')),
              TextFormField(
                  decoration: InputDecoration(labelText: 'Graduation Year')),
              TextFormField(
                  decoration: InputDecoration(labelText: 'School Email')),
              TextFormField(
                  decoration: InputDecoration(labelText: 'Phone Number')),
              TextFormField(decoration: InputDecoration(labelText: 'Password')),
              TextFormField(
                  decoration: InputDecoration(labelText: 'Re-enter Password')),
              ElevatedButton(
                child: Text('Sign Up'),
                onPressed: () {},
              ),
            ],
          )),
    );
  }
}
