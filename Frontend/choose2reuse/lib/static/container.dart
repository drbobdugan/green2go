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
}
