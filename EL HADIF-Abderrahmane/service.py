import subprocess
import crypt
import os
from datetime import datetime

months = [
    "janvier",
    "février",
    "mars",
    "avril",
    "mai",
    "juin",
    "juillet",
    "août",
    "septembre",
    "octobre",
    "novembre",
    "décembre"
]


class UserService:
    def __init__(self):
      pass  


    def seConnecter(self,user,password) :
        output = subprocess.check_output(f'cat /etc/shadow | grep "{user}"',shell=True, universal_newlines=True)
        passwd = output.split(":")[1]
        print(password)
        hashcode = crypt.crypt(password,passwd)
        if passwd == hashcode :
            return True
        else :
            return False
    
    
    def Root(self,user):
        return f'/home/{user}'

    def FilesCount(self,user):
        cmd=f"find {self.Root(user)} -type f | wc -l"
        output = subprocess.check_output(cmd, shell=True, universal_newlines=True)
        return output

    def FoldersCount(self,user):
        return subprocess.check_output(f"find {self.Root(user)} -type d | wc -l", shell=True, universal_newlines=True)

    def UsedSpace(self,user):
        cmd=f"du -sh {self.Root(user)}"
        return subprocess.check_output(cmd, shell=True, universal_newlines=True)
    
    def search(self,user,query):
        listFiles=[]
        cmd=f'find {self.Root(user)} -name "*{query}*"'
        result= subprocess.check_output(cmd, shell=True, universal_newlines=True)
        result.remove('')
        for r in result:  
            
            dict=self.fileToInfos(r)
            listFiles.append(dict)
        return listFiles

    def FileContent(self,file):
        f=open(file,'r')
        content=f.readlines()
        f.close()
        return content

    def FolderElements(self,folder):
        if os.path.isdir(folder):
            files= os.listdir(folder)
        listFiles=[]
        for f in files:
            name=f
            path=folder+'/'+name
            infos=os.stat(path)
            mod=datetime.fromtimestamp(infos.st_mtime)
            date=self.dateToString(mod)
            size=infos.st_size
            type=''
            if os.path.isdir(path):
                type='dir'
            else:
                type='file'
            dict={
                'name':name,
                'modtime':date,
                'size':size,
                'chemin':path,
                'type':type
            }
            listFiles.append(dict)
        return listFiles

    def fileToInfos(self,path):
        infos=os.stat(path)
        mod=datetime.fromtimestamp(infos.st_mtime)
        date=self.dateToString(mod)
        size=infos.st_size
        link=''
        if os.path.isdir(path):
            link=path
        dict={
            'name':path,
            'mtime':date,
            'size':size,
            'link':link
        }
        return dict

    def dateToString(self,date):
        day = date.day
        month = months[int(date.month)-1]
        year = date.year
        hour = date.hour
        minute = date.minute
        return f'{day} {month} {year} à {hour}:{minute}'
    
    def Download(self,user):
        home_dir = f"/home/{user}"
        zip_filename = f"{user}.zip"
        downloads=subprocess.run(["zip", "-r", zip_filename, home_dir])
        return downloads

