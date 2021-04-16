import 'package:Choose2Reuse/components/font_scale_blocker.dart';
import 'package:flutter/material.dart';
import '../components/reuse_label.dart';
import '../components/reuse_textField.dart';
import '../components/reuse_userBar.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';

class ProfilePage extends StatefulWidget {
  const ProfilePage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  @override
  _ProfilePageState createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  StudentDetails user;
  final FocusNode firstNameNode = FocusNode();
  final FocusNode middleNameNode = FocusNode();
  final FocusNode lastNameNode = FocusNode();
  final FocusNode emailNode = FocusNode();
  final FocusNode phoneNumNode = FocusNode();
  final FocusNode passwordNode = FocusNode();
  final FocusNode confirmPasswordNode = FocusNode();

  @override
  void initState() {
    super.initState();

    user = StudentDetails(widget.userAuth);
  }

  void fieldNextFocus(
      BuildContext context, FocusNode currentFocus, FocusNode nextFocus) {
    currentFocus.unfocus();
    if (nextFocus != null) {
      FocusScope.of(context).requestFocus(nextFocus);
    }
  }

  @override
  Widget build(BuildContext context) {
    return FontScaleBlocker(
      child: Scaffold(
        backgroundColor: Colors.white,
        resizeToAvoidBottomInset: true,
        appBar: UserAppBar(userAuth: widget.userAuth),
        body: GestureDetector(
          onTap: () {
            final FocusScopeNode currentFocus = FocusScope.of(context);
            if (!currentFocus.hasPrimaryFocus) {
              currentFocus.unfocus();
            }
          },
          child: SingleChildScrollView(
            padding: const EdgeInsets.only(top: 30.0, left: 50.0, right: 50.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                ReuseLabel(
                  text: ReuseStrings.profilePageTitle,
                  textStyle: CustomTheme.primaryLabelStyle(),
                  bottom: 20.0,
                ),
                ReuseTextField(
                  text: ReuseStrings.firstNameField,
                  node: firstNameNode,
                  onChanged: (String value) {
                    setState(() {
                      user.firstName = value;
                    });
                  },
                  autofillHints: const <String>[AutofillHints.givenName],
                  textInputAction: TextInputAction.next,
                  onFieldSubmitted: () {
                    fieldNextFocus(context, firstNameNode, middleNameNode);
                  },
                ),
                ReuseTextField(
                    text: ReuseStrings.middleNameField,
                    node: middleNameNode,
                    onChanged: (String value) {
                      setState(() {
                        user.middleName = value;
                      });
                    },
                    autofillHints: const <String>[AutofillHints.middleName],
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, middleNameNode, lastNameNode);
                    }),
                ReuseTextField(
                    text: ReuseStrings.lastNameField,
                    node: lastNameNode,
                    onChanged: (String value) {
                      setState(() {
                        user.lastName = value;
                      });
                    },
                    autofillHints: const <String>[AutofillHints.familyName],
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, lastNameNode, emailNode);
                    }),
                ReuseTextField(
                  text: ReuseStrings.emailField,
                  initialValue: widget.userAuth.email,
                  enabled: false,
                  showClearButton: false,
                ),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
