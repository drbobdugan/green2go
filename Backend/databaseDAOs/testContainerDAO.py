from container import Container
from containerDAO import ContainerDAO
dao = ContainerDAO()

def main():
    """
    Uncomment the desired method to test it
    """
    testinsertContainer()
    #testSelectByEmail()  
    #testUpdateAuth()
    #testDeleteAuth()

def testinsertContainer():
    #container 1
    print("yes")
    container = Container("1234567")
    dao.insertContainer(container)

main()