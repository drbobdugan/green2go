import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../pages/login.dart';
import '../pages/checkoutContainer.dart';
import '../pages/returnContainer.dart';
import '../pages/home.dart';
import '../static/student.dart';
import '../components/custom_theme.dart';

class UserAppBar extends StatefulWidget implements PreferredSizeWidget {
  final StudentAuth auth;

  UserAppBar({Key key, this.auth}) : super(key: key);

  @override
  Size get preferredSize => const Size.fromHeight(50);

  @override
  _UserAppBarState createState() => _UserAppBarState();
}

class _UserAppBarState extends State<UserAppBar> {
  Map<String, IconData> icons = {
    'Home': Icons.home,
    'Checkout Container': Icons.rotate_right_rounded,
    'Return Container': Icons.rotate_left_rounded,
    'Logout': Icons.logout
  };

  Future<Null> removeLocalLoginStorage() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('email', null);
    prefs.setString('password', null);
  }

  @override
  Widget build(BuildContext context) {
    return Container(
      child: AppBar(
        title: Text('Choose2Reuse'),
        actions: <Widget>[
          PopupMenuButton(
            icon: Container(
                child: Padding(
                    padding: EdgeInsets.all(3.0),
                    child: Icon(Icons.menu_rounded,
                        size: 24.0,
                        color: CustomTheme.getColor('darkPrimary'))),
                decoration:
                    BoxDecoration(color: Colors.white, shape: BoxShape.circle)),
            onSelected: (choice) {
              switch (choice) {
                case 'Home':
                  Navigator.of(context).popUntil((route) => route.isFirst);
                  Navigator.of(context).pop();
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => new HomePage(userAuth: widget.auth),
                    ),
                  );
                  break;
                case 'Checkout Container':
                  Navigator.of(context).popUntil((route) => route.isFirst);
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => new CheckoutContainerPage(),
                    ),
                  );
                  break;
                case 'Return Container':
                  Navigator.of(context).popUntil((route) => route.isFirst);
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => new ReturnContainerPage(),
                    ),
                  );
                  break;
                case 'Logout':
                  removeLocalLoginStorage();
                  Navigator.of(context).popUntil((route) => route.isFirst);
                  Navigator.of(context).pop();
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => new LoginPage(),
                    ),
                  );
                  break;
                default:
                  break;
              }
            },
            itemBuilder: (BuildContext context) {
              return {
                'Home',
                'Checkout Container',
                'Return Container',
                'Logout'
              }.map((String choice) {
                return PopupMenuItem<String>(
                    value: choice,
                    child: Row(children: <Widget>[
                      Padding(
                          padding: EdgeInsets.only(right: 5.0, bottom: 2.0),
                          child: Icon(icons[choice],
                              size: 24.0,
                              color: CustomTheme.getColor('attention'))),
                      Text(choice,
                          style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: CustomTheme.getColor('darkPrimary')))
                    ]));
              }).toList();
            },
          ),
        ],
      ),
    );
  }
}
