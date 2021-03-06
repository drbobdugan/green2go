import 'container.dart';

class StudentAuth {
  StudentAuth(Map<String, dynamic> value) {
    email = value['user'] as String;
    token = value['auth_token'] as String;
    refresh = value['refresh_token'] as String;
    expiration = value['expires_at'] as String;
  }

  String email;
  String token;
  String refresh;
  String expiration;
}

class StudentDetails {
  StudentDetails(Map<String, dynamic> value, this.auth) {
    if (value != null) {
      final Map<String, String> user = value['user'] as Map<String, String>;
      email = user['email'];
      password = user['password'];
      firstName = user['firstName'];
      middleName = user['middleName'];
      lastName = user['lastName'];
      classYear = user['classYear'];
      phoneNum = user['phoneNum'];
      role = user['role'];

      final List<Map<String, String>> myContainers =
          value['containers'] as List<Map<String, String>>;
      for (final Map<String, String> element in myContainers) {
        containers.add(Container(element));
      }
    }
  }

  String email;
  String password;
  String firstName;
  String middleName;
  String lastName;
  String classYear;
  String phoneNum;
  String role;
  StudentAuth auth;
  List<Container> containers;
}
