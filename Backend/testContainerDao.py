from containerDao import ContainerDao
dao = ContainerDao()
def main():
    #testAddContainer()
    testAddRelationship()
    testGetRelationship()
    #testGetContainer()
    #testDeleteContainer()

def testAddContainer():
    val = []
    qrcode = "000"
    val.append(qrcode)
    dao.addContainer(val)
    val = []
    qrcode = "001"
    val.append(qrcode)
    dao.addContainer(val)
    val = []
    qrcode = "010"
    val.append(qrcode)
    dao.addContainer(val)
    val = []
    qrcode = "011"
    val.append(qrcode)
    dao.addContainer(val)
    
    
def testGetContainer():
    qrcode = "000"
    print(dao.getContainer(qrcode))
    qrcode = "001"
    print(dao.getContainer(qrcode))
    qrcode = "010"
    print(dao.getContainer(qrcode))
    qrcode = "011"
    print(dao.getContainer(qrcode))

def testDeleteContainer():
    qrcode = "000"
    print(dao.deleteContainer(qrcode))
    qrcode = "001"
    print(dao.deleteContainer(qrcode))
    qrcode = "010"
    print(dao.deleteContainer(qrcode))
    qrcode = "011"
    print(dao.deleteContainer(qrcode))

def testGetRelationship():
    email = "test@students.stonehill.edu"
    qrcode = "000"
    status = "Checked out"
    authTime= "2021-01-01 01:01:01"
    relDict={
                "email": email,
                "qrcode": qrcode,
                "status": status,
                "statusUpdateTime": authTime}
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
    val = [email,qrcode,status,authTime]
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
    dao.addRelationship(val)
def testUpdateRelationship():
    email = "test@students.stonehill.edu"
    status = ""
    
main()