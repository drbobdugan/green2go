import 'package:flutter/material.dart';

class ImageBanner extends StatelessWidget {
  final String _path;

  ImageBanner(this._path);

  @override
  Widget build(BuildContext context) {
    return Container(
        constraints: BoxConstraints.expand(
          height: 150.0,
        ),
        child: Image.asset(
          _path,
          fit: BoxFit.cover,
        ));
  }
}
