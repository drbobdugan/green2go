import 'package:flutter/material.dart';

import 'components/custom_theme.dart';
import 'pages/login.dart';

void main() {
  runApp(
    Choose2ReuseApp(),
  );
}

class Choose2ReuseApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Choose2Reuse',
      theme: CustomTheme.appTheme(),
      home: LoginPage(),
    );
  }
}
