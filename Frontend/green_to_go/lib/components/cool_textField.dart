import 'package:flutter/material.dart';

class CoolTextField extends StatelessWidget {
  final String text;
  CoolTextField({@required this.text});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: 10.0),
      child: TextFormField(
        decoration: InputDecoration(
          labelText: text,
          contentPadding: EdgeInsets.only(bottom: 0),
        ),
      ),
    );
  }
}
