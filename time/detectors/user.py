# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@tttech.com
#
#++
# Name
#    user
#
# Purpose
#    Detectors for user class
#
# Revision Dates
#    14-Oct-2004 (MPH) Creation
#     9-Nov-2004 (MPH) Renamed to user.py
#    ««revision-date»»···
#--
#
def audit_user_fields(db, cl, nodeid, new_values):
    ''' Make sure user properties are valid.
        - email address has no spaces in it
        - roles specified exist

        TODO:
        - email address matches TTTspec (and optionally auto-generate)
          - firstname.lastname@tttech.com
          - lastname@tttech.com
          - (fla@tttech.com) # not implemented


    '''
    if new_values.has_key('address') and ' ' in new_values['address']:
        raise ValueError, 'Email address must not contain spaces'

    if new_values.has_key('roles'):
        roles = [x.lower().strip() for x in new_values['roles'].split(',')]
        for rolename in roles:
            if not db.security.role.has_key(rolename):
                raise ValueError, 'Role "%s" does not exist'%rolename

    # automatic setting of realname
    if new_values.has_key ("firstname") \
        or new_values.has_key ("lastname") \
        and nodeid :
        fn = new_values.get ("firstname", cl.get (nodeid, "firstname"))
        ln = new_values.get ("lastname" , cl.get (nodeid, "lastname"))
        realname = " ".join ((fn, ln))
        new_values ["realname"] = realname
# end def audit_user_fields

def init(db):
    # fire before changes are made
    db.user.audit('set'   , audit_user_fields)
    db.user.audit('create', audit_user_fields)

# vim: set filetype=python ts=4 sw=4 et si
