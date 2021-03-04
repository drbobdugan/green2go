import 'package:flutter/material.dart';

class ReuseTextField extends StatefulWidget {
  final String text;
  final bool visible;
  final ValueChanged<String> onChanged;
  final bool obscureText;
  final dynamic autofillHints;
  final TextInputType keyboardType;
  final Function onFieldSubmitted;

  ReuseTextField(
      {Key key,
      @required this.text,
      this.visible,
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
  _ReuseTextFieldState createState() => _ReuseTextFieldState();
}

class _ReuseTextFieldState extends State<ReuseTextField> {
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
    return Visibility(
        visible: (widget.visible != false),
        child: Padding(
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
              obscureText: (widget.obscureText == true),
              autofillHints:
                  (widget.autofillHints == null ? [] : widget.autofillHints),
              keyboardType: (widget.keyboardType == null
                  ? TextInputType.text
                  : widget.keyboardType),
              textInputAction: TextInputAction.next,
              onFieldSubmitted: widget.onFieldSubmitted),
        ));
  }
}
