import 'package:http/http.dart';

class API {
  final String baseURL = '198.199.77.174:5000';
  final String localURL = '127.0.0.1:5000';

  Future postResponse(String path, dynamic params) async {
    Response response = await post(
      "http://$localURL/$path",
      headers: <String, String>{
        'Content-Type': 'application/json; charset=UTF-8',
      },
      body: params,
    );
    print(response.body);
    return response.body;
  }

  Future getResponse(String path, String params) async {
    Response response = await get("http://$localURL/$path$params");
    return response.body;
  }
}
