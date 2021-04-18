from relationship import Relationship
from relationshipDAO import RelationshipDAO
dao = RelationshipDAO()

def main():
    """
    Uncomment the desired method to test it
    """
    #testinsertRelationship()
    #testSelectByEmail()  
    #testUpdateAuth()
    #testUpdateRelationship()
    testSelectPendingReturns()
    #testDeleteAuth()

def testinsertRelationship():
    #relationship 1
    print("yes")
    r = Relationship("ruthie_test@students.stonehill.edu","101010","Checked Out","2021-01-01 01:01:01",None)
   # dao.insertRelationship(r)

    r = Relationship("ruthie_test@students.stonehill.edu","101010","Checked Out","2021-01-01 01:01:01",None)
    dao.insertRelationship(r)

def testUpdateRelationship():
    r = Relationship("ruthie_test@students.stonehill.edu","101010","Pending Return","2021-01-01 01:01:01",None)
    dao.updateRelationship(r)

def testSelectPendingReturns():
    dao.selectPendingReturns()
main()