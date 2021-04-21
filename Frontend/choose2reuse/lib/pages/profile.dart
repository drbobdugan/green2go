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

class ProfilePage extends StatefulWidget {
  const ProfilePage({Key key, @required this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetUser() async {
    return await UserService.getUser(userAuth);
  }

  Future<APIResponse> onUpdateUser(DetailedUser detailedUser) async {
    return await UserService.updateUser(userAuth, detailedUser);
  }

  @override
  _ProfilePageState createState() => _ProfilePageState();
}

class _ProfilePageState extends State<ProfilePage> {
  final FocusNode firstNameNode = FocusNode();
  final FocusNode middleNameNode = FocusNode();
  final FocusNode lastNameNode = FocusNode();
  final FocusNode emailNode = FocusNode();
  final FocusNode phoneNumNode = FocusNode();

  String errorMessage = '';

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

  void onSaveProfile() {
    widget.onUpdateUser(detailedUser).then((APIResponse response) {
      if (response.success) {
        setState(() {
          detailedUser = DetailedUser(response.data);
          errorMessage = '';
        });
        showSuccess(context);
      } else {
        setState(() {
          errorMessage = response.message;
        });
      }
    });
  }

  void onChangePassword() {
    NavigationService(context: context)
        .goToPage(C2RPages.changePassword, widget.userAuth);
  }

  void onLogOut() {
    NavigationService(context: context).logout();
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
                  text: ReuseStrings.profilePageTitle,
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
                    fieldNextFocus(context, emailNode, firstNameNode);
                  },
                ),
                ReuseTextField(
                  text: ReuseStrings.firstNameField,
                  initialValue: detailedUser.firstName,
                  node: firstNameNode,
                  onChanged: (String value) {
                    setState(() {
                      detailedUser.firstName = value;
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
                    initialValue: detailedUser.middleName,
                    node: middleNameNode,
                    onChanged: (String value) {
                      setState(() {
                        detailedUser.middleName = value;
                      });
                    },
                    autofillHints: const <String>[AutofillHints.middleName],
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, middleNameNode, lastNameNode);
                    }),
                ReuseTextField(
                    text: ReuseStrings.lastNameField,
                    initialValue: detailedUser.lastName,
                    node: lastNameNode,
                    onChanged: (String value) {
                      setState(() {
                        detailedUser.lastName = value;
                      });
                    },
                    autofillHints: const <String>[AutofillHints.familyName],
                    textInputAction: TextInputAction.next,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, lastNameNode, phoneNumNode);
                    }),
                ReuseTextField(
                    text: ReuseStrings.phoneNumberField,
                    initialValue: detailedUser.phoneNum,
                    node: phoneNumNode,
                    onChanged: (String value) {
                      setState(() {
                        detailedUser.phoneNum = value;
                      });
                    },
                    autofillHints: const <String>[
                      AutofillHints.telephoneNumber
                    ],
                    textInputAction: TextInputAction.next,
                    keyboardType: TextInputType.phone,
                    onFieldSubmitted: () {
                      fieldNextFocus(context, phoneNumNode, null);
                    }),
                ReuseButton(
                  text: ReuseStrings.save,
                  onPressed: onSaveProfile,
                  buttonStyle: CustomTheme.primaryButtonStyle(),
                  top: 20.0,
                ),
                ReuseButton(
                  text: ReuseStrings.changePassword,
                  onPressed: onChangePassword,
                  buttonStyle: CustomTheme.primaryButtonStyle(),
                  top: 20.0,
                ),
                ReuseButton(
                  text: ReuseStrings.logOut,
                  onPressed: onLogOut,
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
