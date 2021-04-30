import 'dart:math' as math;
import 'package:flutter/material.dart';

import '../services/navigation_service.dart';
import '../static/custom_theme.dart';
import '../static/student.dart';

enum AppBarItems { Home, Profile, Checkout, Return, Points }

const List<AppBarItems> items = <AppBarItems>[
  AppBarItems.Home,
  AppBarItems.Profile,
  AppBarItems.Checkout,
  AppBarItems.Return,
  AppBarItems.Points
];

const Map<AppBarItems, IconData> icons = <AppBarItems, IconData>{
  AppBarItems.Home: Icons.home,
  AppBarItems.Profile: Icons.account_circle,
  AppBarItems.Checkout: Icons.rotate_right_rounded,
  AppBarItems.Return: Icons.rotate_right_rounded,
  AppBarItems.Points: Icons.stars_rounded
};

const Map<AppBarItems, String> labels = <AppBarItems, String>{
  AppBarItems.Home: 'Dashboard',
  AppBarItems.Profile: 'Profile',
  AppBarItems.Checkout: 'Check Out Container',
  AppBarItems.Return: 'Return Container',
  AppBarItems.Points: 'Points & Rewards'
};

class UserAppBar extends StatefulWidget implements PreferredSizeWidget {
  const UserAppBar({Key key, this.userAuth}) : super(key: key);

  final StudentAuth userAuth;

  @override
  Size get preferredSize => const Size.fromHeight(50);

  @override
  _UserAppBarState createState() => _UserAppBarState();
}

class _UserAppBarState extends State<UserAppBar> {
  void handleSelection(String choice) {
    if (choice == labels[AppBarItems.Home]) {
      NavigationService(context: context).goHome(widget.userAuth);
    } else if (choice == labels[AppBarItems.Checkout]) {
      NavigationService(context: context)
          .goToPage(C2RPages.checkoutContainer, widget.userAuth);
    } else if (choice == labels[AppBarItems.Return]) {
      NavigationService(context: context)
          .goToPage(C2RPages.returnContainer, widget.userAuth);
    } else if (choice == labels[AppBarItems.Profile]) {
      NavigationService(context: context)
          .goToPage(C2RPages.profile, widget.userAuth);
    } else if (choice == labels[AppBarItems.Points]) {
      NavigationService(context: context)
          .goToPage(C2RPages.points, widget.userAuth);
    }
  }

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
          onSelected: handleSelection,
          itemBuilder: (BuildContext context) {
            return items.map((AppBarItems choice) {
              return PopupMenuItem<String>(
                  value: labels[choice],
                  child: Row(children: <Widget>[
                    Padding(
                      padding: const EdgeInsets.only(right: 5.0, bottom: 2.0),
                      child: Transform.rotate(
                          angle: choice == AppBarItems.Checkout
                              ? (180 * math.pi / 180)
                              : 0,
                          child: Icon(icons[choice],
                              size: 24.0,
                              color: CustomTheme.getColor('attention'))),
                    ),
                    Text(labels[choice],
                        textScaleFactor: 1,
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
