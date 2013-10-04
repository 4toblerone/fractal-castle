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

    #put projectkey in config 
    indexproject =  PhotoProject.query.filter_by(projectkey="indexphotos").first()
    key1= indexproject.photos[0].photokey
    for photo in indexproject.photos:
        if photo.placenumber == 1:
            key1 = photo.photokey

    key = bucket.get_key("indexphotos" + "/" + key1)
    imgurl = key.generate_url(3600, query_auth=False, force_http=True)
    return render_template("index.html", title='Home',
                           imgurl=imgurl, projectList=sortPhotosProjects(returnPublishedProjects()))

@app.route('/<path:projectkey>')
def project(projectkey):
    print "putanja"
    print request.path
    photos = returnPPPhotosUrls(projectkey)
    dump =json.dumps(photos)
    return render_template("project.html", dump = dump, photosUrl=returnPPPhotosUrls(projectkey), 
                            projectList=sortPhotosProjects(returnPublishedProjects()))



@app.before_request
def before_request():
    g.user = current_user

@app.route('/login', methods=['GET', 'POST'])
def login():

    form1 = LoginForm()
    if form1.validate_on_submit():
        # check if user with that credentials exists
        user = User.query.filter_by(username=form1.username.data, password=form1.password.data).first()
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
    user = User.query.filter_by(username=uname).first()
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
    listOfProjects = PhotoProject.query.all()
    print listOfProjects
    if form_upload.validate_on_submit():
        #extracting photo related data from request
        photoname = form_upload.photoName.data
        uploadedphoto = request.files['photo']
        projectkey = request.form['hiddenkey']
        placenumber = PhotoProject.query.filter_by(projectkey = projectkey).first().photos.count() + 1
        #seting key and data for amazon S3
        keyname = projectkey + "/" + photoname.replace(" ", "").lower()
        key = Key(bucket)
        key.key = keyname
        key.set_contents_from_file(uploadedphoto)
        #creting new Photo instance and adding it to parent PhotoProject
        newphoto = Photo(photokey=photoname.replace(" ", "").lower(), name=photoname, placenumber=placenumber, projectkey=projectkey)
        #photoproject = PhotoProject.query.filter_by(projectkey=projectkey).first()
        db.session.add(newphoto)
        db.session.commit()
        #photoproject.photos.append(newphoto)
        #photoproject.save()
    return render_template('photoupload.html' , form = form_upload , listOfProjects = listOfProjects)


@app.route('/returnproject', methods=['GET'])
@login_required
def returnproject():
    #this should be refactored so that only give list of photos urls
    #so the rest of the element injection should happen on javascript side
    projectkey = request.args.get('projectkey')
    print "ovo je key u returnproject"
    print projectkey
    print "ide potraga"
    project = PhotoProject.query.filter_by(projectkey=projectkey).first()
    listofphotourls = returnPPPhotosUrls(projectkey)
    portion = ""
    for index, url in enumerate(listofphotourls):
        portion += "<li id=" + str(
            index + 1) + "> <img src=" + url + " width='200' height='150'></img><input type = 'checkbox' class='checkbox' value='"+str(index +1)+"'/></li>"
    return jsonify({"listitems": portion,
                    "projectname": project.name,
                    "prdescription": project.description,
                    "projectkey": project.projectkey,
                    "ispublished": project.published})

@app.route('/returnindex' , methods=['GET'])
@login_required
def returnindex():
    htmlprlist=""
    #listofphotourls = returnPPPhotosUrls("indexphotos")
    for index , project in enumerate(sortPhotosProjects(PhotoProject.query.all())):
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
    print enumerate(sortPhotosProjects(PhotoProject.query.all()))
    print "pocetak"
    for project in PhotoProject.query.all():
        print project.projectkey
        print project.placenumber
    print "kraj"
    for index, project in enumerate(sortPhotosProjects(PhotoProject.query.all())):
        print "trenutni broj "+str(project.placenumber)+": novi broj "+ str(newprojectsorder.index(project.placenumber) + 1)
        #print newprojectsorder.index(project.placeNumber) + 1
        project.placenumber = newprojectsorder.index(project.placenumber) + 1
        db.session.commit()
    #send message about success 
    return jsonify({})

#proveri update!!!
@app.route('/saveeditedproject', methods=['GET'])
@login_required
def saveeditedproject():
    projectkey = request.args.get('projectkey')
    project = PhotoProject.query.filter_by(projectkey=projectkey).first()
    project.name = request.args.get('newname')
    project.description = request.args.get('newdescription')
    project.published = True if request.args.get('publish') == "true" else False
    print project.published
    db.session.commit()
    
    if project.photos.count() ==0:
        return jsonify({})


    neworder = [int(x) for x in request.args.get('neworder').split(',')]
    photostodelete = []
    if not request.args.get('photostodelete').strip()=="":
        photostodelete = [int(x) for x in request.args.get('photostodelete').split(',')]
    

    for index, photo in enumerate(sortPhotosProjects(project.photos)):
        if photo.placenumber in photostodelete:
            db.session.delete(photo)
            db.session.commit()
            bucket.delete_key(projectkey + "/" + photo.photoKey)
        else:
            #think about update function
            photo.placenumber = neworder.index(photo.placenumber) + 1
            db.session.commit()
    #send message about success   
    return jsonify({})


@app.route('/createnewproject', methods=['GET'])
@login_required
def createnewproject():
    projectname = request.args.get('projectname')
    projectkey = projectname.replace(" ", "").lower()
    if len(PhotoProject.query.filter_by(projectkey=projectkey).all()) > 0:
        return jsonify({"result": False,
                        "message": "project with that name/key already exists"})
    description = request.args.get('description')
    publish = True if request.args.get('publish') == "true" else False
    placenumber = len(PhotoProject.query.all()) + 1
    photoproject = PhotoProject(projectkey=projectkey,
                 name=projectname,
                 description=description,
                 published=publish,
                 placenumber=placenumber)
    db.session.add(photoproject)
    db.session.commit()
    return jsonify({"projectKey": projectkey,
                    "projectname": projectname,
                    "result": True,
                    "message": "project is successfully saved"})

@app.route('/saveediteduser' , methods=['GET'])
@login_required
def saveediteduser():
    #check if typed in pass is the current pass
    #save edited user
    if g.user.password == request.args.get('oldpass'):
        User.query.filter_by(username =g.user.username).update(dict(username = request.args.get('newusername') ,
                                                             password = request.args.get('newpass') , 
                                                                email = request.args.get('newemail')))
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

    return [project.name for project in PhotoProject.query.all()]


def sortPhotosProjects(pplist):

    return sorted(pplist, key=lambda pplistmember: pplistmember.placenumber)


def returnPPPhotosUrls(projectKey):
    
    listofphotokeys = [projectKey + "/" + photo.photokey
                       for photo in sorted(
                       PhotoProject.query.filter_by(projectkey=projectKey).first().photos,
                       key=lambda photo: photo.placenumber)]
    s3keys = [bucket.get_key(photokey)
              for photokey in listofphotokeys]
    listofphotourls = [s3key.generate_url(3600, query_auth=False,
                                          force_http=True) for s3key in s3keys]

    return listofphotourls


def returnPublishedProjects():
    return [project for project in PhotoProject.query.all() if project.published == True]


