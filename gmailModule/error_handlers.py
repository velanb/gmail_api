class GmailAPIError(Exception):
  def __init__(self, *args):
    if args:
      self.message = args[0]
      self.methodName = args[1]
    else:
      self.message = None
      self.methodName = None

  def __str__(self):
    if self.message:
      return "GmailAPI->Error at method{}, Error message>> {}".format(self.methodName, self.message)



class GmailRepoError(GmailAPIError):
  def __init__(self, *args):
    if args:
      self.message = args[0]
      self.methodName = args[1]
    else:
      self.message = None
      self.methodName = None

  def __str__(self):
    if self.message:
      return "GmailRepoError->Error at method{}, Error message>> {}".format(self.methodName, self.message)

