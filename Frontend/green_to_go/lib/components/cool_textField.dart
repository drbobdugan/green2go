import 'package:flutter/material.dart';

class CoolTextField extends StatefulWidget {
  final String text;
  final ValueChanged<String> onChanged;
  final bool obscureText;
  final dynamic autofillHints;
  final TextInputType keyboardType;
  final Function onFieldSubmitted;

  CoolTextField(
      {Key key,
      @required this.text,
      this.onChanged,
      this.obscureText,
      this.autofillHints,
      this.keyboardType,
      this.onFieldSubmitted})
      : super(key: key);

  onTextChange(value) {
    onChanged(value);
  }

  @override
  _CoolTextFieldState createState() => _CoolTextFieldState();
}

class _CoolTextFieldState extends State<CoolTextField> {
  final _controller = TextEditingController();

  bool isValidInput() {
    return _controller.text != null && _controller.text != '';
  }

  @override
  void initState() {
    super.initState();
    _controller.addListener(() {
      if (isValidInput()) {
        widget.onTextChange(_controller.text);
      }
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: EdgeInsets.only(bottom: 10.0),
      child: TextFormField(
          controller: _controller,
          decoration: InputDecoration(
              labelText: widget.text,
              contentPadding: EdgeInsets.symmetric(vertical: 0.0),
              suffixIcon: Padding(
                padding: EdgeInsets.only(bottom: 0.0),
                child: isValidInput()
                    ? IconButton(
                        onPressed: () => _controller.clear(),
                        icon: Icon(Icons.clear, size: 16.0),
                      )
                    : null,
              )),
          obscureText: (widget.obscureText == true ? true : false),
          autofillHints:
              (widget.autofillHints == null ? [] : widget.autofillHints),
          keyboardType: (widget.keyboardType == null
              ? TextInputType.text
              : widget.keyboardType),
          textInputAction: TextInputAction.next,
          onFieldSubmitted: widget.onFieldSubmitted),
    );
  }
}
