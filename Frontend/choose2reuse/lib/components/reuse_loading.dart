import 'package:flutter/material.dart';

class ReuseLoading extends StatelessWidget {
  const ReuseLoading({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.center,
      child: Padding(
        padding: const EdgeInsets.symmetric(horizontal: 50.0),
        child: Image.asset(
          'assets/images/c2r_loading.gif',
        ),
      ),
    );
  }
}
