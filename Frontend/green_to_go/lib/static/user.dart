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

  NewUser() {}

  consoleLog() {
    print(
        "email: ${email},\n password: ${password},\n email: ${email},\n email: ${email},\n email: ${email},\n email: ${email},\n email: ${email},\n email: ${email},\n email: ${email}");
  }
}

class ExistingUser {
  String email;
  String password;

  ExistingUser() {}
}
