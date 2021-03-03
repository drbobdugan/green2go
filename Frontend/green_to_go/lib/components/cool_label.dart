import 'package:flutter/material.dart';

class CoolLabel extends StatelessWidget {
  final String text;
  final double left, top, right, bottom;
  final TextStyle textStyle;
  final bool isCenter;

  CoolLabel({
    @required this.text,
    @required this.textStyle,
    this.left = 0.0,
    this.right = 0.0,
    this.top = 0.0,
    this.bottom = 0.0,
    this.isCenter = true,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.fromLTRB(left, top, right, bottom),
      child: Text(
        text,
        textAlign: (isCenter) ? TextAlign.center : TextAlign.left,
        style: textStyle,
      ),
    );
  }
}
