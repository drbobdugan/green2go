import 'package:flutter/material.dart';

import '../pages/login.dart';
import '../pages/checkout.dart';

class UserAppBar extends StatelessWidget implements PreferredSizeWidget {
  @override
  Size get preferredSize => const Size.fromHeight(50);

  @override
  Widget build(BuildContext context) {
    return Container(
      child: AppBar(
        title: Text('Green2Go'),
        actions: <Widget>[
          PopupMenuButton(
            onSelected: (choice) {
              switch (choice) {
                case 'Checkout Container':
                  Navigator.of(context).popUntil((route) => route.isFirst);
                  Navigator.of(context).push(
                    MaterialPageRoute(
                      builder: (context) => new CheckoutPage(),
                    ),
                  );
                  break;
                case 'Logout':
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
              return {'Checkout Container', 'Logout'}.map((String choice) {
                return PopupMenuItem<String>(
                  value: choice,
                  child: Text(choice),
                );
              }).toList();
            },
          ),
        ],
      ),
    );
  }
}
