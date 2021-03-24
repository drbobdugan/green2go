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

class SignUpPage extends StatefulWidget {
  const SignUpPage({Key key}) : super(key: key);

  Future<APIResponse> onSignUp(NewUser user) async {
    return await UserService.signUp(user);
  }

  @override
  _SignUpPageState createState() => _SignUpPageState();
}

class _SignUpPageState extends State<SignUpPage> {
  final FocusNode firstNameNode = FocusNode();
  final FocusNode middleNameNode = FocusNode();
  final FocusNode lastNameNode = FocusNode();
  final FocusNode emailNode = FocusNode();
  final FocusNode phoneNumNode = FocusNode();
  final FocusNode classYearNode = FocusNode();
  final FocusNode passwordNode = FocusNode();
  final FocusNode confirmPasswordNode = FocusNode();

  NewUser user = NewUser();
  String errorMessage = '';

  void handleSignUp(BuildContext context) {
    widget.onSignUp(user).then((APIResponse response) {
      print(response.data);
      if (response.success) {
        NavigationService(context: context).goToPage(C2RPages.validation, user);
      } else {
        setState(() {
          errorMessage = response.message;
        });
      }
    });
  }

  void handleValidation(BuildContext context) {
    NavigationService(context: context).goToPage(C2RPages.validation, user);
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
    return Scaffold(
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
            padding: const EdgeInsets.only(top: 30.0, left: 50.0, right: 50.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: <Widget>[
                ReuseLabel(
                  text: ReuseStrings.signUpPageTitle,
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
                    }),
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
                    node: emailNode,
                    onChanged: (String value) {
                      setState(() {
                        user.email = value;
                      });
                    },
                    autofillHints: const <String>[AutofillHints.email],
                    textInputAction: TextInputAction.next,
                    keyboardType: TextInputType.emailAddress,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, emailNode, phoneNumNode);
                    }),
                ReuseTextField(
                    text: ReuseStrings.phoneNumberField,
                    node: phoneNumNode,
                    onChanged: (String value) {
                      setState(() {
                        user.phoneNum = value;
                      });
                    },
                    autofillHints: const <String>[
                      AutofillHints.telephoneNumber
                    ],
                    textInputAction: TextInputAction.next,
                    keyboardType: TextInputType.phone,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, phoneNumNode, classYearNode);
                    }),
                ReuseTextField(
                    text: ReuseStrings.classYearField,
                    node: classYearNode,
                    onChanged: (String value) {
                      setState(() {
                        user.classYear = value;
                      });
                    },
                    keyboardType: TextInputType.number,
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, classYearNode, passwordNode);
                    }),
                ReuseTextField(
                    text: ReuseStrings.passwordField,
                    node: passwordNode,
                    obscureText: true,
                    onChanged: (String value) {
                      setState(() {
                        user.password = value;
                      });
                    },
                    autofillHints: const <String>[AutofillHints.password],
                    keyboardType: TextInputType.visiblePassword,
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: () {
                      fieldNextFocus(
                          context, passwordNode, confirmPasswordNode);
                    }),
                ReuseTextField(
                    text: ReuseStrings.confirmPasswordField,
                    node: confirmPasswordNode,
                    obscureText: true,
                    onChanged: (String value) {
                      setState(() {
                        user.confirmPassword = value;
                      });
                    },
                    autofillHints: const <String>[AutofillHints.password],
                    keyboardType: TextInputType.visiblePassword,
                    textInputAction: TextInputAction.done,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, confirmPasswordNode, null);
                    }),
                ReuseButton(
                  text: ReuseStrings.signUpButtonText,
                  onPressed: () => handleSignUp(context),
                  buttonStyle: CustomTheme.primaryButtonStyle(),
                  top: 20.0,
                ),
                ReuseButton(
                  text: ReuseStrings.goToValidationPageText,
                  onPressed: () => handleValidation(context),
                  buttonType: 'text',
                ),
                ReuseErrorMessage(text: errorMessage),
              ],
            ),
          )),
    );
  }
}
