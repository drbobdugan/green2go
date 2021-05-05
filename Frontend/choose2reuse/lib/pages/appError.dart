import 'package:flutter/material.dart';

import '../components/font_scale_blocker.dart';
import '../components/reuse_label.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';

class AppErrorPage extends StatelessWidget {
  const AppErrorPage({Key key}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return FontScaleBlocker(
        child: Scaffold(
      backgroundColor: Colors.white,
      body: Form(
        child: SingleChildScrollView(
          child: Column(
            children: <Widget>[
              Padding(
                padding: const EdgeInsets.symmetric(
                    vertical: 50.0, horizontal: 10.0),
                child: FittedBox(
                  fit: BoxFit.fitWidth,
                  alignment: Alignment.bottomCenter,
                  child: ConstrainedBox(
                    constraints:
                        const BoxConstraints(minWidth: 1, minHeight: 1), // here
                    child: Image.asset('assets/images/choose2reuse_icon.jpg',
                        scale: 6),
                  ),
                ),
              ),
              ReuseLabel(
                text: ReuseStrings.appError,
                textStyle: CustomTheme.secondaryLabelStyle(fontSize: 16.0),
                top: 10.0,
                left: 5.0,
                right: 5.0,
                backgroundWidth: 100,
              )
            ],
          ),
        ),
      ),
    ));
  }
}
