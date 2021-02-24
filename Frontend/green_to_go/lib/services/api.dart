import 'package:http/http.dart';

class API {
  Future postResponse(String path, dynamic params) async {
    Response response = await post(
      "http://198.199.77.174:5000/$path",
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: params,
    );
    print(response.body);
    return response.body;
  }

  Future getResponse(String path, String params) async {
    Response response = await get("http://198.199.77.174:5000/$path$params");
    return response.body;
  }
}
