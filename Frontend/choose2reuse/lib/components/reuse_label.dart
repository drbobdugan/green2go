import 'package:flutter/material.dart';

class ReuseLabel extends StatelessWidget {
  const ReuseLabel({
    Key key,
    @required this.text,
    @required this.textStyle,
    this.left = 0.0,
    this.right = 0.0,
    this.top = 0.0,
    this.bottom = 0.0,
    this.isCenter = true,
    this.hasBackground = false,
    this.backgroundName,
    this.backgroundHeight,
    this.backgroundWidth,
  }) : super(key: key);

  final String text, backgroundName;
  final double left, top, right, bottom, backgroundHeight, backgroundWidth;
  final TextStyle textStyle;
  final bool isCenter, hasBackground;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.fromLTRB(left, top, right, bottom),
      child: hasBackground
          ? Stack(
              children: <Widget>[
                Container(
                  alignment: Alignment.center,
                  height: backgroundHeight,
                  width: backgroundWidth,
                  child: Image.asset(
                    backgroundName,
                    fit: BoxFit.cover,
                  ),
                ),
                Container(
                  alignment: Alignment.center,
                  height: backgroundHeight,
                  width: backgroundWidth,
                  child: Text(
                    text,
                    textAlign: isCenter ? TextAlign.center : TextAlign.left,
                    style: textStyle,
                  ),
                )
              ],
            )
          : Text(
              text,
              textScaleFactor: 1,
              textAlign: isCenter ? TextAlign.center : TextAlign.left,
              style: textStyle,
            ),
    );
  }
}
