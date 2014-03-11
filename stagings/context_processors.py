import os

def last_commit_date(request):
  return {
    'last_commit_date': os.popen('git log -1 --format=%ci').read()
  }
