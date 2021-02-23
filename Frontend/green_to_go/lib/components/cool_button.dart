import 'package:flutter/material.dart';

class CoolButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final double left, top, right, bottom;

  CoolButton({
    @required this.text,
    @required this.onPressed,
    this.left = 0.0,
    this.right = 0.0,
    this.top = 0.0,
    this.bottom = 0.0,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.fromLTRB(left, top, right, bottom),
      child: ElevatedButton(
        child: Text(text),
        onPressed: onPressed,
      ),
    );
  }
}
