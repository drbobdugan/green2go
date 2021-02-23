class NewUser {
  String email;
  String password;
  String confirmPassword;
  String firstName;
  String middleName;
  String lastName;
  int classYear;
  String phoneNum;
  int authCode;

  NewUser() {
    email = '';
    password = '';
    confirmPassword = '';
    firstName = '';
    middleName = '';
    lastName = '';
    classYear = 0;
    phoneNum = '';
    authCode = 0;
  }

  consoleLog() {
    print(
        "email: ${email},\n password: ${password},\n confirmPassword: ${confirmPassword},\n firstName: ${firstName},\n lastName: ${lastName},\n middleName: ${middleName},\n phoneNum: ${phoneNum},\n classYear: ${classYear},\n authCode: ${authCode}");
  }
}

class ExistingUser {
  String email;
  String password;

  ExistingUser() {}
}
