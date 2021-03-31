from authDao import AuthDao

def test_add():
    a = AuthDao()
    dic = {"email" : "patTestUser@students.stonehill.edu",
            "auth_token" : "Ggpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL",
            "refresh_token" : "l9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9"}
    myresult = a.addAuth(dic)
    print(myresult)
    assert myresult[0] == True
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
    dic = {"email" : "patTestUser@students.stonehill.edu",
            "token" : "Ggpmy1lEbwaNoIqZmnjBkkzOtskzYquyL11ISH5ij9iRL",
            "refresh_token" : "l9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9"}
    call = a.updateAuth(dic)
    print("Call of 0",call[0])
    print("Call of 1",call[1])
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