import 'package:flutter/material.dart';

class ImageBanner extends StatelessWidget {
  final String _path;

  ImageBanner(this._path);

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 30.0, bottom: 20.0),
      child: Container(
        constraints: BoxConstraints.expand(
          height: 175.0,
        ),
        child: Image.asset(
          _path,
          fit: BoxFit.cover,
        ),
      ),
    );
  }
}
