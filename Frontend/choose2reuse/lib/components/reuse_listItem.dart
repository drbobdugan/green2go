import 'package:flutter/material.dart';

import '../components/reuse_button.dart';
import '../components/reuse_label.dart';
import '../static/container.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';

class ListItem extends StatelessWidget {
  ListItem(
      {Key key,
      @required this.text1,
      @required this.text2,
      @required this.text3,
      @required this.colorID,
      @required this.status,
      @required this.onSubmitDialog})
      : super(key: key);

  final String text1, text2, text3, colorID;
  final ContainerStatus status;
  final Function(String) onSubmitDialog;

  String reportMessage;

  AlertDialog lostDamagedDialog(BuildContext context, bool isUndo) {
    return AlertDialog(
      title: ReuseLabel(
        text: ReuseStrings.lostOrDamagedTitle,
        textStyle: CustomTheme.primaryLabelStyle(),
        isCenter: true,
      ),
      content: SingleChildScrollView(
        child: ListBody(
          children: <Widget>[
            ReuseLabel(
              text: isUndo
                  ? ReuseStrings.undoLostOrDamagedQuestion
                  : ReuseStrings.lostOrDamagedQuestion,
              textStyle: CustomTheme.primaryLabelStyle(fontSize: 16.0),
              isCenter: true,
            ),
            if (isUndo)
              Container(
                  margin: const EdgeInsets.only(top: 20.0),
                  padding: const EdgeInsets.all(8.0),
                  child: SizedBox(
                      width: 200.0,
                      height: 100.0,
                      child: TextField(
                        onChanged: (String text) {
                          reportMessage = text;
                        },
                        maxLines: null,
                        maxLength: 128,
                        decoration: InputDecoration.collapsed(
                            hintText: ReuseStrings.lostOrDamagedPrompt),
                      )),
                  decoration: BoxDecoration(
                    border: Border.all(width: 1.0),
                    borderRadius: const BorderRadius.all(Radius.circular(5.0)),
                  ))
          ],
        ),
      ),
      actions: <Widget>[
        ReuseButton(
          text: ReuseStrings.cancel,
          onPressed: () => Navigator.pop(context),
          buttonType: 'text',
        ),
        ReuseButton(
          text: isUndo ? ReuseStrings.yes : ReuseStrings.submit,
          onPressed: () {
            Navigator.pop(context);
            onSubmitDialog(reportMessage);
          },
          buttonType: 'text',
        ),
      ],
    );
  }

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
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: <Widget>[
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  ReuseLabel(
                    text: text1,
                    textStyle: CustomTheme.leftListStyle(),
                    right: 5,
                  ),
                ],
              ),
              Row(
                mainAxisAlignment: MainAxisAlignment.spaceAround,
                children: <Widget>[
                  Flexible(
                    child: ReuseLabel(
                      text: text3,
                      textStyle: CustomTheme.leftIDStyle(),
                      right: 5,
                    ),
                  )
                ],
              )
            ],
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
              if (status == ContainerStatus.CheckedOut)
                IconButton(
                    icon: Icon(
                      Icons.broken_image_rounded,
                      size: 30.0,
                      color: CustomTheme.getColor('attention'),
                    ),
                    onPressed: () => showDialog<void>(
                        context: context,
                        builder: (BuildContext context) =>
                            lostDamagedDialog(context, false))),
              if (status == ContainerStatus.DamagedLost)
                IconButton(
                    icon: Icon(
                      Icons.undo,
                      size: 30.0,
                      color: CustomTheme.getColor('attention'),
                    ),
                    onPressed: () => showDialog<void>(
                        context: context,
                        builder: (BuildContext context) =>
                            lostDamagedDialog(context, true)))
            ],
          ),
        ),
      ],
    );
  }
}
