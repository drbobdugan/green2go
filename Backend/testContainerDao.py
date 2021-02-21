from containerDao import ContainerDao
dao = ContainerDao()
def main():
    testAddContainer()
    testGetContainer()
    testDeleteContainer()

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

main()