class Student {
  String email;
  String password;
  String firstName;
  String middleName;
  String lastName;
  int classYear;
  String phoneNum;

  Student() {
    email = '';
    password = '';
    firstName = '';
    middleName = '';
    lastName = '';
    classYear = 0;
    phoneNum = '';
  }

  consoleLog() {
    print(
        "email: $email,\n password: $password,\n firstName: $firstName,\n lastName: $lastName,\n middleName: $middleName,\n phoneNum: $phoneNum,\n classYear: $classYear}");
  }
}
