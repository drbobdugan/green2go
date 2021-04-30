import 'package:Choose2Reuse/components/font_scale_blocker.dart';
import 'package:Choose2Reuse/services/navigation_service.dart';
import 'package:flutter/material.dart';

import '../components/reuse_button.dart';
import '../components/reuse_errorMessage.dart';
import '../components/reuse_label.dart';
import '../components/reuse_textField.dart';
import '../services/api.dart';
import '../services/user_service.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/user.dart';

class ForgotPasswordPage extends StatefulWidget {
  const ForgotPasswordPage({Key key}) : super(key: key);

  Future<APIResponse> onSendCode(String email) async {
    return await UserService.resendCode(email);
  }

  Future<APIResponse> onNewPassword(
      String authCode, String email, String password) async {
    return await UserService.forgotPassword(authCode, email, password);
  }

  @override
  _ForgotPasswordPageState createState() => _ForgotPasswordPageState();
}

class _ForgotPasswordPageState extends State<ForgotPasswordPage> {
  final FocusNode authCodeNode = FocusNode();
  final FocusNode newPasswordNode = FocusNode();
  final FocusNode confirmNewPasswordNode = FocusNode();

  String email = '';
  String authCode = '';
  String newPassword = '';
  String confirmNewPassword = '';
  String errorMessage = '';
  bool codeSent = false;

  void fieldNextFocus(
      BuildContext context, FocusNode currentFocus, FocusNode nextFocus) {
    currentFocus.unfocus();
    if (nextFocus != null) {
      FocusScope.of(context).requestFocus(nextFocus);
    }
  }

  void handleSendCode(String email) {
    widget.onSendCode(email).then((APIResponse response) {
      if (response.success) {
        setState(() {
          codeSent = true;
        });
      } else {
        setState(() {
          errorMessage = response.message;
        });
      }
    });
  }

  void handleNewPassword(String authCode, String email, String newPassword,
      String confirmNewPassword) {
    if (newPassword == confirmNewPassword) {
      widget
          .onNewPassword(authCode, email, newPassword)
          .then((APIResponse response) {
        if (response.success) {
          NavigationService(context: context).goToPage(C2RPages.login, email);
        } else {
          setState(() {
            errorMessage = response.message;
          });
        }
      });
    } else {
      setState(() {
        errorMessage = ReuseStrings.passMismatchErrorMessage;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return FontScaleBlocker(
      child: Scaffold(
        backgroundColor: Colors.white,
        resizeToAvoidBottomInset: true,
        appBar: AppBar(
          title: Text(ReuseStrings.appName),
        ),
        body: GestureDetector(
            onTap: () {
              final FocusScopeNode currentFocus = FocusScope.of(context);
              if (!currentFocus.hasPrimaryFocus) {
                currentFocus.unfocus();
              }
            },
            child: SingleChildScrollView(
              padding:
                  const EdgeInsets.only(top: 30.0, left: 50.0, right: 50.0),
              child: Column(
                mainAxisAlignment: MainAxisAlignment.start,
                crossAxisAlignment: CrossAxisAlignment.stretch,
                children: <Widget>[
                  ReuseLabel(
                    text: ReuseStrings.forgotPasswordPageTitle,
                    textStyle: CustomTheme.primaryLabelStyle(),
                    bottom: 20.0,
                  ),
                  ReuseTextField(
                    text: ReuseStrings.emailField,
                    onChanged: (String value) {
                      setState(() {
                        email = value;
                      });
                    },
                    autofillHints: const <String>[AutofillHints.email],
                    visible: !codeSent,
                  ),
                  if (!codeSent)
                    ReuseButton(
                        text: ReuseStrings.sendCode,
                        onPressed: () => handleSendCode(email),
                        buttonStyle: CustomTheme.primaryButtonStyle(),
                        top: 10.0,
                        bottom: 10.0),
                  ReuseTextField(
                      text: ReuseStrings.enterValidationCodeField,
                      node: authCodeNode,
                      onChanged: (String value) {
                        setState(() {
                          authCode = value;
                        });
                      },
                      textInputAction: TextInputAction.next,
                      visible: codeSent,
                      onFieldSubmitted: () {
                        fieldNextFocus(context, authCodeNode, newPasswordNode);
                      }),
                  ReuseTextField(
                      text: ReuseStrings.passwordField,
                      node: newPasswordNode,
                      onChanged: (String value) {
                        setState(() {
                          newPassword = value;
                        });
                      },
                      textInputAction: TextInputAction.next,
                      obscureText: true,
                      visible: codeSent,
                      onFieldSubmitted: () {
                        fieldNextFocus(
                            context, newPasswordNode, confirmNewPasswordNode);
                      }),
                  ReuseTextField(
                      text: ReuseStrings.confirmPasswordField,
                      node: confirmNewPasswordNode,
                      onChanged: (String value) {
                        setState(() {
                          confirmNewPassword = value;
                        });
                      },
                      textInputAction: TextInputAction.next,
                      obscureText: true,
                      visible: codeSent,
                      onFieldSubmitted: () {
                        fieldNextFocus(context, confirmNewPasswordNode, null);
                      }),
                  if (codeSent)
                    ReuseButton(
                      text: ReuseStrings.submit,
                      onPressed: () => handleNewPassword(
                          authCode, email, newPassword, confirmNewPassword),
                      buttonStyle: CustomTheme.primaryButtonStyle(),
                      top: 20.0,
                    ),
                  ReuseErrorMessage(text: errorMessage),
                ],
              ),
            )),
      ),
    );
  }
}
