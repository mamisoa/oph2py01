# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################

def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    also notice there is http://..../[app]/appadmin/manage/auth to allow administrator to manage users
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()

def home():
    if (request.args(0) == None):
        membership = '2'
    else:
        try:
            check_group= db(db.auth_group.id == request.args(0)).isempty()
        except ValueError:
            membership = '2'
        else:
            if check_group is True:
                membership = '2'
            else:
                membership = str(request.args(0))
    group = (db(db.auth_group.id == membership).select().first()).role #name of membership
    exams = XML(rows2json('content',db(db.exam2do_OBR4).select(db.exam2do_OBR4.id,db.exam2do_OBR4.exam_description)))
    facilities = XML(rows2json('content',db(db.facility).select(db.facility.id,db.facility.facility_name)))
    modalities = XML(rows2json('content',db(db.modality).select(db.modality.id,db.modality.modality_name)))
    query_sessions = ((db.auth_user.id == db.auth_membership.user_id)&
    ((db.auth_membership.group_id == 3)|(db.auth_membership.group_id == 4)|(db.auth_membership.group_id == 7))
    )
    providers = XML(rows2json('content',db(query_sessions).select(db.auth_user.id,db.auth_user.first_name,db.auth_user.last_name)))
    return locals()

def rows2json (tablename,rows):
    import datetime
    import json
    def date_handler(obj):
        if isinstance(obj, datetime.datetime):
            return obj.strftime(str(T('%d/%m/%Y %T')))
        elif isinstance(obj, datetime.date):
            return obj.strftime(str(T('%d/%m/%Y')))
        else:
            return False
    rows = rows.as_list()
    concat = '{ "'+tablename+'": ['
    for row in rows:
        concat = concat + json.dumps(row, default=date_handler)+","
    concat = concat.strip(',')
    concat = concat + ']}'
    return concat

def check_duplicate(form):
    form.vars.first_name = form.vars.first_name.capitalize()
    form.vars.last_name = form.vars.last_name.capitalize()
    fname = form.vars.first_name
    lname = form.vars.last_name
    dob = form.vars.dob_pid7
    check = db((db.auth_user.first_name==fname)&(db.auth_user.last_name==lname)&(db.auth_user.dob_pid7==dob)).isempty()
    if check is False: # if user with same first_name last_name dob exist, it is a duplicate
        form.errors.first_name = form.errors.last_name = form.errors.dob_pid7 = "Duplicate exist in database"

# ****  "END CRUD users" ******

def file():
    user_id = request.args(0) or redirect(URL('home'))
    try:
        if (db(db.auth_user.id == user_id).count() == 0):
            redirect(URL('home'))
    except ValueError:
        redirect(URL('home'))
    origin_rows = db(db.data_origin).select(db.data_origin.origin)
    origin_json = XML(rows2json('phones',origin_rows))
    return locals()

def get_user_name(id):
    try:
        username = db(db.auth_user == id).select(db.auth_user.first_name, db.auth_user.last_name)
    except ValueError: return 'unknown'
    firstname= username[0].first_name
    lastname= username[0].last_name
    return dict(lastname=lastname,firstname=firstname)


def test():
    return locals()
