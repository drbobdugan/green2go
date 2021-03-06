class Container {
  Container(Map<String, String> value) {
    email = value['user'];
    qrCode = value['qrcode'];
    status = value['status'];
    statusUpdateTime = value['statusUpdateTime'];
  }

  String email;
  String qrCode;
  String status;
  String statusUpdateTime;
}
