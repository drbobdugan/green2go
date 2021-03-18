import 'package:intl/intl.dart';
import '../components/reuse_listItem.dart';

class ReusableContainer {
  ReusableContainer(dynamic value) {
    email = value['user'] as String;
    qrCode = value['qrcode'] as String;
    status = value['status'] as String;
    statusUpdateTime = value['statusUpdateTime'] as String;
    statusLocation = value['location_qrcode'] as String;
  }

  String email;
  String qrCode;
  String status;
  String statusUpdateTime;
  String statusLocation;

  ListItem dataRow() {
    return ListItem(
      text1: status,
      text3: '#$qrCode',
      text2: status == 'Checked out'
          ? formatDate(statusUpdateTime)
          : '${formatDate(statusUpdateTime)}\n$statusLocation',
      colorID: status.contains('Checked')
          ? 'attention'
          : (status.contains('Pending') ? 'primary' : 'darkPrimary'),
    );
  }

  String formatDate(String date) {
    final DateTime inputDate = DateFormat('yyyy-MM-dd HH:mm:ss').parse(date);
    return DateFormat('MM/dd/yyyy hh:mm a').format(inputDate);
  }
}

enum ContainerStatus { CheckedOut, Verified, Unverified }

const List<ContainerStatus> containerItems = <ContainerStatus>[
  ContainerStatus.CheckedOut,
  ContainerStatus.Verified,
  ContainerStatus.Unverified,
];

const Map<ContainerStatus, String> containerIconColors =
    <ContainerStatus, String>{
  ContainerStatus.CheckedOut: 'light',
  ContainerStatus.Verified: 'primary',
  ContainerStatus.Unverified: 'dark',
};

const Map<ContainerStatus, String> containerLabels = <ContainerStatus, String>{
  ContainerStatus.CheckedOut: 'Checked out',
  ContainerStatus.Verified: 'Pending Return',
  ContainerStatus.Unverified: 'Verified Return',
};
