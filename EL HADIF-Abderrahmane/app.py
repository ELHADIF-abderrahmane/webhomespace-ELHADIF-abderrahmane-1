import logging
import os
from service import UserService
from flask import (
  Flask,
  request,
  render_template,
  redirect,
  session,
)
app = Flask(__name__)
app.secret_key = '8529@jnhuc'




@app.route("/")
def index():
  if 'username' in session:
    path=service.Root(session['username'])
    return redirect(f'/home?path={path}')
  return render_template("login.html")


@app.route("/home")
def homePage():
  path=request.args.get('path')
  user=session['username']
  if path==None:
    path=session['currentPath']
  session['currentPath']=path
  files=service.FolderElements(path)
  backPath='/'.join(str(path).split('/')[:-1])
  filesCount=service.FilesCount(user)
  foldersCount=service.FoldersCount(user)
  usedSpace=service.UsedSpace(user)
  return render_template("home.html",path=path,backPath=backPath,files=files,filesCount=filesCount,foldersCount=foldersCount,usedSpace=usedSpace)
 

@app.route("/file")
def File():
  file=request.args.get('path')  
  content=service.FileContent(file)
  tab=file.split('/')
  title=tab[-1]
  back='/'.join(tab[:-1])
  return render_template("file.html",content=content,title=title,backPath=back)

@app.route("/search",methods=["POST" , "GET"])
def search():
  if request.method == "POST":
        query = request.form.get("query")
        username = session.get('username')
        home_dir=f"/home/{username}"
        matching_files = []
        for root, dirs, files in os.walk(home_dir):
            for file in files:
                if query in file:
                    matching_files.append(os.path.join(root, file))
        return render_template("search-form.html", matching_files=matching_files)
  else:
        return render_template("search-form.html")


@app.route("/return")
def goBack():
  redirect(f'/home')

@app.route('/login', methods=['POST'])
def login():
  user = request.form["username"]
  password = request.form['password']
  sign=service.seConnecter(user, password)
  if sign==True:
    session['username']=user
    path=service.Root(session['username'])
    return redirect(f'/home?path={path}')
  else:
    return render_template('login.html',err=sign)
  
@app.route('/logout')
def logout():
  if 'username' in session:
    session.pop('username')
    return redirect('/')

@app.route("/download", methods=["POST"])
def Download():
    username = session.get('username')
    service.Download(username)
    return "Download successful"

   
if __name__ == "__main__":
  
  service=UserService()
  
  app.run(host="0.0.0.0", port=9090, debug=True)
  logging.basicConfig(filename='app.log', level=logging.INFO) 