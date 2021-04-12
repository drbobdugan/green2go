import 'package:flutter/material.dart';

class FontScaleBlocker extends StatelessWidget {
  final Widget child;

  const FontScaleBlocker({
    Key key,
    @required this.child,
  }) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return MediaQuery(
      data: MediaQuery.of(context).copyWith(textScaleFactor: 1),
      child: child,
    );
  }
}
