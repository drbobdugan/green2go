import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';
import 'package:flutter/material.dart';
import 'package:countdown_flutter/countdown_flutter.dart';

import '../components/custom_theme.dart';
import '../components/reuse_button.dart';
import '../components/reuse_errorMessage.dart';
import '../components/reuse_label.dart';
import '../components/reuse_strings.dart';
import '../components/user_appBar.dart';
import '../services/api.dart';
import '../services/navigation_service.dart';
import '../services/student_service.dart';
import '../static/student.dart';

class ReturnContainerPage extends StatefulWidget {
  const ReturnContainerPage({Key key, @required this.userAuth})
      : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onScanQR(String qrCode) async {
    return await StudentService.returnContainer(userAuth, qrCode);
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
      appBar: UserAppBar(userAuth: widget.userAuth),
      body: Padding(
        padding: const EdgeInsets.all(50.0),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.start,
          crossAxisAlignment: CrossAxisAlignment.stretch,
          children: <Widget>[
            ReuseLabel(
              text: containerScanActive
                  ? ReuseStrings.scanBeforeTimer()
                  : ReuseStrings.scanLocationMessage(),
              textStyle: CustomTheme.primaryLabelStyle(),
              isCenter: false,
            ),
            if (containerScanActive)
              CountdownFormatted(
                duration: const Duration(minutes: 5),
                onFinish: () {
                  setState(() {
                    containerScanActive = false;
                    errorMessage = ReuseStrings.timerOutErrorMessage();
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
              const Image(
                image: AssetImage('assets/images/sample_qr_code.png'),
              ),
            ReuseButton(
              text: containerScanActive
                  ? ReuseStrings.scanContainerButtonText()
                  : ReuseStrings.scanLocationButtonText(),
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
            '#FF2E856E', ReuseStrings.cancel(), true, ScanMode.QR)
        .then((String code) {
      widget.onScanQR(code).then((APIResponse response) {
        if (response.success) {
          if (!containerScanActive) {
            setState(() {
              containerScanActive = true;
            });
          } else {
            NavigationService(context: context).goHome(widget.userAuth);
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
