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

  StudentDetails(Map<String, dynamic> value) {
    email = value['email'];
    password = value['password'];
    firstName = value['firstName'];
    middleName = value['middleName'];
    lastName = value['lastName'];
    classYear = value['classYear'];
    phoneNum = value['phoneNum'];
    role = value['role'];
    authCode = value['authCode'];
  }
}
