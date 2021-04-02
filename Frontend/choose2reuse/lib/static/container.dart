import 'package:intl/intl.dart';
import '../components/reuse_listItem.dart';

class ReusableContainer {
  ReusableContainer(dynamic value) {
    qrCode = value['qrcode'] as String;
    status = value['status'] as String;
    statusUpdateTime = value['statusUpdateTime'] as String;
    statusLocation = value['location_qrcode'] as String;
  }

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

class SortedReusableContainers {
  SortedReusableContainers(Map<String, dynamic> value) {
    all = getContainerList(value['All']);
    checkedOut = getContainerList(value['Checked_out']);
    verified = getContainerList(value['Verified_Return']);
    pending = getContainerList(value['Pending_Return']);
  }

  static List<ReusableContainer> getContainerList(dynamic value) {
    if (value != null) {
      return (value as List<dynamic>)
          .map((dynamic item) => ReusableContainer(item))
          .toList();
    }
    return <ReusableContainer>[];
  }

  List<ReusableContainer> all;
  List<ReusableContainer> checkedOut;
  List<ReusableContainer> verified;
  List<ReusableContainer> pending;
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
