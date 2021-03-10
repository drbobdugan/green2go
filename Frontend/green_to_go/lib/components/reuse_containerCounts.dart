import 'package:flutter/material.dart';

class ContainerCounts extends StatelessWidget {
  const ContainerCounts({
    Key key,
    @required this.text,
    @required this.textStyle,
    this.left = 0.0,
    this.right = 0.0,
    this.top = 0.0,
    this.bottom = 0.0,
    this.isCenter = true,
    @required this.backgroundName,
    @required this.backgroundHeight,
    @required this.backgroundWidth,
  }) : super(key: key);

  final String text, backgroundName;
  final double left, top, right, bottom, backgroundHeight, backgroundWidth;
  final TextStyle textStyle;
  final bool isCenter;

  @override
  Widget build(BuildContext context) {
    return Padding(
        padding: EdgeInsets.fromLTRB(left, top, right, bottom),
        child: Stack(
          children: <Widget>[
            Container(
                alignment: Alignment.center,
                height: backgroundHeight,
                width: backgroundWidth,
                decoration: BoxDecoration(
                    image: DecorationImage(
                        image: AssetImage(backgroundName), fit: BoxFit.cover))),
            Container(
              alignment: Alignment.center,
              height: backgroundHeight,
              width: backgroundWidth,
              child: Padding(
                  padding: const EdgeInsets.only(bottom: 10.0),
                  child: Text(
                    text,
                    textAlign: isCenter ? TextAlign.center : TextAlign.left,
                    style: textStyle,
                  )),
            )
          ],
        ));
  }
}
