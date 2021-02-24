import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';
import 'package:flutter/material.dart';

import '../components/user_appBar.dart';
import '../services/student_service.dart';
import '../static/student.dart';

class CheckoutPage extends StatefulWidget {
  CheckoutPage({Key key}) : super(key: key);

  final _studentService = StudentService();
  Future<bool> onScanQR(user, qrCode) async {
    return await _studentService.addContainer(user, qrCode);
  }

  @override
  _CheckoutPageState createState() => _CheckoutPageState();
}

class _CheckoutPageState extends State<CheckoutPage> {
  final Student user = new Student();

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
                Padding(
                  padding: const EdgeInsets.only(bottom: 10.0),
                  child: Text("Checkout a container here...",
                      textAlign: TextAlign.center,
                      style: TextStyle(
                          fontWeight: FontWeight.bold, fontSize: 20.0)),
                ),
                Padding(
                    padding: const EdgeInsets.only(top: 20.0),
                    child: ElevatedButton(
                      child: Text('Scan QR Code'),
                      onPressed: () => scanQRCode(),
                    )),
              ],
            )));
  }

  Future<void> scanQRCode() async {
    String qrCode = await FlutterBarcodeScanner.scanBarcode(
        '#FF2E856E', 'Cancel', true, ScanMode.QR);
    print(qrCode);
    widget.onScanQR(user, qrCode);
  }
}
