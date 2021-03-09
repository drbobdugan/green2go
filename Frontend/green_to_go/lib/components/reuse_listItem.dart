import 'package:flutter/material.dart';
import '../components/custom_theme.dart';

class ListItem extends StatelessWidget {
  const ListItem({
    Key key,
    @required this.text1,
    @required this.text2,
    @required this.textStyle,
    this.color,
  }) : super(key: key);

  final String text1, text2;
  final TextStyle textStyle;
  final Color color;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: <Widget>[
        Container(
            padding: const EdgeInsets.only(left: 25),
            alignment: Alignment.centerLeft,
            width: MediaQuery.of(context).size.width / 2.5,
            height: 60,
            decoration: const BoxDecoration(
                color: Color(0xFF2E856E),
                borderRadius: BorderRadius.only(
                    topRight: Radius.circular(25),
                    bottomRight: Radius.circular(25))),
            child: Text(text1,
                textAlign: TextAlign.center,
                style: CustomTheme.leftListStyle())),
        Container(
            alignment: Alignment.centerRight,
            width: MediaQuery.of(context).size.width / 2,
            height: 60,
            child: Text(text2,
                textAlign: TextAlign.center,
                style: CustomTheme.rightListStyle()))
      ],
    );
  }
}
