class Container {
  String email;
  String qrCode;
  String status;
  String statusUpdateTime;

  Container(Map<String, dynamic> value) {
    email = value['user'];
    qrCode = value['qrcode'];
    status = value['status'];
    statusUpdateTime = value['statusUpdateTime'];
  }
}
