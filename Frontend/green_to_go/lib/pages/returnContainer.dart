import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';
import 'package:flutter/material.dart';
import 'package:countdown_flutter/countdown_flutter.dart';

import '../components/reuse_label.dart';
import '../components/custom_theme.dart';
import '../components/reuse_button.dart';
import '../components/reuse_errorMessage.dart';
import '../components/user_appBar.dart';
import '../services/api.dart';
import '../services/student_service.dart';
import '../static/student.dart';
import '../pages/home.dart';

class ReturnContainerPage extends StatefulWidget {
  final StudentDetails user;

  ReturnContainerPage({Key key, this.user}) : super(key: key);

  final _studentService = StudentService();
  Future<APIResponse> onScanQR(qrCode) async {
    return await _studentService.addContainer(user, qrCode);
  }

  @override
  _ReturnContainerPageState createState() => _ReturnContainerPageState();
}

class _ReturnContainerPageState extends State<ReturnContainerPage> {
  String errorMessage = '';
  bool containerScanActive = false;

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
            ReuseLabel(
              text: (containerScanActive)
                  ? "Please scan the QR code on the container before the timer runs out:"
                  : "Please scan the QR code at the drop-off location. Here is a sample QR code:",
              textStyle: CustomTheme.primaryLabelStyle(),
              isCenter: false,
            ),
            if (containerScanActive)
              CountdownFormatted(
                duration: Duration(minutes: 5),
                onFinish: () {
                  setState(() {
                    containerScanActive = false;
                    errorMessage = "Timer has ran out.";
                  });
                },
                builder: (BuildContext ctx, String remaining) {
                  return ReuseLabel(
                    text: remaining,
                    textStyle: CustomTheme.primaryLabelStyle(fontSize: 35),
                    top: 25,
                    bottom: 15,
                  );
                },
              ),
            if (!containerScanActive)
              Image(
                image: AssetImage("assets/images/sample_qr_code.png"),
              ),
            ReuseButton(
              text: (containerScanActive)
                  ? "Scan container QR code"
                  : "Scan location QR code",
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
        .then((code) {
      widget.onScanQR(code).then((response) {
        if (response.success) {
          if (!containerScanActive) {
            setState(() {
              containerScanActive = true;
            });
          } else {
            Navigator.of(context).push(
              MaterialPageRoute(
                builder: (context) => new HomePage(),
              ),
            );
          }
        } else {
          setState(() {
            errorMessage = response.message;
          });
        }
      });
    });
  }
}
