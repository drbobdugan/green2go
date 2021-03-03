import 'package:Choose2Reuse/components/cool_label.dart';
import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';
import 'package:flutter/material.dart';

import '../components/cool_button.dart';
import '../components/custom_theme.dart';
import '../components/cool_errorMessage.dart';
import '../components/user_appBar.dart';
import '../services/api.dart';
import '../services/student_service.dart';
import '../static/student.dart';
import '../pages/home.dart';

class CheckoutContainerPage extends StatefulWidget {
  CheckoutContainerPage({Key key}) : super(key: key);

  final _studentService = StudentService();
  Future<APIResponse> onScanQR(user, qrCode) async {
    return await _studentService.addContainer(user, qrCode);
  }

  @override
  _CheckoutContainerPageState createState() => _CheckoutContainerPageState();
}

class _CheckoutContainerPageState extends State<CheckoutContainerPage> {
  final Student user = new Student();
  String errorMessage = '';

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: Colors.white,
      appBar: UserAppBar(),
      body: Padding(
        padding: const EdgeInsets.all(50.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: [
            CoolLabel(
              text: "Please scan the QR code on the container:",
              textStyle: CustomTheme.primaryLabelStyle(),
              bottom: 10.0,
            ),
            CoolButton(
              text: "Use Camera",
              onPressed: () => scanQRCode(),
              buttonStyle: CustomTheme.primaryButtonStyle(),
              top: 20.0,
            ),
            CoolErrorMessage(text: errorMessage),
          ],
        ),
      ),
    );
  }

  Future<void> scanQRCode() async {
    await FlutterBarcodeScanner.scanBarcode(
            '#FF2E856E', 'Cancel', true, ScanMode.QR)
        .then((code) {
      widget.onScanQR(user, code).then((response) {
        if (response.success) {
          Navigator.of(context).push(
            MaterialPageRoute(
              builder: (context) => new HomePage(),
            ),
          );
        } else {
          setState(() {
            errorMessage = response.message;
          });
        }
      });
    });
  }
}
