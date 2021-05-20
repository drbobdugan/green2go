import 'package:Choose2Reuse/components/font_scale_blocker.dart';
import 'package:flutter_barcode_scanner/flutter_barcode_scanner.dart';
import 'package:flutter/material.dart';
import 'package:countdown_flutter/countdown_flutter.dart';
import 'package:shared_preferences/shared_preferences.dart';

import '../components/reuse_button.dart';
import '../components/reuse_errorMessage.dart';
import '../components/reuse_label.dart';
import '../components/reuse_userBar.dart';
import '../services/api.dart';
import '../services/navigation_service.dart';
import '../services/student_service.dart';
import '../static/container.dart';
import '../static/custom_theme.dart';
import '../static/strings.dart';
import '../static/student.dart';

const int initial_timer_seconds = 300;

class NavArguments {
  NavArguments(this.user, this.points, this.earnedBadge);

  final StudentAuth user;
  final int points;
  final bool earnedBadge;
}

class ReturnContainerPage extends StatefulWidget {
  const ReturnContainerPage({Key key, @required this.userAuth})
      : super(key: key);

  final StudentAuth userAuth;

  Future<APIResponse> onGetSortedContainers() async {
    return await StudentService.getSortedContainers(userAuth);
  }

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

class _ReturnContainerPageState extends State<ReturnContainerPage>
    with WidgetsBindingObserver {
  String errorMessage = '';
  bool containerScanActive = false;
  String locationQR = '';
  int secondsRemaining = initial_timer_seconds;
  int points;
  bool earnedBadge;
  StudentDetails user;
  List<ReusableContainer> checkedOut;

  @override
  void initState() {
    super.initState();
    WidgetsBinding.instance.addObserver(this);

    autoCheckTimeRemaining();
  }

  @override
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);

    super.dispose();
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      autoCheckTimeRemaining();
    }
  }

  void resetTimer(bool showMessage) async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    prefs.setString('returnContainerStartTime', null);

    setState(() {
      containerScanActive = false;
      secondsRemaining = initial_timer_seconds;
      if (showMessage) {
        errorMessage = ReuseStrings.timerOutErrorMessage;
      }
    });
  }

  void autoCheckTimeRemaining() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    final String startTime = prefs.getString('returnContainerStartTime');

    if (startTime != null) {
      final DateTime parsed = DateTime.parse(startTime);
      final DateTime invalidAt =
          parsed.add(const Duration(seconds: initial_timer_seconds));
      if (DateTime.now().isAfter(invalidAt)) {
        resetTimer(false);
      } else {
        setState(() {
          secondsRemaining = initial_timer_seconds -
              DateTime.now().difference(parsed).inSeconds;
          containerScanActive = true;
        });
      }
    }
  }

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
                text: containerScanActive
                    ? ReuseStrings.scanBeforeTimer
                    : ReuseStrings.scanLocationMessage,
                textStyle: CustomTheme.primaryLabelStyle(),
                isCenter: false,
              ),
              if (containerScanActive)
                CountdownFormatted(
                  duration: Duration(seconds: secondsRemaining),
                  onFinish: () {
                    resetTimer(true);
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
              if (containerScanActive)
                ReuseButton(
                  text: ReuseStrings.resetReturnButtonText,
                  onPressed: () {
                    resetTimer(false);
                  },
                  buttonStyle: CustomTheme.primaryButtonStyle(),
                  top: 20.0,
                )
            ],
          ),
        ),
      ),
    );
  }

  void testMethod() {
    points = 5;
    earnedBadge = true;

    NavigationService(context: context).goToPage(C2RPages.returnConfirmation,
        NavArguments(widget.userAuth, points, earnedBadge));
  }

  Future<void> scanLocationQRCode() async {
    final SharedPreferences prefs = await SharedPreferences.getInstance();
    locationQR = await FlutterBarcodeScanner.scanBarcode(
        '#FF2E856E', ReuseStrings.cancel, false, ScanMode.QR);

    widget.onScanLocationQR(locationQR).then((APIResponse response) {
      if (response.success) {
        if (!containerScanActive) {
          setState(() {
            containerScanActive = true;
          });
          prefs.setString(
              'returnContainerStartTime', DateTime.now().toString());
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
            '#FF2E856E', ReuseStrings.cancel, false, ScanMode.QR)
        .then((String code) {
      widget.onScanContainerQR(code, locationQR).then((APIResponse response) {
        if (response.success) {
          if (response.data ==
              '') //data will be empty if user is returning someone else's container
          {
            NavigationService(context: context).goHome(widget.userAuth);
          } else {
            final Map<String, dynamic> data =
                response.data as Map<String, dynamic>;
            points = data['points'] as int;
            earnedBadge = data['newReward'] as bool;
            NavigationService(context: context).goToPage(
                C2RPages.returnConfirmation,
                NavArguments(widget.userAuth, points, earnedBadge));
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
