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

class ChangePasswordPage extends StatefulWidget {
  const ChangePasswordPage({Key key, @required this.userAuth})
      : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onChangePassword(String oldPass, String newPass) async {
    return await UserService.changePassword(userAuth, oldPass, newPass);
  }

  @override
  _ChangePasswordPageState createState() => _ChangePasswordPageState();
}

class _ChangePasswordPageState extends State<ChangePasswordPage> {
  final FocusNode currentPasswordNode = FocusNode();
  final FocusNode newPasswordNode = FocusNode();
  final FocusNode confirmNewPasswordNode = FocusNode();

  String currentPassword;
  String newPassword;
  String confirmNewPassword;
  String errorMessage = '';

  @override
  void initState() {
    super.initState();
  }

  void fieldNextFocus(
      BuildContext context, FocusNode currentFocus, FocusNode nextFocus) {
    currentFocus.unfocus();
    if (nextFocus != null) {
      FocusScope.of(context).requestFocus(nextFocus);
    }
  }

  void showSuccess(BuildContext context) {
    ScaffoldMessenger.of(context)
        .showSnackBar(SnackBar(content: Text(ReuseStrings.changePassSuccess)));
  }

  void onChangePassword() {
    if (newPassword == confirmNewPassword) {
      widget
          .onChangePassword(currentPassword, newPassword)
          .then((APIResponse response) {
        if (response.success) {
          setState(() {
            errorMessage = '';
          });
          showSuccess(context);
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
                  text: ReuseStrings.changePasswordPageTitle,
                  textStyle: CustomTheme.primaryLabelStyle(),
                  bottom: 20.0,
                ),
                ReuseTextField(
                  text: ReuseStrings.currentPasswordField,
                  node: currentPasswordNode,
                  obscureText: true,
                  onChanged: (String value) {
                    setState(() {
                      currentPassword = value;
                    });
                  },
                  textInputAction: TextInputAction.next,
                  onFieldSubmitted: () {
                    fieldNextFocus(
                        context, currentPasswordNode, newPasswordNode);
                  },
                ),
                ReuseTextField(
                    text: ReuseStrings.newPasswordField,
                    node: newPasswordNode,
                    obscureText: true,
                    onChanged: (String value) {
                      setState(() {
                        newPassword = value;
                      });
                    },
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: () {
                      fieldNextFocus(
                          context, newPasswordNode, confirmNewPasswordNode);
                    }),
                ReuseTextField(
                    text: ReuseStrings.confirmNewPasswordField,
                    node: confirmNewPasswordNode,
                    obscureText: true,
                    onChanged: (String value) {
                      setState(() {
                        confirmNewPassword = value;
                      });
                    },
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, confirmNewPasswordNode, null);
                    }),
                ReuseButton(
                  text: ReuseStrings.changePassword,
                  onPressed: onChangePassword,
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
