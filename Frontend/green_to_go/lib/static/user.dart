class NewUser {
  String email;
  String password;
  String confirmPassword;
  String firstName;
  String middleName;
  String lastName;
  String classYear;
  String phoneNum;

  NewUser() {
    email = '';
    password = '';
    confirmPassword = '';
    firstName = '';
    middleName = '';
    lastName = '';
    classYear = '';
    phoneNum = '';
  }

  consoleLog() {
    print(
        "email: ${email},\n password: ${password},\n confirmPassword: ${confirmPassword},\n firstName: ${firstName},\n lastName: ${lastName},\n middleName: ${middleName},\n phoneNum: ${phoneNum},\n classYear: ${classYear}");
  }
}

class ExistingUser {
  String email;
  String password;

  ExistingUser() {
    email = '';
    password = '';
  }

  consoleLog() {
    print("email: ${email},\n password: ${password}");
  }
}
