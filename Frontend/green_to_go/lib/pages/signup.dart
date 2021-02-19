import 'package:flutter/material.dart';

import 'home.dart';

class SignUpPage extends StatelessWidget {
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
                Padding(
                    padding: const EdgeInsets.only(bottom: 10.0),
                    child: Text("Sign Up",
                        style: TextStyle(
                            fontWeight: FontWeight.bold, fontSize: 20.0))),
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
                TextFormField(
                    decoration: InputDecoration(labelText: 'Password')),
                TextFormField(
                    decoration:
                        InputDecoration(labelText: 'Re-enter Password')),
                Padding(
                    padding: const EdgeInsets.only(top: 20.0),
                    child: ElevatedButton(
                      child: Text('Sign Up'),
                      onPressed: () {
                        Navigator.of(context).pop();
                        Navigator.of(context).pushReplacement(MaterialPageRoute(
                            builder: (context) => new HomePage()));
                      },
                    )),
              ],
            )));
  }
}
