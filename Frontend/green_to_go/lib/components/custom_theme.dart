import 'package:flutter/material.dart';

const Map<int, Color> green = <int, Color>{
  50: Color.fromRGBO(70, 154, 45, .1),
  100: Color.fromRGBO(70, 154, 45, .2),
  200: Color.fromRGBO(70, 154, 45, .3),
  300: Color.fromRGBO(70, 154, 45, .4),
  400: Color.fromRGBO(70, 154, 45, .5),
  500: Color.fromRGBO(70, 154, 45, .6),
  600: Color.fromRGBO(70, 154, 45, .7),
  700: Color.fromRGBO(70, 154, 45, .8),
  800: Color.fromRGBO(70, 154, 45, .9),
  900: Color.fromRGBO(70, 154, 45, 1),
};

Map<String, Color> colors = <String, Color>{
  'primary': const Color(0xFF469A2D),
  'darkPrimary': const Color(0xFF469A2D),
  'attention': const Color(0xFF469A2D),
  'light': const Color(0xFF469A2D),
  'disabled': Colors.grey,
};

class CustomTheme {
  static Color getColor(String id) {
    return colors[id];
  }

  static ThemeData appTheme() {
    return ThemeData(
      primarySwatch: const MaterialColor(0xFF469A2D, green),
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

  static TextStyle rightListStyle(
      {double fontSize = 16.0, bool isBold = true}) {
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
