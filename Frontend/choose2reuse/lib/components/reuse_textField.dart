import 'package:flutter/material.dart';

class ReuseTextField extends StatefulWidget {
  const ReuseTextField({
    Key key,
    @required this.text,
    this.initialValue,
    this.visible,
    this.onChanged,
    this.obscureText,
    this.autofillHints,
    this.keyboardType,
    this.onFieldSubmitted,
    this.textInputAction,
    this.node,
    this.enabled = true,
    this.showClearButton = true,
  }) : super(key: key);

  final String text;
  final String initialValue;
  final bool visible;
  final ValueChanged<String> onChanged;
  final bool obscureText;
  final Iterable<String> autofillHints;
  final TextInputType keyboardType;
  final Function onFieldSubmitted;
  final TextInputAction textInputAction;
  final FocusNode node;
  final bool enabled;
  final bool showClearButton;

  void onTextChange(String value) {
    onChanged(value);
  }

  @override
  _ReuseTextFieldState createState() => _ReuseTextFieldState();
}

class _ReuseTextFieldState extends State<ReuseTextField> {
  TextEditingController _controller;

  bool isValidInput() {
    return _controller.text != null && _controller.text != '';
  }

  @override
  void initState() {
    super.initState();
    _controller = TextEditingController(text: widget.initialValue);
    _controller.addListener(() {
      widget.onTextChange(_controller.text);
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
        visible: widget.visible != false,
        child: Padding(
          padding: const EdgeInsets.only(bottom: 10.0),
          child: TextFormField(
              controller: _controller,
              focusNode: widget.node,
              enabled: widget.enabled,
              decoration: InputDecoration(
                  labelText: widget.text,
                  contentPadding: const EdgeInsets.symmetric(vertical: 0.0),
                  suffixIcon: widget.showClearButton
                      ? Padding(
                          padding: const EdgeInsets.only(bottom: 0.0),
                          child: isValidInput()
                              ? IconButton(
                                  onPressed: () => _controller.clear(),
                                  icon: const Icon(Icons.clear, size: 16.0),
                                )
                              : null,
                        )
                      : null),
              obscureText: widget.obscureText == true,
              autofillHints: widget.autofillHints ?? widget.autofillHints,
              keyboardType: widget.keyboardType ?? TextInputType.text,
              textInputAction: widget.textInputAction,
              onFieldSubmitted: (String s) {
                widget.onFieldSubmitted();
              }),
        ));
  }
}
