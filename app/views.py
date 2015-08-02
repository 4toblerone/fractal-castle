import os

from flask import (render_template, flash, redirect,
                   url_for, request, g, jsonify, send_from_directory)
from flask.ext.login import login_user, logout_user, current_user, login_required
from boto.s3.key import Key

from sqlalchemy import exc

from forms import LoginForm, PhotoUpload
from app.models import Photo, User, PhotoProject, Page
from app import lm
from app import Session
from app import app2 as app
from s3connect import getbucket as bucket


@app.route('/')
@app.route('/index')
def index():
    # put projectkey in config
    # make decorator madafaka!
    db = Session()
    # attempt = 0
    for attempt in range(3):
        try:
            imgurl = (db.query(Photo).join(PhotoProject)
                        .filter(PhotoProject.projectkey == "indexphotos")
                        .filter(Photo.placenumber == 1)
                        .first()
                        .photourl)
            break
        except exc.OperationalError:
            db.rollback()
            attempt += 1
    return render_template("index.html", title='Home',
                           imgurl=imgurl, projectList=sortPhotosProjects(returnPublishedProjects()))

@app.route('/<path:projectkey>')
def project(projectkey):
    # make decorator!
    db = Session()
    # attempt = 0
    for attempt in range(3):
        try:
            photos = db.query(PhotoProject).filter_by(projectkey=projectkey).first().photos
            photos = returnPPPhotosUrls(projectkey)
            break
        except exc.OperationalError:
            db.session.rollback()
            attempt += 1
    return render_template("project.html", photosUrl=photos, length=len(photos),
                           projectList=sortPhotosProjects(returnPublishedProjects()))


@app.before_request
def before_request():
    g.user = current_user


@app.route('/login', methods=['GET', 'POST'])
def login():
    form1 = LoginForm()
    db = Session()
    if form1.validate_on_submit():
        # check if user with that credentials exists
        user = db.query(User).filter_by(username=form1.username.data,
                                        password=form1.password.data).first()
        if user:
            login_user(user)
            flash("Logged in successfully")
            return redirect('/admin')
            # else:
            # pass
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
    return (redirect(url_for('login')))


@app.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    db = Session()
    form_upload = PhotoUpload()
    listOfProjects = PhotoProject.query.all()

    if form_upload.validate_on_submit():
        # extracting photo related data from request
        photoname = form_upload.photoName.data
        uploadedphoto = request.files['photo']
        projectkey = request.form['hiddenkey']
        placenumber = db.query(PhotoProject).filter_by(projectkey=projectkey).first().photos.count() + 1
        # seting key and data for amazon S3
        keyname = projectkey + "/" + photoname.replace(" ", "").lower()
        key = Key(bucket())
        key.key = keyname
        key.set_metadata("Content-Type", 'image/jpeg')
        key.set_metadata("Cache-Control", 'max-age=910000')
        # key.set_acl('public-read')
        key.set_contents_from_file(uploadedphoto)
        key.set_acl('public-read')
        url = key.generate_url(0, query_auth=False, force_http=True)
        # creting new Photo instance and adding it to parent PhotoProject
        newphoto = Photo(photokey=photoname.replace(" ", "").lower(),
                         name=photoname, placenumber=placenumber,
                         projectkey=projectkey, photourl=url)
        db.add(newphoto)
        db.commit()
    return render_template('photoupload.html', form=form_upload, listOfProjects=listOfProjects)


@app.route('/returnproject', methods=['GET'])
@login_required
def returnproject():
    # this should be refactored so that only give list of photos urls
    # so the rest of the element injection should happen on javascript side
    # put this big ass "portion" string outside views
    db = Session()
    projectkey = request.args.get('projectkey')
    #project = db.query(PhotoProject).filter_by(projectkey=projectkey).first()
    listofphotourls = returnPPPhotosUrls(projectkey)
    portion = ""
    # create html (jinja) template and fill it
    for index, url in enumerate(listofphotourls):
        portion += "<li id=" + str(
            index + 1) + "> <img src=" + url + " width='200' height='150'></img><input type = 'checkbox' class='checkbox' value='" + str(
            index + 1) + "'/></li>"
    return jsonify({"listitems": portion,
                    "projectname": project.name,
                    "prdescription": project.description,
                    "projectkey": project.projectkey,
                    "ispublished": project.published})


@app.route('/returnindex', methods=['GET'])
@login_required
def returnindex():
    htmlprlist = ""
    for index, project in enumerate(sortPhotosProjects(PhotoProject.query.all())):
        htmlprlist += "<li id=" + str(index + 1) + ">" + project.name + "</li>"
    return jsonify({"projectlist": htmlprlist})


@app.route('/saveeditedindex', methods=['GET', 'POST'])
@login_required
def saveeditedindex():
    db = Session()
    newprojectsorder = [int(x) for x in request.args.get('newprorder').split(',')]
    for index, project in enumerate(sortPhotosProjects(db.query(PhotoProject).all())):
        project.placenumber = newprojectsorder.index(project.placenumber) + 1
        db.commit()
    # send message about success
    return jsonify({})


# check flasksqlalchemy updated function
@app.route('/saveeditedproject', methods=['GET'])
@login_required
def saveeditedproject():
    db = Session()
    projectkey = request.args.get('projectkey')
    project = db.query(PhotoProject).filter_by(projectkey=projectkey).first()
    project.name = request.args.get('newname')
    project.description = request.args.get('newdescription')
    project.published = True if request.args.get('publish') == "true" else False
    db.commit()

    if project.photos.count() == 0:
        return jsonify({})

    neworder = [int(x) for x in request.args.get('neworder').split(',')]
    photostodelete = []
    if not request.args.get('photostodelete').strip() == "":
        photostodelete = [int(x) for x in request.args.get('photostodelete').split(',')]

    for index, photo in enumerate(sortPhotosProjects(project.photos)):
        if photo.placenumber in photostodelete:
            db.delete(photo)
            db.commit()
            bucket.delete_key(projectkey + "/" + photo.photokey)
        else:
            # think about update function
            photo.placenumber = neworder.index(photo.placenumber) + 1
            db.commit()
    # send message about success
    return jsonify({})


@app.route('/createnewproject', methods=['GET'])
@login_required
def createnewproject():
    db = Session()
    projectname = request.args.get('projectname')
    projectkey = projectname.replace(" ", "").lower()
    if len(db.query(PhotoProject).filter_by(projectkey=projectkey).all()) > 0:
        return jsonify({"result": False,
                        "message": "project with that name/key already exists"})
    description = request.args.get('description')
    publish = True if request.args.get('publish') == "true" else False
    placenumber = len(db.query(PhotoProject).all()) + 1
    photoproject = PhotoProject(projectkey=projectkey,
                                name=projectname,
                                description=description,
                                published=publish,
                                placenumber=placenumber)
    db.add(photoproject)
    db.commit()
    return jsonify({"projectKey": projectkey,
                    "projectname": projectname,
                    "result": True,
                    "message": "project is successfully saved"})


@app.route('/saveediteduser', methods=['GET'])
@login_required
def saveediteduser():
    # check if typed in pass is the current pass
    # save edited user
    db = Session()
    if g.user.password == request.args.get('oldpass'):
        db.query(User)\
          .filter_by(username=g.user.username)\
          .update(dict(username=request.args.get('newusername'),
                       password=request.args.get('newpass'),
                       email=request.args.get('newemail')))
        return jsonify({"success": "Novi podaci su uspesno sacuvani"})
    else:
        return jsonify({"success": "Trenutna sifra nije identicna unetoj"})


@app.route('/savenewuser', methods=['GET'])
def savenewuser():
    # do i rlly need this?
    # check if pass is empty , i user with that name already exists
    pass


@app.route('/returnuser', methods=['GET'])
def returnuser():
    pass


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')


@app.teardown_appcontext
def shutdown_session(exception=None):
    # db.session.remove()
    pass


def returnProjectList():
    db = Session()
    return [project.name for project in db.query(PhotoProject).all()]


def sortPhotosProjects(pplist):
    return sorted(pplist, key=lambda pplistmember: pplistmember.placenumber)


def returnPPPhotosUrls(projectKey):
    db = Session()
    # photos = db.query(Photo).filter_by(projectkey=projectKey).all()
    photos = db.query(PhotoProject).filter_by(projectkey=projectKey).first().photos
    listofphotourls = [photo.photourl for photo in
                       sorted(photos,
                              key=lambda photo: photo.placenumber)]
    return listofphotourls


def returnPublishedProjects():
    db = Session()
    return [project for project in db.query(PhotoProject).all() if project.published == True]


def get_pages(frm=0, to=1):
    try:
        db = Session()
        pages = db.query(Page).filter(Page.page_num.between(frm, to))
        return pages
    except exc.OperationalError:
        try:
            db.rollback()
        except Exception:
            pass


def add_obj(object):
    db = Session()
    try:
        db.add(object)
        db.commit()
        return object
    except exc.OperationalError:
        try:
            db.rollback()
        except Exception:
            pass


def photo_to_page(photo, page):
    photo.projectkey = 'back-yard'


@app.route('/back-yard')
def back_yard():
    # return first two pages

    return render_template('backyard.html')
