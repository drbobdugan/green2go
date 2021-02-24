import 'package:flutter/material.dart';

class CoolTextField extends StatelessWidget {
  final String text;
  final ValueChanged<String> onChanged;
  final bool obscureText;
  final dynamic autofillHints;
  final TextInputType keyboardType;

  CoolTextField(
      {@required this.text,
      this.onChanged,
      this.obscureText,
      this.autofillHints,
      this.keyboardType});

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: 10.0),
      child: TextFormField(
        decoration: InputDecoration(
          labelText: text,
          contentPadding: EdgeInsets.only(bottom: 0),
        ),
        onChanged: onChanged,
        obscureText: (obscureText == true ? true : false),
        autofillHints: (autofillHints == null ? [] : autofillHints),
        keyboardType:
            (keyboardType == null ? TextInputType.text : keyboardType),
      ),
    );
  }
}
