import 'container.dart';

class StudentAuth {
  String email;
  String authToken;
  String refreshToken;
  String tokenExpiration;

  StudentAuth(Map<String, dynamic> value) {
    email = value['user'];
    authToken = value['auth_token'];
    refreshToken = value['refresh_token'];
    tokenExpiration = value['expires_at'];
  }
}

class StudentDetails {
  String email;
  String password;
  String firstName;
  String middleName;
  String lastName;
  String classYear;
  String phoneNum;
  String role;
  String authCode;
  String authToken;
  String refreshToken;
  String tokenExpiration;
  List<Container> containers;

  StudentDetails([Map<String, dynamic> value]) {
    if (value != null) {
      Map<String, dynamic> user = value['user'];
      List<dynamic> myContainers = value['containers'];
      email = user['email'];
      password = user['password'];
      firstName = user['firstName'];
      middleName = user['middleName'];
      lastName = user['lastName'];
      classYear = user['classYear'];
      phoneNum = user['phoneNum'];
      role = user['role'];
      authCode = user['authCode'];
      containers = new List();
      myContainers.forEach((element) {
        containers.add(Container(element));
      });
    }
  }
}
