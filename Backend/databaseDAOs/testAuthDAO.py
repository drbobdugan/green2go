from auth import Auth
from authDAO import AuthDao
dao = AuthDao()

def main():
    """
    Uncomment the desired method to test it
    """
    #testinsertAuth()
    testSelectByEmail()  
    #testUpdateAuth()
    #testDeleteAuth()

def testinsertAuth():
    #auth 1
    auth = Auth("auth1TestUser@students.stonehill.edu","Ggpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","l9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
    #dao.insertAuth(auth)
    #auth 2
    auth = Auth("auth2TestUser@students.stonehill.edu","Zgpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","Z9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
    #dao.insertAuth(auth)
    #auth 3
    auth = Auth("auth3estUser@students.stonehill.edu","Tgpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","T9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
    dao.insertAuth(auth)

def testSelectByEmail():
    #auth 1
    email = "auth1TestUser@students.stonehill.edu"
    print(dao.selectByEmail(email)) #returns specific location object selected by location_qrcode
    #auth 2
    email = "auth2TestUser@students.stonehill.edu"
    print(dao.selectByEmail(email))

def testUpdateAuth():
    auth = Auth("auth1TestUser@students.stonehill.edu","Rgpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","l9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
    print(dao.updateAuth(auth))

def testDeleteAuth():
    auth = Auth("auth1TestUser@students.stonehill.edu","Ggpmy1lEbwaNoIqZmkjBkkzOtskzYquyL11ISH5ij9iRL","l9R51hFTGUgV0LeyJJAkwbSiZL1dfennuGDlPcUJnnNm9","2021-01-01 01:01:01")
    dao.deleteAuth(auth)

main()