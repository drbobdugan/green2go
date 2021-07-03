class NewUser {
  NewUser() {
    email = '';
    password = '';
    confirmPassword = '';
    firstName = '';
    middleName = '';
    lastName = '';
    phoneNum = '';
  }

  String email;
  String password;
  String confirmPassword;
  String firstName;
  String middleName;
  String lastName;
  String phoneNum;
}

class ExistingUser {
  ExistingUser() {
    email = '';
    password = '';
  }

  String email;
  String password;
}

class DetailedUser {
  DetailedUser(dynamic value) {
    email = value['email'] as String;
    firstName = value['firstName'] as String;
    middleName = value['middleName'] as String;
    lastName = value['lastName'] as String;
    phoneNum = value['phoneNum'] as String;
    password = value['password'] as String;
    points = value['points'] as int;
    badges = value['badges'] as int;
  }

  String email;
  String firstName;
  String middleName;
  String lastName;
  String phoneNum;
  String password;
  int points;
  int badges;
}
