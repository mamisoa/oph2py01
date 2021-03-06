# -*- coding: utf-8 -*-

#########################################################################
## This scaffolding model makes your app work on Google App Engine too 
## File is released under public domain and you can use without limitations
#########################################################################

## if SSL/HTTPS is properly configured and you want all HTTP requests to
## be redirected to HTTPS, uncomment the line below:
# request.requires_https()

## app configuration made easy. Look inside private/appconfig.ini
from gluon.contrib.appconfig import AppConfig
## once in production, remove reload=True to gain full speed
myconf = AppConfig(reload=True)


if not request.env.web2py_runtime_gae:
    ## if NOT running on Google App Engine use SQLite or other DB
    db = DAL(myconf.take('db.uri'), pool_size=myconf.take('db.pool_size', cast=int), check_reserved=['all'])
else:
    ## connect to Google BigTable (optional 'google:datastore://namespace')
    db = DAL('google:datastore+ndb')
    ## store sessions and tickets there
    session.connect(request, response, db=db)
    ## or store session in Memcache, Redis, etc.
    ## from gluon.contrib.memdb import MEMDB
    ## from google.appengine.api.memcache import Client
    ## session.connect(request, response, db = MEMDB(Client()))

## by default give a view/generic.extension to all actions from localhost
## none otherwise. a pattern can be 'controller/function.extension'
response.generic_patterns = ['*'] if request.is_local else []
## choose a style for forms
response.formstyle = myconf.take('forms.formstyle')  # or 'bootstrap3_stacked' or 'bootstrap2' or other
response.form_label_separator = myconf.take('forms.separator')


## (optional) optimize handling of static files
# response.optimize_css = 'concat,minify,inline'
# response.optimize_js = 'concat,minify,inline'
## (optional) static assets folder versioning
# response.static_version = '0.0.0'
#########################################################################
## Here is sample code if you need for
## - email capabilities
## - authentication (registration, login, logout, ... )
## - authorization (role based authorization)
## - services (xml, csv, json, xmlrpc, jsonrpc, amf, rss)
## - old style crud actions
## (more options discussed in gluon/tools.py)
#########################################################################

from gluon.tools import Auth, Service, PluginManager

auth = Auth(db)
service = Service()
plugins = PluginManager()

## create all tables needed by auth if not custom tables
# custom auth_user

db.define_table('gender',
    Field('sex','string'))
db.define_table('ethny',
    Field('ethny','string'))
db.define_table('marital',
    Field('marital_status'))
db.define_table('photo_id',
    Field('imagefile', 'upload'))

auth.settings.extra_fields['auth_user']= [  Field('maiden_name_pid6','string', label='Maiden name'),
                                            Field('dob_pid7','date', label='Date of birth'),
                                            Field('birth_town_pid23', 'string', label='Town of birth'),
                                            Field('birth_country_pid23', 'string', label='Country of birth'),
                                            Field('gender_pid8', 'reference gender', label='Gender'),
                                            Field('marital_pid16', 'reference marital', label='Marital status'),
                                            Field('ethny_pid22', 'reference ethny', label='Ethny'),
                                            Field('idc_num', 'string', label='ID card number'),
                                            Field('ssn_pid19', 'string', label='SSN'),
                                            Field('user_notes', 'string', label ='User notes'),
                                            Field('photo_id', 'reference photo_id'),
                                            Field('chipnumber', 'string', label ='Chipnumber'),
                                            Field('validfrom', 'date', label ='ID valid from'),
                                            Field('validtill', 'date', label ='ID valid til'),
                                            Field('initials', 'string', label ='ID initials'),
                                            Field('nationality', 'string', label ='nationality'),
                                            Field('noblecondition', 'string', label ='ID noble condition'),
                                            Field('documenttype', 'integer', label ='ID doctype'),
                                            Field('specialstatus', 'integer', label ='ID specialstatus'),
                                            auth.signature]

def represent_auth(auth_ref, row):
    user = db(db.auth_user.id == auth_ref).select(db.auth_user.first_name, db.auth_user.last_name).first()
    return ('%(first_name)s %(last_name)s' % user) if user else '<system>'  # else assume it was the scheduler.

auth.signature.created_by.represent = auth.signature.modified_by.represent = represent_auth


auth.define_tables(username=False, signature=False)

db.auth_user.gender_pid8.requires = IS_IN_DB(db,db.gender.id,'%(sex)s')
db.auth_user.dob_pid7.requires = IS_NOT_EMPTY()

## configure email
mail = auth.settings.mailer
mail.settings.server = 'logging' if request.is_local else myconf.take('smtp.server')
mail.settings.sender = myconf.take('smtp.sender')
mail.settings.login = myconf.take('smtp.login')

## configure auth policy
auth.settings.registration_requires_verification = False
auth.settings.registration_requires_approval = False
auth.settings.reset_password_requires_verification = True

#########################################################################
## Define your tables below (or better in another model file) for example
##
## >>> db.define_table('mytable',Field('myfield','string'))
##
## Fields can be 'string','text','password','integer','double','boolean'
##       'date','time','datetime','blob','upload', 'reference TABLENAME'
## There is an implicit 'id integer autoincrement' field
## Consult manual for more options, validators, etc.
##
## More API examples for controllers:
##
## >>> db.mytable.insert(myfield='value')
## >>> rows=db(db.mytable.myfield=='value').select(db.mytable.ALL)
## >>> for row in rows: print row.id, row.myfield
#########################################################################

## after defining tables, uncomment below to enable auditing
# auth.enable_record_versioning(db)
