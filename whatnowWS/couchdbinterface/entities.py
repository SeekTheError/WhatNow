
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
  isActivated=BooleanField()
  
  type=TextField()
  TYPE='user'
 
    
  
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



class Article(Document) :
  _id = TextField()
  link=TextField()
  title=TextField()
  date=DateTimeField()
  extract=TextField()
  content=TextField()
  sessionExpire=DateTimeField()
  tags=ListField(TextField)
  isAnalyzed=BooleanField()
  source=TextField()
  
  def __init__(self,id,link,title,date,extract,isAnalyzed=False,content=None)
    self._id=id
    self.link=link
    self.title=title
    self.date=date
    self.extract=extract
    self.isAnalyzed=isAnalyzed
    self.content=content
  
  def create(self):
    if self.findByName() == None:
      self.store(getDb())
  def update(self):
    '''
    update the user, only if he already exist
    '''  
    if self.id:
      self.store(getDb())*
      
  def findByLink(self)
    return Article.load(dblayer.db,self.name)

class IllegalAttempt(Exception) :
  pass

