import 'package:flutter/material.dart';

import '../components/reuse_label.dart';
import '../static/custom_theme.dart';

class ListItem extends StatelessWidget {
  const ListItem({
    Key key,
    @required this.text1,
    @required this.text2,
    @required this.text3,
    @required this.colorID,
    this.iconOnPressed,
  }) : super(key: key);

  final String text1, text2, text3, colorID;
  final VoidCallback iconOnPressed;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: <Widget>[
        Container(
          alignment: Alignment.centerLeft,
          width: MediaQuery.of(context).size.width * 0.4,
          height: 65,
          decoration: BoxDecoration(
            color: CustomTheme.getColor(colorID),
            borderRadius: const BorderRadius.only(
              topRight: Radius.circular(25),
              bottomRight: Radius.circular(25),
            ),
          ),
          child: Padding(
            padding: const EdgeInsets.only(left: 15.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: <Widget>[
                ReuseLabel(
                  text: text1,
                  textStyle: CustomTheme.leftListStyle(),
                  right: 5,
                ),
                ReuseLabel(
                  text: text3,
                  textStyle: CustomTheme.leftIDStyle(),
                  right: 5,
                )
              ],
            ),
          ),
        ),
        Container(
          alignment: Alignment.centerRight,
          width: MediaQuery.of(context).size.width * 0.6,
          height: 65,
          child: Row(
            mainAxisAlignment: MainAxisAlignment.spaceAround,
            children: <Widget>[
              ReuseLabel(
                text: text2,
                textStyle: CustomTheme.rightListStyle(
                    fontSize: MediaQuery.of(context).size.width * 0.04),
                left: 10,
              ),
              IconButton(
                icon: Image.asset('assets/images/broken-glass.png'),
                onPressed: null,
              ),
            ],
          ),
        ),
      ],
    );
  }
}
