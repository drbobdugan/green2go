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
