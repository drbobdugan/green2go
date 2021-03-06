import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';
import 'package:flutter/material.dart';

import '../components/custom_theme.dart';
import '../components/reuse_button.dart';
import '../components/reuse_errorMessage.dart';
import '../components/reuse_label.dart';
import '../components/user_appBar.dart';
import '../services/api.dart';
import '../services/navigation_service.dart';
import '../services/student_service.dart';
import '../static/student.dart';

class CheckoutContainerPage extends StatefulWidget {
  const CheckoutContainerPage({Key key, @required this.user}) : super(key: key);

  final StudentDetails user;

  Future<APIResponse> onScanQR(String qrCode) async {
    return await StudentService.addContainer(user, qrCode);
  }

  @override
  _CheckoutContainerPageState createState() => _CheckoutContainerPageState();
}

class _CheckoutContainerPageState extends State<CheckoutContainerPage> {
  String errorMessage = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: UserAppBar(user: widget.user),
      body: Padding(
        padding: const EdgeInsets.all(50.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            ReuseLabel(
              text: 'Please scan the QR code on the container:',
              textStyle: CustomTheme.primaryLabelStyle(),
              bottom: 10.0,
            ),
            ReuseButton(
              text: 'Use Camera',
              onPressed: () => scanQRCode(),
              buttonStyle: CustomTheme.primaryButtonStyle(),
              top: 20.0,
            ),
            ReuseErrorMessage(text: errorMessage),
          ],
        ),
      ),
    );
  }

  Future<void> scanQRCode() async {
    await FlutterBarcodeScanner.scanBarcode(
            '#FF2E856E', 'Cancel', true, ScanMode.QR)
        .then((String code) {
      widget.onScanQR(code).then((APIResponse response) {
        if (response.success) {
          NavigationService(context: context).goHome(widget.user);
        } else {
          setState(() {
            errorMessage = response.message;
          });
        }
      });
    });
  }
}
