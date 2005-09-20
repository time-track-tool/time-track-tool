#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2004 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
# ****************************************************************************
# $Id$

from roundup.cgi.TranslationService import get_translation
from roundup.date                   import Date, Range
try :
    from happydoc.StructuredText import StructuredText
except ImportError :
    StructuredText = None

_ = None

if StructuredText :
    date_help  = StructuredText (Date.__doc__,  level = 1, header = 0)
    range_help = StructuredText (Range.__doc__, level = 1, header = 0)
else :
    date_help  = Date.__doc__ 
    range_help = Range.__doc__

date_text = "<br><br>Ranges are used for searching dates: A range ".join \
    ((date_help, range_help))
durations = \
    ""'''Flag if booking of durations is allowed for this %(Classname)s.'''
daily_hours = \
    ""'''Expected daily work-time for %(Classname)s for each day of
         the week. If nothing is specified, the average of Weekly
         hours is taken. The field is mainly needed for part-time
         employees with irregular work time.
      '''
work_loc = \
    ""'''Location where you worked.'''

helptext = \
    { ""'activity'                   :
      ""'''Date of last change'''
    , ""'actor'                      :
      ""'''Person who has done the last change'''
    , ""'alternate_addresses'        :
      ""'''Alternate email addresses for this user, one per line'''
    , ""'announcements'              :
      ""'''Announcements for this %(Classname)s'''
    , ""'add_announcement'           :
      ""'''Mail out an announcement for another review step'''
    , ""'author'                     :
      ""'''Author of this %(Classname)s'''
    , ""'authors'                    :
      ""'''Authors of the artefact of this %(Classname)s'''
    , ""'bookers'                    :
      ""'''Users who may book on this %(Classname)s. If nothing is
           selected here, all users may book on this %(Classname)s (e.g.,
           jour fixe).
        '''
    , ""'clearance_by'               :
      ""'''Usually the supervisor of a person approves
           time records. This can be delegated using this attribute. It
           specifies the person who approves time records for
           all people whose supervisor this is.
        '''
    , ""'company'                    :
      ""'''Company for %(Classname)s'''
    , ""'confirm'                    :
      ""'''Confirm the password here: first password and this entry
           must match.
        '''
    , ""'content'                    :
      ""'''Content of %(Classname)s'''
    , ""'cost_center_status'         :
      ""'''Specifies the Phase the Cost Center is in'''
    , ""'creation'                   :
      ""'''Record creation date'''
    , ""'creator'                    :
      ""'''Person who created this record'''
    , ""'cut_off_date'               :
      ""'''Date until when this %(Classname)s must be finished.''' + date_text
    , ""'date'                       :
      ""'''Date of this %(Classname)s.<br>''' + date_text
    , ""'daily_hours'                : daily_hours
    , ""'department'                 :
      ""'''Department in which the %(Classname)s is based, e.g., SW, Sales.'''
    , ""'deputy'                     :
      ""'''Substitute for the responsible Person of %(Classname)s'''
    , ""'description'                :
      ""'''Verbose description of %(Classname)s'''
    , ""'dist'                       :
      ""'''Distribute: In a first step you can enter Start and End time
           for each day or the hours you worked during the day. In a
           second step you can distribute these hours to the different
           work packages you worked on during the week by entering the
           work package and the number of hours into the "Distr." field.
           The remaining hours will be distributed to your time records
           which don't have a work package associated.
           This mechanism works after you press "Save" and will split a
           single time record into two if necessary.
        '''
    , ""'duration'                   :
      ""'''Work duration in hours, e.g. 7.25 -- only quarter hours
           allowed, e.g., 7.10 is not allowed. The duration is created
           automatically by the system when you specify "Start" and
           "End". Attention: If you specify both, "Start" and "Duration"
           with a duration of more than six hours, the system will
           consult your user preferences and add the lunch break, e.g.
           specifying "Start" 10:00 and "Duration" 8 will result in an
           "End" time of 18:30.
        '''
    , ""'user_dynamic.durations_allowed' : durations
    , ""'vacation_remaining'         :
      ""'''Remaining vacation for this user at the start of a dynamic
           user data record.
        '''
    , ""'vacation_yearly'            :
      ""'''Yearly vacation for this user: This is the amount of vacation
           that is added for each year.
        '''
    , ""'wp.durations_allowed'       : durations +
      ""'''This is mainly used for special %(Classname)ss, like,
           e.g., vacation.
        '''
    , ""'email'                      :
      ""'''Email address for this %(Classname)s'''
    , ""'end'                        :
      ""'''Format xx:xx  (e.g. 17:00), is created automatically by the
           system when you specify "Start" and "Duration". Attention: If
           you specify both, "Start" and "End", with more than six hours
           in between, the system will consult your user preferences and
           subtract the lunch break, e.g. specifying "Start" 10:00 and
           "End" 18:00 will result in a duration of 7.5 hours (because
           half an hour lunch break was subtracted).
        '''
    , ""'external_phone'             :
      ""'''Short mobile or external phone number, e.g., 6142.
           Can be concatenated with
           the company prefix stored in "Organisation" to form a valid
           external phone number.
        '''
    , ""'add_file'                   :
      ""'''Add an new file for %(Classname)s'''
    , ""'files'                      :
      ""'''Files for %(Classname)s'''
    , ""'final_meeting_date'         :
      ""'''Date of final meeting for this %(Classname)s.''' + date_text
    , ""'firstname'                  :
      ""'''First name for this user, e.g., Ralf'''
    , ""'hours_mon'                  : daily_hours
    , ""'hours_tue'                  : daily_hours
    , ""'hours_wed'                  : daily_hours
    , ""'hours_thu'                  : daily_hours
    , ""'hours_fri'                  : daily_hours
    , ""'hours_sat'                  : daily_hours
    , ""'hours_sun'                  : daily_hours
    , ""'id'                         :
      ""'''ID of this record, automatically generated by the system.
           Cannot be changed by the user.
        '''
    , ""'initial'                    :
      ""'''Initials of this %(Classname)s'''
    , ""'inreplyto'                  :
      ""'''In Reply To field if this %(Classname)s was received by email'''
    , ""'is_alias'                   :
      ""'''No real user but only an email alias'''
    , ""'klass'                      :
      ""'''Class for this query'''
    , ""'lastname'                   :
      ""'''Last name for this user, e.g., Schlatterbeck'''
    , ""'location'                   :
      ""'''Location of %(Classname)s, e.g., Vienna HQ.'''
    , ""'lunch_duration'             :
      ""'''Preference for time tracking, duration of lunch break in minutes'''
    , ""'lunch_start'                :
      ""'''Preference for time tracking, start of lunch break'''
    , ""'manager'                    :
      ""'''Responsible person of the %(Classname)s'''
    , ""'messageid'                  :
      ""'''Message-ID if this message was received via email'''
    , ""'messages'                   :
      ""'''List of messages for %(Classname)s'''
    , ""'msg'                        :
      ""'''New message or notice for %(Classname)s'''
    , ""'name'                       :
      ""'''Unique %(Classname)s name'''
    , ""'nickname'                   :
      ""'''Nickname (or short name) for this %(Classname)s, e.g., rsc'''
    , ""'nosy'                       :
      ""'''People receiving announcements (messages) for %(Classname)s'''
    , ""'opt_reviewers'              :
      ""'''Optional reviewers for this %(Classname)s'''
    , ""'order'                      :
      ""'''Items are ordered by this property in drop-down boxes etc.'''
    , ""'organisation'               :
      ""'''Organisation in which the %(Classname)s is based, e.g., TTTech.'''
    , ""'password'                   :
      ""'''Password for this %(Classname)s'''
    , ""'peer_reviewers'             :
      ""'''Peer reviewers for this %(Classname)s'''
    , ""'phone'                      :
      ""'''Short phone number (suffix) only, e.g., 42.
           Can be concatenated with
           the company prefix stored in "Organisation" to form a valid
           external phone number.
        '''
    , ""'planned_effort'             :
      ""'''Effort for the %(Classname)s in person-days; as it is stated
           in the Project Evaluation Sheet.
        '''
    , ""'private_for'                :
      ""'''Flag if this is a private %(Classname)s'''
    , ""'private_phone'              :
      ""'''Privat phone number. Always as a full number valid on the
           PSTN.
        '''
    , ""'project'                    :
      ""'''%(Classname)s is part of a Project. With the Project name a
           %(Classname)s can be clearly  identified
        '''
    , ""'qa_representative'          :
      ""'''Representative from the QA department for this %(Classname)s'''
    , ""'queries'                    :
      ""'''Queries for this %(Classname)s'''
    , ""'recorder'                   :
      ""'''Person responsible for recording findings'''
    , ""'realname'                   :
      ''"""Real name for this %(Classname)s -- automatically generated
           by the system from first and last name. Needed by roundup
           internally. (More specifically by roundupdp.py's send_message
           -- which is used e.g. by the nosyreactor)
        """
    , ""'recipients'                 :
      ""'''Only set if message was received via email.'''
    , ""'remove'                     :
      ""'''Remove attached item. Will not remove item from the database,
           it can usually still be downloaded via the History button.
        '''
    , ""'responsible'                :
      ""'''Person who is responsible for the %(Classname)s'''
    , ""'review.responsible'         :
      ""'''Moderator for %(Classname)s -- Note: If you do not specify
           the moderator, you will get an indication that the field
           "Responsible" must be filled in -- the moderator is reponsible for
           %(Classname)s.
        '''
    , ""'roles'                      :
      ""'''Roles for this %(Classname)s -- to give the user more than
           one role, enter a comma,separated,list
        '''
    , ""'room'                       :
      ""'''Room number'''
    , ""'start'                      :
      ""'''Format xx:xx (e.g. 09:00), defines your start of work. Has to
           be specified except for absences like e.g. holidays or sick
           leave.
        '''
    , ""'status'                     :
      ""'''Status of this %(Classname)s'''
    , ""'subject'                    :
      ""'''Short identification of this message'''
    , ""'substitute'                 :
      ""'''Person who can substitute %(Classname)s for approving time
           records.
        '''
    , ""'subst_active'               :
      ""'''This field is set to "yes" for enabling the field
           "Substitute" for delegating time record approval.
        '''
    , ""'summary'                    :
      ""'''Short summary of this message (usually first line)'''
    , ""'superior'                   :
      ""'''Supervisor for %(Classname)s'''
    , ""'team_members'               :
      ""'''Persons who are assigned to the project and are allowed
           to book their effort on this project
        '''
    , ""'time_activity'              :
      ""'''Specifies the kind of work you did (e.g. meeting, ...)'''
    , ""'time_start'                 :
      ""'''Date when %(Classname)s officially starts'''
    , ""'time_end'                   :
      ""'''Date when %(Classname)s is officially closed'''
    , ""'timezone'                   :
      ""'''Time zone of this %(Classname)s -- this is a numeric hour offset'''
    , ""'title'                      :
      ""'''Title of this %(Classname)s'''
    , ""'type'                       :
      ""'''Mime type of this file'''
    , ""'url'                        :
      ""'''Web-Link for this %(Classname)s'''
    , ""'user.address'               :
      ""'''Primary email address for this user'''
    , ""'user.title'                 :
      ""'''Academic title of %(Classname)s, e.g., Dipl. Ing.'''
    , ""'username'                   :
      ""'''Login-name for this %(Classname)s, e.g., schlatterbeck'''
    , ""'valid_from'                 :
      ""'''Creation date, or date since when this %(Classname)s can be
           booked at
        ''' + date_text
    , ""'valid_to'                   :
      ""'''Expiration date for %(Classname)s.''' + date_text
    , ""'week'                       :
      ""'''Week for time tracking, this is an alternative for specifying
           a date range: just enter the week number here (for the
           current year) or YYYY/WW where YYYY is the year and WW the
           week number for that year.
      '''
    , ""'weekend_allowed'            :
      ""'''Flag if booking on weekends is allowed for this %(Classname)s.'''
    , ""'weekly_hours'               :
      ""'''Expected weekly work-time for %(Classname)s.'''
    , ""'wp_no'                      :
      ""'''Work package number in the project. Number must be unique for
           the project and cannot be changed after assignment.
        '''
    , ""'wp'                         :
      ""'''Only work packages where you have permission to register show
           here. If you miss one, please contact the responsible project
           manager
        '''
    , ""'wps'                        :
      ""'''For a better handling of the work load of a project it is
           split in to work packages. This field defines a list of work
           packages for this %(Classname)s
        '''
    , ""'work_location'              : work_loc
    , ""'time_project.work_location' : work_loc +
      ""''' If a value is given here, the work location will be
           corrected for all time records booked on work packages of
           this project.
        '''
    }

def combined_name (cls, attr) :
    """ Produce a combined name of class and attribute of the class. If
        a help-text exists for the combination, return the combination,
        otherwise return only the attribute. In this way we can override
        help-texts by specifying a help-text entry with the key
        classname.attribute.
    """
    pname = '%s.%s' % (cls, attr)
    if pname in helptext :
        return pname
    return attr
# end def combined_name

def help_properties (klass) :
    """Return all class properties plus some more for which help texts
       should be displayed (e.g., "message" which describes the message
       window). The parameter klass is a html klass.
    """
    p = []
    properties = klass._klass.getprops ()
    if 'messages' in properties :
        p.append ('msg')
    if klass.classname == 'user' :
        p.append ('confirm')
    if klass.classname == 'daily_record' :
        p.append ('week')
    if klass.classname == 'file' :
        p.append (""'remove')
    if klass.classname == 'user_dynamic' :
        p.append (""'daily_hours')
    if 'announcements' in properties :
        p.append ('add_announcement')
    if 'files' in properties :
        p.append ('add_file')
    for i in properties.iterkeys () :
        pname = combined_name (klass.classname, i)
        if pname in helptext :
            p.append (pname)
    p = [(_ (i).decode ('utf-8'), i) for i in p]
    p.sort ()
    return [i [1] for i in p]
# end def help_properties

def fieldname (cls, name, fieldname = None, space = True) :
    nbsp = ['&nbsp;', ''][not space]
    if not fieldname : fieldname = name
    prop = combined_name (cls, fieldname)
    if not prop in helptext :
        return "%s%s" % (_ (prop), nbsp)
    return "<a href=\"javascript:help_window" \
           "('%s?:template=property_help#%s', '500', '400')\">" \
           "%s%s</a>" \
           % (cls, prop, _ (prop), nbsp)

# end def fieldname

def init (instance) :
    global _
    _   = get_translation \
        (instance.config.TRACKER_LANGUAGE, instance.tracker_home).gettext
    instance.registerUtil ('helptext',        helptext)
    instance.registerUtil ('help_properties', help_properties)
    instance.registerUtil ('fieldname',       fieldname)
# end def init
