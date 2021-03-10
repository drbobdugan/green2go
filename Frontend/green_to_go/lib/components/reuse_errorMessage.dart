import 'package:flutter/material.dart';

import '../components/custom_theme.dart';

class ReuseErrorMessage extends StatelessWidget {
  const ReuseErrorMessage({Key key, @required this.text}) : super(key: key);

  final String text;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 10.0),
      child: Center(
        child: Text(
          text,
          style: CustomTheme.errorMessageStyle(),
        ),
      ),
    );
  }
}
