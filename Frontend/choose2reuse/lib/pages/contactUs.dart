import 'package:flutter/material.dart';

import '../components/font_scale_blocker.dart';
import '../components/reuse_button.dart';
import '../components/reuse_errorMessage.dart';
import '../components/reuse_label.dart';
import '../components/reuse_loading.dart';
import '../components/reuse_textField.dart';
import '../components/reuse_userBar.dart';
import '../services/api.dart';
import '../services/navigation_service.dart';
import '../services/user_service.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';
import '../static/user.dart';

class ContactUsPage extends StatefulWidget {
  const ContactUsPage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetUser() async {
    return await UserService.getUser(userAuth);
  }

  Future<String> onSendEmailContactUs(
      String userEmail, String subject, String body) {
    return UserService.onSendEmailContactUs(userAuth, userEmail, subject, body);
  }

  @override
  _ContactUsPageState createState() => _ContactUsPageState();
}

class _ContactUsPageState extends State<ContactUsPage> {
  final FocusNode emailNode = FocusNode();
  final FocusNode emailSubjectNode = FocusNode();
  final FocusNode emailBodyNode = FocusNode();

  String errorMessage = '';
  String userEmail = '';
  String subject = '';
  String body = '';

  DetailedUser detailedUser;

  @override
  void initState() {
    super.initState();

    widget.onGetUser().then((APIResponse response) {
      if (response.success) {
        setState(() {
          detailedUser = DetailedUser(response.data);
        });
      }
    });
  }

  void fieldNextFocus(
      BuildContext context, FocusNode currentFocus, FocusNode nextFocus) {
    currentFocus.unfocus();
    if (nextFocus != null) {
      FocusScope.of(context).requestFocus(nextFocus);
    }
  }

  void showSuccess(BuildContext context) {
    ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(content: Text(ReuseStrings.updateProfileSuccess)));
  }

  void onSendEmail() {
    widget
        .onSendEmailContactUs(userEmail, subject, body)
        .then((String response) {
      if (response == 'success') {
        setState(() {
          errorMessage = '';
        });
        showSuccess(context);
      } else {
        setState(() {
          errorMessage = response;
        });
      }
    });
  }

  @override
  Widget build(BuildContext context) {
    if (detailedUser == null) {
      return const Scaffold(
        backgroundColor: Colors.white,
        body: ReuseLoading(),
      );
    }

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
                  text: ReuseStrings.contactUsPageTitle,
                  textStyle: CustomTheme.primaryLabelStyle(),
                  bottom: 20.0,
                ),
                ReuseTextField(
                  text: ReuseStrings.emailField,
                  initialValue: detailedUser.email,
                  node: emailNode,
                  enabled: false,
                  showClearButton: false,
                  onFieldSubmitted: () {
                    fieldNextFocus(context, emailNode, emailSubjectNode);
                  },
                ),
                ReuseTextField(
                  text: ReuseStrings.emailSubject,
                  initialValue: '',
                  node: emailSubjectNode,
                  onChanged: (String value) {
                    setState(() {
                      subject = value;
                    });
                  },
                  textInputAction: TextInputAction.next,
                  onFieldSubmitted: () {
                    fieldNextFocus(context, emailSubjectNode, emailBodyNode);
                  },
                ),
                ReuseTextField(
                    text: ReuseStrings.emailBody,
                    initialValue: '',
                    node: emailBodyNode,
                    onChanged: (String value) {
                      setState(() {
                        body = value;
                      });
                    },
                    //autofillHints: const <String>[AutofillHints.middleName],
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, emailBodyNode, null);
                    }),
                ReuseButton(
                  text: ReuseStrings.sendEmail,
                  onPressed: onSendEmail,
                  buttonStyle: CustomTheme.primaryButtonStyle(),
                  top: 20.0,
                ),
                ReuseErrorMessage(text: errorMessage),
              ],
            ),
          ),
        ),
      ),
    );
  }
}
