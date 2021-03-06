import 'package:Choose2Reuse/services/navigation_service.dart';
import 'package:flutter/material.dart';

import '../components/custom_theme.dart';
import '../static/student.dart';

class UserAppBar extends StatefulWidget implements PreferredSizeWidget {
  const UserAppBar({Key key, this.user}) : super(key: key);

  final StudentDetails user;

  @override
  Size get preferredSize => const Size.fromHeight(50);

  @override
  _UserAppBarState createState() => _UserAppBarState();
}

class _UserAppBarState extends State<UserAppBar> {
  Map<String, IconData> icons = <String, IconData>{
    'Home': Icons.home,
    'Checkout Container': Icons.rotate_right_rounded,
    'Return Container': Icons.rotate_left_rounded,
    'Logout': Icons.logout
  };

  void navigateTo(BuildContext context, String path) {}

  @override
  Widget build(BuildContext context) {
    return AppBar(
      title: const Text('Choose2Reuse'),
      actions: <Widget>[
        PopupMenuButton<String>(
          icon: Container(
              child: Padding(
                  padding: const EdgeInsets.all(3.0),
                  child: Icon(Icons.menu_rounded,
                      size: 24.0, color: CustomTheme.getColor('darkPrimary'))),
              decoration: const BoxDecoration(
                  color: Colors.white, shape: BoxShape.circle)),
          onSelected: (String choice) {
            switch (choice) {
              case 'Home':
                NavigationService(context: context).goHome(widget.user);
                break;
              case 'Checkout Container':
                NavigationService(context: context)
                    .goToPage(C2RPages.checkoutContainer, widget.user);
                break;
              case 'Return Container':
                NavigationService(context: context)
                    .goToPage(C2RPages.returnContainer, widget.user);
                break;
              case 'Logout':
                NavigationService(context: context).logout();
                break;
              default:
                break;
            }
          },
          itemBuilder: (BuildContext context) {
            return <String>{
              'Home',
              'Checkout Container',
              'Return Container',
              'Logout'
            }.map((String choice) {
              return PopupMenuItem<String>(
                  value: choice,
                  child: Row(children: <Widget>[
                    Padding(
                        padding: const EdgeInsets.only(right: 5.0, bottom: 2.0),
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
    );
  }
}
