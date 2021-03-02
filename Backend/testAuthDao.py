from authDao import AuthDao

def test_add():
    a = AuthDao()
    assert a.addAuth({"email" : "patTestUser@students.stonehill.edu"})[0] == True, 'Add auth code'
    del a

def get_auth():
    a = AuthDao()
    call = a.getAuth({"email" : "patTestUser@students.stonehill.edu"})
    assert call[0], 'Get auth code'
    del a
    return call[1]

def del_auth():
    a = AuthDao()
    assert a.deleteAuth({"email" : "patTestUser@students.stonehill.edu"})[0], 'Delete auth code'
    del a

def update_auth(t):
    a = AuthDao()
    call = a.updateAuth({"email" : "patTestUser@students.stonehill.edu", "refresh_token" : t})
    assert call[0], 'Get auth code'
    del a
    return call[1]

if __name__ == "__main__":
    test_add()
    token = get_auth()
    token2 = update_auth(token["refresh_token"])
    assert token["auth_token"] != token2["auth_token"], "Update check"
    del_auth()
    print("All tests passed")