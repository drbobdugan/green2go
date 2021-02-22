import 'package:http/http.dart';

class UserService {
  Future postResponse(String path, dynamic params) async {
    Response response = await post(
      "http://198.199.77.174:5000/${path}",
      body: params,
    );
    return response.body;
  }

  dynamic signUp(dynamic params) async {
    return await postResponse("addUser", params);
  }

  dynamic signIn(dynamic params) async {
    return await postResponse("getUser", params);
  }

  dynamic sendCode(dynamic params) async {
    return null;
  }
}
