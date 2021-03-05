import 'package:flutter/material.dart';

import '../components/reuse_button.dart';
import '../components/custom_theme.dart';
import '../components/reuse_textField.dart';
import '../components/reuse_errorMessage.dart';
import '../components/reuse_label.dart';
import '../static/user.dart';
import '../services/api.dart';
import '../services/user_service.dart';
import 'validation.dart';

class SignUpPage extends StatefulWidget {
  SignUpPage({Key key}) : super(key: key);

  final _userService = UserService();
  Future<APIResponse> onSignUp(user) async {
    return await _userService.signUp(user);
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

  NewUser user = new NewUser();
  String errorMessage = '';

  void handleSignUp(BuildContext context) {
    widget.onSignUp(user).then((response) {
      if (response.success) {
        Navigator.of(context).push(MaterialPageRoute(
            builder: (context) => new ValidationPage(user: user)));
      } else {
        setState(() {
          errorMessage = response.message;
        });
      }
    });
  }

  void handleValidation(BuildContext context) {
    Navigator.of(context).push(MaterialPageRoute(
        builder: (context) => new ValidationPage(user: user)));
  }

  fieldNextFocus(
      BuildContext context, FocusNode currentFocus, FocusNode nextFocus) {
    currentFocus.unfocus();
    if (nextFocus != null) FocusScope.of(context).requestFocus(nextFocus);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      resizeToAvoidBottomPadding: false,
      resizeToAvoidBottomInset: true,
      appBar: AppBar(
        title: Text('Choose2Reuse'),
      ),
      body: GestureDetector(
          onTap: () {
            FocusScopeNode currentFocus = FocusScope.of(context);

            if (!currentFocus.hasPrimaryFocus) {
              currentFocus.unfocus();
            }
          },
          child: SingleChildScrollView(
            padding: const EdgeInsets.only(top: 30.0, left: 50.0, right: 50.0),
            child: Column(
              mainAxisAlignment: MainAxisAlignment.start,
              crossAxisAlignment: CrossAxisAlignment.stretch,
              children: [
                ReuseLabel(
                  text: "Sign Up",
                  textStyle: CustomTheme.primaryLabelStyle(),
                  bottom: 20.0,
                ),
                ReuseTextField(
                    text: "First Name",
                    node: firstNameNode,
                    onChanged: (value) {
                      setState(() {
                        user.firstName = value;
                      });
                    },
                    autofillHints: [AutofillHints.givenName],
                    textInputAction: TextInputAction.next,
                    keyboardType: TextInputType.name,
                    onFieldSubmitted: (value) {
                      fieldNextFocus(context, firstNameNode, middleNameNode);
                    }),
                ReuseTextField(
                    text: "Middle Name",
                    node: middleNameNode,
                    onChanged: (value) {
                      setState(() {
                        user.middleName = value;
                      });
                    },
                    autofillHints: [AutofillHints.middleName],
                    textInputAction: TextInputAction.next,
                    keyboardType: TextInputType.name,
                    onFieldSubmitted: (value) {
                      fieldNextFocus(context, middleNameNode, lastNameNode);
                    }),
                ReuseTextField(
                    text: "Last Name",
                    node: lastNameNode,
                    onChanged: (value) {
                      setState(() {
                        user.lastName = value;
                      });
                    },
                    autofillHints: [AutofillHints.familyName],
                    textInputAction: TextInputAction.next,
                    keyboardType: TextInputType.name,
                    onFieldSubmitted: (value) {
                      fieldNextFocus(context, lastNameNode, emailNode);
                    }),
                ReuseTextField(
                    text: "Email",
                    node: emailNode,
                    onChanged: (value) {
                      setState(() {
                        user.email = value;
                      });
                    },
                    autofillHints: [AutofillHints.email],
                    textInputAction: TextInputAction.next,
                    keyboardType: TextInputType.emailAddress,
                    onFieldSubmitted: (value) {
                      fieldNextFocus(context, emailNode, phoneNumNode);
                    }),
                ReuseTextField(
                    text: "Phone Number",
                    node: phoneNumNode,
                    onChanged: (value) {
                      setState(() {
                        user.phoneNum = value;
                      });
                    },
                    autofillHints: [AutofillHints.telephoneNumber],
                    textInputAction: TextInputAction.next,
                    keyboardType: TextInputType.phone,
                    onFieldSubmitted: (value) {
                      fieldNextFocus(context, phoneNumNode, classYearNode);
                    }),
                ReuseTextField(
                    text: "Class Year",
                    node: classYearNode,
                    onChanged: (value) {
                      setState(() {
                        user.classYear = value;
                      });
                    },
                    keyboardType: TextInputType.number,
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: (value) {
                      fieldNextFocus(context, classYearNode, passwordNode);
                    }),
                ReuseTextField(
                    text: "Password",
                    node: passwordNode,
                    obscureText: true,
                    onChanged: (value) {
                      setState(() {
                        user.password = value;
                      });
                    },
                    autofillHints: [AutofillHints.password],
                    keyboardType: TextInputType.visiblePassword,
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: (value) {
                      fieldNextFocus(
                          context, passwordNode, confirmPasswordNode);
                    }),
                ReuseTextField(
                    text: "Confirm Password",
                    node: confirmPasswordNode,
                    obscureText: true,
                    onChanged: (value) {
                      setState(() {
                        user.confirmPassword = value;
                      });
                    },
                    autofillHints: [AutofillHints.password],
                    keyboardType: TextInputType.visiblePassword,
                    textInputAction: TextInputAction.done,
                    onFieldSubmitted: (value) {
                      fieldNextFocus(context, confirmPasswordNode, null);
                    }),
                ReuseButton(
                  text: "Sign Up",
                  onPressed: () => handleSignUp(context),
                  buttonStyle: CustomTheme.primaryButtonStyle(),
                  top: 20.0,
                ),
                ReuseButton(
                  text: "Have a verification code? Enter it here!",
                  onPressed: () => handleValidation(context),
                  buttonType: "text",
                ),
                ReuseErrorMessage(text: errorMessage),
              ],
            ),
          )),
    );
  }
}
