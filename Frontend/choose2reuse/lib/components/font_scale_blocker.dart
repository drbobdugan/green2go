import 'package:flutter/material.dart';

class FontScaleBlocker extends StatelessWidget {
  const FontScaleBlocker({
    Key key,
    @required this.child,
  }) : super(key: key);

  final Widget child;

  @override
  Widget build(BuildContext context) {
    return MediaQuery(
      data: MediaQuery.of(context).copyWith(textScaleFactor: 1),
      child: child,
    );
  }
}
