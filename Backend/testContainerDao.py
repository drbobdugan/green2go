from containerDao import ContainerDao
dao = ContainerDao()
def main():
    #testAddContainer()
    testAddRelationship()
    #testUpdateRelationship()
    #testGetRelationship()
    #testGetContainer()
    #testDeleteContainer()
    testSelectAllByEmail()
    #testSelectCheckedOut()

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
    email = "shai@stonehill.edu"
    qrcode = "000000001"
    status = "Pending Return"
    authTime= "2021-01-01 01:01:01"
    location_qrcode="L003"
    relDict={
                "email": email,
                "qrcode": qrcode,
                "status": status,
                "statusUpdateTime": None,
                "location_qrcode": location_qrcode}
    dao.addRelationship(relDict)

    """
    email = "test@students.stonehill.edu"
    qrcode = "000"
    status = "Pending Return"
    authTime= "2021-01-01 01:01:01"
    location_qrcode = "L001"
    relDict={
                "email": email,
                "qrcode": qrcode,
                "status": status,
                "statusUpdateTime": None,
                "location_qrcode": location_qrcode}
    dao.addRelationship(relDict)

    email = "test@students.stonehill.edu"
    qrcode = "001"
    status = "Verified Return"
    authTime= "2021-01-01 01:01:01"
    relDict={
                "email": email,
                "qrcode": qrcode,
                "status": status,
                "statusUpdateTime": None,
                "location_qrcode": None}
    dao.addRelationship(relDict)
"""
def testUpdateRelationship():
    #email = "test@students.stonehill.edu"
    #status = ""
    email = "test@students.stonehill.edu"
    qrcode = "000"
    status = "Pending Return"
    authTime= "2021-01-01 01:01:01"
    location_qrcode = "L002"
    relDict={
                "email": email,
                "qrcode": qrcode,
                "status": status,
                "statusUpdateTime": None,
                "location_qrcode": location_qrcode}
    dao.updateRelationship(relDict)

def testSelectAllByEmail():
    emailDict={
                "email": "test@students.stonehill.edu"
            }
    dao.selectAllByEmail(emailDict)

def testSelectCheckedOut():
    relDict={
                "email": "test@students.stonehill.edu",
                "status": "Checked out"
            }
    dao.selectCheckedOut(relDict)

main()