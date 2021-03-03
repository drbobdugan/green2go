class Student {
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

  Student() {
    email = '';
    password = '';
    firstName = '';
    middleName = '';
    lastName = '';
    classYear = '';
    phoneNum = '';
    role = '';
    authCode = '';
    authToken = '';
  }

  jsonToStudent(json) {
    email = json['email'];
    password = json['password'];
    firstName = json['firstName'];
    middleName = json['middleName'];
    lastName = json['lastName'];
    classYear = json['classYear'];
    phoneNum = json['phoneNum'];
    role = json['role'];
    authCode = json['authCode'];
    authToken = json['auth_token'];
  }
}
