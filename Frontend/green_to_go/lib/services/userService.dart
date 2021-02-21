import "package:http/http.dart";

class UserService {
  String baseUrl = "http://198.199.77.174:5000";

  Future getUser(String email) async {
    final data = {'email': email};
    Response response = await post(Uri.https(baseUrl, 'getUser'),
        headers: {"Content-Type": "application/json"}, body: data);

    print(response.body);
    return response.body;
  }
}
