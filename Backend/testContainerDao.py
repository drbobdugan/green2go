from containerDao import ContainerDao
dao = ContainerDao()
def main():
    testAddContainer()
    testAddRelationship()
    testGetRelationship()
    testGetContainer()
    testDeleteContainer()

def testAddContainer():
    
    qrcode = "000"
    contDict={"qrcode": qrcode}
    dao.addContainer(contDict)
    qrcode = "001"
    contDict={"qrcode": qrcode}
    dao.addContainer(contDict)
    qrcode = "010"
    contDict={"qrcode": qrcode}
    dao.addContainer(contDict)
    qrcode = "011"
    contDict={"qrcode": qrcode}
    dao.addContainer(contDict)
    
    
def testGetContainer():
    qrcode = "000"
    contDict={"qrcode": qrcode}
    print(dao.getContainer(contDict))
    qrcode = "001"
    contDict={"qrcode": qrcode}
    print(dao.getContainer(contDict))
    qrcode = "010"
    contDict={"qrcode": qrcode}
    print(dao.getContainer(contDict))
    qrcode = "011"
    contDict={"qrcode": qrcode}
    print(dao.getContainer(contDict))

def testDeleteContainer():
    qrcode = "000"
    contDict={"qrcode": qrcode}
    print(dao.deleteContainer(contDict))
    qrcode = "001"
    contDict={"qrcode": qrcode}
    print(dao.deleteContainer(contDict))
    qrcode = "010"
    contDict={"qrcode": qrcode}
    print(dao.deleteContainer(contDict))
    qrcode = "011"
    contDict={"qrcode": qrcode}
    print(dao.deleteContainer(contDict))

def testGetRelationship():
    email = "test@students.stonehill.edu"
    qrcode = "000"
    status = "Checked out"
    authTime= "2021-01-01 01:01:01"
    relDict={
                "email": email,
                "qrcode": qrcode,
                "status": status,
                "statusUpdateTime": None}
    dao.getRelationship(relDict)
    relDict['qrcode'] = None
    dao.getRelationship(relDict)
    relDict['status'] = None
    dao.getRelationship(relDict)
    relDict['statusUpdateTime'] = None
    dao.getRelationship(relDict)


def testAddRelationship():
    email = "test@students.stonehill.edu"
    qrcode = "000"
    status = "Checked out"
    authTime= "2021-01-01 01:01:01"
    relDict={
                "email": email,
                "qrcode": qrcode,
                "status": status,
                "statusUpdateTime": None}
    dao.addRelationship(relDict)
    email = "test1@students.stonehill.edu"
    qrcode = "000"
    status = "Checked out"
    authTime= "2021-01-01 01:01:01"
    val = [email,qrcode,status,authTime]
    email = "test@students.stonehill.edu"
    qrcode = "001"
    status = "Checked out"
    authTime= "2021-01-01 01:01:01"
    val = [email,qrcode,status]
    #dao.addRelationship(val)
def testUpdateRelationship():
    email = "test@students.stonehill.edu"
    status = ""
    
main()