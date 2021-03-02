import 'package:flutter/material.dart';

class CoolErrorMessage extends StatelessWidget {
  final String text;

  CoolErrorMessage({@required this.text});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 10.0),
      child: Center(
          child: Text(text,
              style: TextStyle(
                  fontStyle: FontStyle.italic, color: Color(0xffff0000)))),
    );
  }
}
