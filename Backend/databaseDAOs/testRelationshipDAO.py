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
    #testSelectPendingReturns()
    #testSelectActiveQRcode()
    #testDeleteAuth()
    testUpdatePoints()
    testUpdateUser()

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

def testSelectActiveQRcode():
    dao.selectActiveQRcode("958bbde6-c11a-49fb-9952-70d95ce2e277")

def testUpdatePoints():
    r = Relationship('eblake1@students.stonehill.edu', '742598cc-7281-4b0a-a401-3bf9da6d7200', 'Checked Out', '2021-04-27 20:11:17', 'None', None)
    dao.updatePoints(r)

def testUpdateUser():
    r = Relationship('eblake1@students.stonehill.edu', 'ce60607c-b4e0-4050-93de-698ac34354d6', 'Pending Return', '2021-04-23 12:41:20', 'L002', None)
    dao.updateRelationship(r)

main()

