import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';
import 'package:flutter/material.dart';
import 'package:countdown_flutter/countdown_flutter.dart';

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

class ReturnContainerPage extends StatefulWidget {
  const ReturnContainerPage({Key key, @required this.userAuth})
      : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onScanLocationQR(String locationqrCode) async {
    return await StudentService.checkLocation(userAuth, locationqrCode);
  }

  Future<APIResponse> onScanContainerQR(
      String qrCode, String locationqrCode) async {
    return await StudentService.returnContainer(
        userAuth, qrCode, locationqrCode);
  }

  @override
  _ReturnContainerPageState createState() => _ReturnContainerPageState();
}

class _ReturnContainerPageState extends State<ReturnContainerPage> {
  String errorMessage = '';
  bool containerScanActive = false;
  String locationQR = '';

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
                  ? ReuseStrings.scanBeforeTimer
                  : ReuseStrings.scanLocationMessage,
              textStyle: CustomTheme.primaryLabelStyle(),
              isCenter: false,
            ),
            if (containerScanActive)
              CountdownFormatted(
                duration: const Duration(minutes: 5),
                onFinish: () {
                  setState(() {
                    containerScanActive = false;
                    errorMessage = ReuseStrings.timerOutErrorMessage;
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
                  ? ReuseStrings.scanContainerButtonText
                  : ReuseStrings.scanLocationButtonText,
              onPressed: () => containerScanActive
                  ? scanContainerQRCode()
                  : scanLocationQRCode(),
              buttonStyle: CustomTheme.primaryButtonStyle(),
              top: 20.0,
            ),
            ReuseErrorMessage(text: errorMessage),
          ],
        ),
      ),
    );
  }

  Future<void> scanLocationQRCode() async {
    locationQR = await FlutterBarcodeScanner.scanBarcode(
        '#FF2E856E', ReuseStrings.cancel, true, ScanMode.QR);

    widget.onScanLocationQR(locationQR).then((APIResponse response) {
      if (response.success) {
        if (!containerScanActive) {
          setState(() {
            containerScanActive = true;
          });
        }
      } else {
        setState(() {
          errorMessage = response.message;
        });
      }
    });
  }

  Future<void> scanContainerQRCode() async {
    await FlutterBarcodeScanner.scanBarcode(
            '#FF2E856E', ReuseStrings.cancel, true, ScanMode.QR)
        .then((String code) {
      widget.onScanContainerQR(code, locationQR).then((APIResponse response) {
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
