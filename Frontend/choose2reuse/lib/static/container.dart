import 'package:intl/intl.dart';

class ReusableContainer {
  ReusableContainer(dynamic value) {
    qrCode = value['qrcode'] as String;
    status = containerDataStrings[value['status'] as String];
    statusUpdateTime = value['statusUpdateTime'] as String;
    statusLocation = value['location_qrcode'] as String;
  }

  String qrCode;
  ContainerStatus status;
  String statusUpdateTime;
  String statusLocation;

  String dataRowText1() {
    return containerLabels[status];
  }

  String dataRowText2() {
    return status == ContainerStatus.CheckedOut
        ? formatDate(statusUpdateTime)
        : '${formatDate(statusUpdateTime)}\n$statusLocation';
  }

  String dataRowText3() {
    return '#$qrCode';
  }

  String dataRowColorID() {
    return containerDataRowColors[status];
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
    pending = getContainerList(value['Pending_Return']);
    verified = getContainerList(value['Verified_Return']);
    damagedLost = getContainerList(value['Damaged_Lost']);
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
  List<ReusableContainer> pending;
  List<ReusableContainer> verified;
  List<ReusableContainer> damagedLost;
}

enum ContainerStatus { CheckedOut, Pending, Verified, DamagedLost }

const List<ContainerStatus> containerIconItems = <ContainerStatus>[
  ContainerStatus.CheckedOut,
  ContainerStatus.Pending,
  ContainerStatus.Verified
];

const Map<String, ContainerStatus> containerDataStrings =
    <String, ContainerStatus>{
  'Checked out': ContainerStatus.CheckedOut,
  'Pending Return': ContainerStatus.Pending,
  'Verified Return': ContainerStatus.Verified,
  'Damaged/Lost': ContainerStatus.DamagedLost
};

const Map<ContainerStatus, String> containerIconColors =
    <ContainerStatus, String>{
  ContainerStatus.CheckedOut: 'light',
  ContainerStatus.Pending: 'primary',
  ContainerStatus.Verified: 'dark',
};

const Map<ContainerStatus, String> containerDataRowColors =
    <ContainerStatus, String>{
  ContainerStatus.CheckedOut: 'attention',
  ContainerStatus.Pending: 'primary',
  ContainerStatus.Verified: 'darkPrimary',
  ContainerStatus.DamagedLost: 'disabled',
};

const Map<ContainerStatus, String> containerLabels = <ContainerStatus, String>{
  ContainerStatus.CheckedOut: 'Checked out',
  ContainerStatus.Pending: 'Pending Return',
  ContainerStatus.Verified: 'Verified Return',
  ContainerStatus.DamagedLost: 'Damaged or Lost'
};
