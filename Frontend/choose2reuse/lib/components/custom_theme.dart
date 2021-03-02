import 'package:flutter/material.dart';

Map<String, Color> colors = {
  "primary": Color(0xFF2E856E),
  "darkPrimary": Color(0xFF006A4E),
  "attention": Color(0xFF03CD3B),
  "light": Color(0xFFD2FFCC),
  "disabled": Colors.grey,
};

class CustomTheme {
  static ThemeData get appTheme {
    return ThemeData(
      primarySwatch: colors["primary"],
      visualDensity: VisualDensity.adaptivePlatformDensity,
      fontFamily: 'Raleway',
      elevatedButtonTheme: ElevatedButtonThemeData(
        style: ElevatedButton.styleFrom(
          primary: colors["attention"],
          onPrimary: Colors.white,
          padding: EdgeInsets.fromLTRB(15, 10, 15, 10),
        ),
      ),
    );
  }
}
