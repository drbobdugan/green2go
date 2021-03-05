import 'package:flutter/material.dart';

class ReuseLoading extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Align(
      alignment: Alignment.center,
      child: Padding(
        padding: EdgeInsets.symmetric(horizontal: 50.0),
        child: Image.asset(
          'assets/images/c2r_loading.gif',
        ),
      ),
    );
  }
}
