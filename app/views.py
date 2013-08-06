from flask import render_template, flash, redirect, session, url_for, request, g, jsonify, make_response
from app import app
from forms import LoginForm, PhotoUpload, CreateProject
from models import Photo, User, PhotoProject
from app import db, app, lm, s3 , bucket
from flask.ext.login import login_user, logout_user, current_user, login_required
from boto.s3.key import Key
import inspect
import boto
import os
import json

@app.route('/')
@app.route('/index')
def index():

    # PhotoProject.objects(projectKey = "probaprojekat")[0].delete()
    #put projectkey in config 
    indexproject =  PhotoProject.objects.get(projectKey="indexphotos")
    key1= indexproject.photos[0].photoKey
    for photo in indexproject.photos:
        if photo.photoKey == 1:
            key1 = photo.photoKey

    key = bucket.get_key("indexphotos" + "/" + key1)
    imgurl = key.generate_url(3600, query_auth=False, force_http=True)
    return render_template("index.html", title='Home',
                           imgurl=imgurl, projectList=sortPhotosProjects(returnPublishedProjects()))
    #response = make_response(render_template("index.html", title='Home',imgurl=imgurl, projectList=returnPublishedProjects()))
    #response.headers['proba'] = "reci nesto"
    #return response


@app.route('/project/<projectKey>')
def project(projectKey):
    print "putanja"
    print request.path
    print request.endpoint
    photos = returnPPPhotosUrls(projectKey)
    dump =json.dumps(photos)
    return render_template("project.html", dump = dump, photosUrl=returnPPPhotosUrls(projectKey), 
                            projectList=sortPhotosProjects(returnPublishedProjects()))


@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():

    form1 = LoginForm()
    if form1.validate_on_submit():
        # check if user with that credentials exists
        user = User.objects.get(username=form1.username.data, password=form1.password.data)
        if user:
            login_user(user)
            flash("Logged in successfully")
            return redirect('/admin')
        #else:
            #pass

    return render_template('login.html', title='Sign in', formcreate=form1)


@lm.user_loader
def load_user(uname):
    # un  = str(username)
    user = User.objects.get(username=uname)
    if user:
        return user
    else:
        return None


@app.route('/logout')
@login_required
def logout():

    logout_user()
    flash('You have logged out')
    return(redirect(url_for('login')))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    form_upload = PhotoUpload()
    """PhotoProject(projectKey="noviprojekat",
                 name="Novi projekat",
                 description="opis drugog projekta",
                 publish=False,
                 placeNumber=2).save()"""
    listOfProjects = PhotoProject.objects
    print listOfProjects
    if form_upload.validate_on_submit():
        #extracting photo related data from request
        photoName = form_upload.photoName.data
        uploadedphoto = request.files['photo']
        projectkey = request.form['hiddenkey']
        placeNumber = len(PhotoProject.objects.get(projectKey = projectkey).photos) + 1
        #seting key and data for amazon S3
        keyname = projectkey + "/" + photoName.replace(" ", "").lower()
        key = Key(bucket)
        key.key = keyname
        key.set_contents_from_file(uploadedphoto)
        #creting new Photo instance and adding it to parent PhotoProject
        newphoto = Photo(photoKey=photoName.replace(" ", "").lower(), name=photoName, placeNumber=placeNumber)
        photoproject = PhotoProject.objects.get(projectKey=projectkey)
        photoproject.photos.append(newphoto)
        photoproject.save()
    return render_template('photoupload.html' , form = form_upload , listOfProjects = listOfProjects)


@app.route('/returnproject', methods=['GET'])
@login_required
def returnproject():
    #this should be refactored so that only give list of photos urls
    #so the rest of the element injection should happen on javascript side
    projectkey = request.args.get('projectkey')
    project = PhotoProject.objects.get(projectKey=projectkey)
    listofphotourls = returnPPPhotosUrls(projectkey)
    portion = ""
    for index, url in enumerate(listofphotourls):
        portion += "<li id=" + str(
            index + 1) + "> <img src=" + url + " width='200' height='150'></img><input type = 'checkbox' class='checkbox' value='"+str(index +1)+"'/></li>"
    return jsonify({"listitems": portion,
                    "projectname": project.name,
                    "prdescription": project.description,
                    "projectkey": project.projectKey,
                    "ispublished": project.published})

@app.route('/returnindex' , methods=['GET'])
@login_required
def returnindex():
    htmlprlist=""
    #listofphotourls = returnPPPhotosUrls("indexphotos")
    for index , project in enumerate(sortPhotosProjects(PhotoProject.objects)):
        htmlprlist += "<li id="+str(index+1) +">"+project.name+"</li>"
        print "ime projekta"
        print project.name
    return jsonify({"projectlist":htmlprlist})

@app.route('/saveeditedindex' , methods=['GET', 'POST'])
@login_required
def saveeditedindex():

    print "nesto se desava"
    newprojectsorder = [int(x) for x in request.args.get('newprorder').split(',')]
    print newprojectsorder

    print "posle sortiranja"
    print enumerate(sortPhotosProjects(PhotoProject.objects))
    print "pocetak"
    for project in PhotoProject.objects:
        print project.projectKey
        print project.placeNumber
    print "kraj"
    for index, project in enumerate(sortPhotosProjects(PhotoProject.objects)):
        print "trenutni broj "+str(project.placeNumber)+": novi broj "+ str(newprojectsorder.index(project.placeNumber) + 1)
        #print newprojectsorder.index(project.placeNumber) + 1
        project.placeNumber = newprojectsorder.index(project.placeNumber) + 1
        project.save()
    #send message about success 
    return jsonify({})


#PhotoProject.objects(projectKey = "indexphotos" , photos__placeNumber=photonumber).update_one(set__photos__S__placeNumber=1)	

@app.route('/saveeditedproject', methods=['GET'])
@login_required
def saveeditedproject():
    projectkey = request.args.get('projectkey')
    project = PhotoProject.objects.get(projectKey=projectkey)
    
    neworder = [int(x) for x in request.args.get('neworder').split(',')]
    photostodelete = []
    if not request.args.get('photostodelete').strip()=="":
        photostodelete = [int(x) for x in request.args.get('photostodelete').split(',')]

    project.name = request.args.get('newname')
    project.description = request.args.get('newdescription')
    project.published = True if request.args.get('publish') == "true" else False
    project.save()
    for index, photo in enumerate(sortPhotosProjects(project.photos)):
        if photo.placeNumber in photostodelete:
            #for some reasone i can't call update_one on project which is returned via objects.get()
            PhotoProject.objects(projectKey=projectkey).update_one(pull__photos__placeNumber = photo.placeNumber)
            bucket.delete_key(projectkey + "/" + photo.photoKey)

        else:

            photo.placeNumber = neworder.index(photo.placeNumber) + 1
            project.save()
    #send message about success   
    return jsonify({})


@app.route('/createnewproject', methods=['GET'])
@login_required
def createnewproject():
    projectname = request.args.get('projectname')
    projectKey = projectname.replace(" ", "").lower()
    if len(PhotoProject.objects(projectKey=projectKey)) > 0:
        return jsonify({"result": False,
                        "message": "project with that name/key already exists"})
    description = request.args.get('description')
    publish = True if request.args.get('publish') == "true" else False
    placeNumber = len(PhotoProject.objects) + 1
    PhotoProject(projectKey=projectKey,
                 name=projectname,
                 description=description,
                 publish=publish,
                 placeNumber=placeNumber).save()
    return jsonify({"projectKey": projectKey,
                    "projectname": projectname,
                    "result": True,
                    "message": "project is successfully saved"})

@app.route('/saveediteduser' , methods=['GET'])
@login_required
def saveediteduser():
    #check if typed in pass is the current pass
    #save edited user
    if g.user.password == request.args.get('oldpass'):
        User.objects.get(username =g.user.username).update(username = request.args.get('newusername') ,
                                                             password = request.args.get('newpass') , 
                                                                email = request.args.get('newemail'))
        return jsonify({"success" : "Novi podaci su uspesno sacuvani"})
    else:
        return jsonify({"success": "Trenutna sifra nije identicna unetoj"})


@app.route('/savenewuser' , methods=['GET'])
def savenewuser():
    #do i rlly need this?
    #check if pass is empty , i user with that name already exists
    pass

@app.route('/returnuser' , methods=['GET'])
def returnuser():
    pass

def returnProjectList():

    return [project.name for project in PhotoProject.objects]


def sortPhotosProjects(pplist):

    return sorted(pplist, key=lambda pplistmember: pplistmember.placeNumber)


def returnPPPhotosUrls(projectKey):

    listofphotokeys = [projectKey + "/" + photo.photoKey
                       for photo in sorted(
                       PhotoProject.objects.get(projectKey=projectKey).photos,
                       key=lambda photo: photo.placeNumber)]
    s3keys = [bucket.get_key(photokey)
              for photokey in listofphotokeys]
    listofphotourls = [s3key.generate_url(3600, query_auth=False,
                                          force_http=True) for s3key in s3keys]

    return listofphotourls


def returnPublishedProjects():
    return [project for project in PhotoProject.objects if project.published == True]


