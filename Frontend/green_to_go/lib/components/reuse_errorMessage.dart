import '../components/custom_theme.dart';
import 'package:flutter/material.dart';

class ReuseErrorMessage extends StatelessWidget {
  final String text;

  ReuseErrorMessage({@required this.text});

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
