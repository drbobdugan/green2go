import 'package:Choose2Reuse/components/font_scale_blocker.dart';
import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';
import 'package:flutter/material.dart';

import '../components/reuse_button.dart';
import '../components/reuse_errorMessage.dart';
import '../components/reuse_label.dart';
import '../components/reuse_userBar.dart';
import '../services/api.dart';
import '../services/navigation_service.dart';
import '../services/student_service.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';

class CheckoutContainerPage extends StatefulWidget {
  const CheckoutContainerPage({Key key, @required this.userAuth})
      : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onScanQR(String qrCode) async {
    return await StudentService.checkoutContainer(userAuth, qrCode);
  }

  @override
  _CheckoutContainerPageState createState() => _CheckoutContainerPageState();
}

class _CheckoutContainerPageState extends State<CheckoutContainerPage> {
  String errorMessage = '';

  @override
  Widget build(BuildContext context) {
    return FontScaleBlocker(
      child: Scaffold(
        backgroundColor: Colors.white,
        appBar: UserAppBar(userAuth: widget.userAuth),
        body: Padding(
          padding: const EdgeInsets.all(50.0),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.start,
            crossAxisAlignment: CrossAxisAlignment.stretch,
            children: <Widget>[
              ReuseLabel(
                text: ReuseStrings.scanContainerMessage,
                textStyle: CustomTheme.primaryLabelStyle(),
                bottom: 10.0,
              ),
              ReuseButton(
                text: ReuseStrings.useCamera,
                onPressed: () => scanQRCode(),
                buttonStyle: CustomTheme.primaryButtonStyle(),
                top: 20.0,
              ),
              ReuseErrorMessage(text: errorMessage),
            ],
          ),
        ),
      ),
    );
  }


  Future<void> scanQRCode() async {
    await FlutterBarcodeScanner.scanBarcode(
            '#FF2E856E', ReuseStrings.cancel, false, ScanMode.QR)
        .then((String code) {
      widget.onScanQR(code).then((APIResponse response) {
        if (response.success) {
          NavigationService(context: context).goHome(widget.userAuth);
        } else {
          setState(() {
            errorMessage = response.message;
          });
        }
      });
    });
  }
}
