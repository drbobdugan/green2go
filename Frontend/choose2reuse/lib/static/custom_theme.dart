import 'package:flutter/material.dart';

const Map<int, Color> green = <int, Color>{
  50: Color.fromRGBO(46, 133, 110, .1),
  100: Color.fromRGBO(46, 133, 110, .2),
  200: Color.fromRGBO(46, 133, 110, .3),
  300: Color.fromRGBO(46, 133, 110, .4),
  400: Color.fromRGBO(46, 133, 110, .5),
  500: Color.fromRGBO(46, 133, 110, .6),
  600: Color.fromRGBO(46, 133, 110, .7),
  700: Color.fromRGBO(46, 133, 110, .8),
  800: Color.fromRGBO(46, 133, 110, .9),
  900: Color.fromRGBO(46, 133, 110, 1),
};

Map<String, Color> colors = <String, Color>{
  'primary': const Color(0xFF2E856E),
  'darkPrimary': const Color(0xFF005E45),
  'attention': const Color(0xFF6ACB8C),
  'light': const Color(0xFF53DC98),
  'medium': const Color(0xFF44A68C),
  'disabled': Colors.grey,
};

class CustomTheme {
  static Color getColor(String id) {
    return colors[id];
  }

  static ThemeData appTheme() {
    return ThemeData(
      primarySwatch: const MaterialColor(0xFF2E856E, green),
      visualDensity: VisualDensity.adaptivePlatformDensity,
      fontFamily: 'Raleway',
    );
  }

  static ButtonStyle primaryButtonStyle() {
    return ButtonStyle(
      backgroundColor: MaterialStateProperty.all(colors['attention']),
      foregroundColor: MaterialStateProperty.all(Colors.white),
    );
  }

  static TextStyle primaryLabelStyle(
      {double fontSize = 20.0, bool isBold = true}) {
    return TextStyle(
      fontWeight: isBold ? FontWeight.bold : FontWeight.normal,
      fontSize: fontSize,
    );
  }

  static TextStyle secondaryLabelStyle(
      {double fontSize = 13.0, bool isBold = false}) {
    return TextStyle(
      fontWeight: isBold ? FontWeight.bold : FontWeight.normal,
      fontSize: fontSize,
    );
  }

  static TextStyle brightLabelStyle(
      {double fontSize = 24.0, bool isBold = true}) {
    return TextStyle(
        fontWeight: isBold ? FontWeight.bold : FontWeight.normal,
        fontSize: fontSize,
        color: colors['attention']);
  }

  static TextStyle secondaryDarkLabelStyle(
      {double fontSize = 13.0, bool isBold = false}) {
    return TextStyle(
        fontWeight: isBold ? FontWeight.bold : FontWeight.normal,
        fontSize: fontSize,
        color: colors['darkPrimary']);
  }

  static TextStyle leftListStyle({double fontSize = 16.0, bool isBold = true}) {
    return TextStyle(
        fontWeight: isBold ? FontWeight.bold : FontWeight.normal,
        fontSize: fontSize,
        color: const Color(0xffffffff));
  }

  static TextStyle leftIDStyle({double fontSize = 12.0, bool isBold = false}) {
    return TextStyle(
        fontWeight: isBold ? FontWeight.bold : FontWeight.normal,
        fontSize: fontSize,
        color: const Color(0xffffffff));
  }

  static TextStyle rightListStyle({double fontSize = 16, bool isBold = true}) {
    return TextStyle(
      fontWeight: isBold ? FontWeight.bold : FontWeight.normal,
      fontSize: fontSize,
    );
  }

  static TextStyle errorMessageStyle() {
    return const TextStyle(
      fontStyle: FontStyle.italic,
      color: Color(0xffff0000),
    );
  }
}
