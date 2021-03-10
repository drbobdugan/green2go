import 'package:flutter/material.dart';

class ImageBanner extends StatelessWidget {
  const ImageBanner({Key key, this.path}) : super(key: key);

  final String path;

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.only(top: 30.0, bottom: 20.0),
      child: Container(
        constraints: const BoxConstraints.expand(
          height: 175.0,
        ),
        child: Image.asset(
          path,
          fit: BoxFit.cover,
        ),
      ),
    );
  }
}
