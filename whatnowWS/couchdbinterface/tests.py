#Author: RemiBouchar
from django.test import TestCase  
import dblayer
from dblayer import loadDatabase, getDb
from entities import User, IllegalAttempt


TEST_DB_NAME='kuestiondbtest'
server=dblayer.getServer()
def switchToTestDatabase(replicate=True) :
  '''
  this method change the database to a test database
  the default argument replicate mean that the database is replicate from the original
  so the design document are replicated
  '''
  print '\n------------------Running the couchdbinterface test -------------------------\n'
  print 'switching to test database'
  #easy way to make sure we have a clean database
  dblayer.db=loadDatabase(server,TEST_DB_NAME)
  if replicate :
    server.replicate(dblayer.DB_NAME,TEST_DB_NAME)
  print 'DATABASE TEST ENVIRONMENT: ',server,',',getDb()
  
def deleteTestDatabase() :
  print 'deleting the test database: ',TEST_DB_NAME
  dblayer.server.delete(TEST_DB_NAME)

class SimpleTest(TestCase):

  def test_entity_manipulation(self):
    switchToTestDatabase()
    #creating a user
    u=User(login='rem',password='pass')   
    print User.create(u) , '\n'
    self.assertTrue(u.findByLogin()!= None)
  
    #finding & updating a user
    u=User(login='rem')
    u=u.findByLogin()
    print 'user before update: ', u
    print 'changing password to strong'
    u.password='strong'
    u.update()
    u=u.findByLogin()
    print u
    self.assertEqual(u.password,'strong')
    print 'changing password to VERYstrong'
    u.password='VERYstrong'
    u.update()
    u=u.findByLogin()
    print u
    self.assertEqual(u.password,'VERYstrong')
  
    #try to update a non existing user
    raised=False
    
    try :
      u=User(login='jose',password='de')
      u.update()
    except Exception :
      print 'catch an Illegal Attempt'
      print '\ntrying to update jose, but he don\'t exist'
      raised=True
    self.assertTrue(raised)
    self.assertEqual(u.findByLogin(),None)
    
    
    deleteTestDatabase()
  '''
  #10s on remi's laptop
  #100ms /creation
  def test_lots_of_entities(self):
    switchToTestDatabase()
    i=0
    login='a'
    while i < 100 :
      u=User(login=login,password='pass')
      User.create(u)
      login+='b'
      i+=1
      
    deleteTestDatabase()
 
  #remi laptop 41ms/update
  def test_lots_of_updates(self):
    switchToTestDatabase()
    u=User(login='rem',password='pass')
    User.create(u)
    u.findByLogin()
    i=0
    while i < 100 :
      u.password=u.password+'x'
      u.update()
      i+=1
      
    deleteTestDatabase()
    
  '''
    


