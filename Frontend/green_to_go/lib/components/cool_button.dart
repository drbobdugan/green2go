import 'package:flutter/material.dart';

class CoolButton extends StatelessWidget {
  final String text;
  final VoidCallback onPressed;
  final double left, top, right, bottom;
  final ButtonStyle buttonStyle;
  final String buttonType;

  CoolButton({
    @required this.text,
    @required this.onPressed,
    this.buttonStyle,
    this.left = 0.0,
    this.right = 0.0,
    this.top = 0.0,
    this.bottom = 0.0,
    this.buttonType = "elevated",
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.fromLTRB(left, top, right, bottom),
      child: (buttonType == "text")
          ? TextButton(
              child: Text(text),
              onPressed: onPressed,
            )
          : ElevatedButton(
              child: Text(text),
              onPressed: onPressed,
              style: buttonStyle,
            ),
    );
  }
}
