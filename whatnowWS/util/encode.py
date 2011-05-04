from hashlib import sha1

def encode(string) : 
  return sha1(string).hexdigest()
