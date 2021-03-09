import 'package:flutter/material.dart';

import '../components/custom_theme.dart';
import '../components/reuse_button.dart';
import '../components/reuse_errorMessage.dart';
import '../components/reuse_label.dart';
import '../components/reuse_strings.dart';
import '../components/reuse_textField.dart';
import '../services/api.dart';
import '../services/navigation_service.dart';
import '../services/user_service.dart';
import '../static/user.dart';
import '../static/student.dart';

class ValidationPage extends StatefulWidget {
  const ValidationPage({Key key, @required this.user}) : super(key: key);

  final NewUser user;

  Future<APIResponse> onVerify(String email, String code) async {
    return await UserService.validateCode(email, code);
  }

  Future<bool> onSendCode() async {
    //return await UserService.sendCode(user);
    return false;
  }

  NewUser getUser() => user;

  @override
  _ValidationPageState createState() => _ValidationPageState();
}

class _ValidationPageState extends State<ValidationPage> {
  String email = '';
  String code = '';
  String errorMessage = '';

  bool isValidCode() {
    if (code == '') {
      setState(() {
        errorMessage = ReuseStrings.invalidCodeErrorMessage();
      });
      return false;
    }
    return true;
  }

  void handleVerify(BuildContext context) {
    if (isValidCode()) {
      widget.onVerify(email, code).then((APIResponse response) {
        if (response.success) {
          NavigationService(context: context)
              .goHome(StudentAuth(response.data as Map<String, dynamic>));
        } else {
          setState(() {
            errorMessage = response.message;
          });
        }
      });
    }
  }

  void handleNewCode(BuildContext context) {
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    email = widget.user.email;

    return Scaffold(
      backgroundColor: Colors.white,
      resizeToAvoidBottomPadding: false,
      resizeToAvoidBottomInset: true,
      appBar: AppBar(
        title: Text(ReuseStrings.appName()),
      ),
      body: GestureDetector(
        onTap: () {
          final FocusScopeNode currentFocus = FocusScope.of(context);
          if (!currentFocus.hasPrimaryFocus) {
            currentFocus.unfocus();
          }
        },
        child: SingleChildScrollView(
          padding: const EdgeInsets.all(50.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              ReuseLabel(
                text: ReuseStrings.welcomeLabel(),
                textStyle: CustomTheme.primaryLabelStyle(),
                bottom: 15.0,
              ),
              ReuseLabel(
                text: ReuseStrings.validationInstruction(),
                textStyle: CustomTheme.primaryLabelStyle(isBold: false),
                bottom: 15.0,
              ),
              ReuseTextField(
                  visible: widget.user.email == '',
                  text: ReuseStrings.emailField(),
                  onChanged: (String value) {
                    setState(() {
                      email = value;
                    });
                  },
                  autofillHints: const <String>[AutofillHints.email],
                  keyboardType: TextInputType.emailAddress),
              ReuseTextField(
                  text: ReuseStrings.enterValidationCodeField(),
                  onChanged: (String value) {
                    setState(() {
                      code = value;
                    });
                  }),
              ReuseButton(
                text: ReuseStrings.submit(),
                onPressed: () => handleVerify(context),
                buttonStyle: CustomTheme.primaryButtonStyle(),
                top: 15.0,
              ),
              ReuseButton(
                text: ReuseStrings.requestNewCode(),
                onPressed: () => handleNewCode(context),
                buttonType: 'text',
              ),
              ReuseErrorMessage(text: errorMessage),
            ],
          ),
        ),
      ),
    );
  }
}
