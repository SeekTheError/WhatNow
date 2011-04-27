
#-------------------------User---------------------------
from couchdb.mapping import *
import dblayer
from dblayer import getDb

#TODO add topics field
class User(Document) :
  login=TextField()
  password=TextField()
  email=TextField()
  resume=TextField()
  activationCode=TextField()
  sessionId=TextField()
  sessionExpire=DateTimeField()
  topics=ListField(TextField)
  followedQuestions=ListField(TextField)
  isActivated=BooleanField()
  
  type=TextField()
  TYPE='user'
  
  #Those strings are javascript function, their usage are deprecated
  FIND_BY_LOGIN='function(u) { if(u.type == \'user\') {if( u.login == \'$login\') {emit (u.id,u);}}}'
  FIND_BY_SESSION_ID='function(u) { if(u.type == \'user\') {if( u.sessionId == \'$sessionId\') {emit (u.id,u);}}}'
  FIND_BY_ACTIVATION_CODE='function(u) { if(u.type == \'user\') {if( u.activationCode == \'$activationCode\') {emit (u.id,u);}}}'
 
    
  
  def create(self) :
  #to ensure database integrity, it is mandatory to use this method the first time to creat a new user
    if self.findByLogin() == None :
      self.isActivated=False
      self.type=self.TYPE
      self.store(getDb())
      #TODO: check if it return the last version
      return self
    else :
      print 'a user already exist for login: ', self.login
      return None
      
      
  def update(self) :
    '''
    update the user, only if he already exist
    '''  
    if self.id :
      self.store(getDb())
    else :
      print 'invalid state, attemp to update a non existing user'
      raise  IllegalAttempt



  def findByLogin(self) :
    '''
    return the actual version of the user.
    '''
    view=dblayer.view("user/login",self.login)
    if len(view) == 0 :
      return None
    elif len(view) == 1:
      #TODO optimize
      for u in view : return User.load(getDb(),u.id)
    else :
      print 'WARNING: critical error, more than one user for same login'
      raise IntegrityConstraintException

  def findByActivationCode(self) :
    view=dblayer.view('user/activationCode',self.activationCode)
    
    if len(view) == 0 :
      return None
    elif len(view) == 1:
      for u in view : return User.load(getDb(),u.id)
    else :
      print 'WARNING: critical error, more than one user with same activation Code '
      raise IntegrityConstraintException
      
  def findBySessionId(self) :
    view=dblayer.view("user/sessionId",self.sessionId)
    if len(view) == 0 :
      return None
    elif len(view) == 1:
      for u in view : return User.load(getDb(),u.id)
    else :
      print 'WARNING: critical error, more than one user with sthe same session Id '
      raise IntegrityConstraintException



class IllegalAttempt(Exception) :
  pass

