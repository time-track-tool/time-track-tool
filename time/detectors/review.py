# -*- coding: iso-8859-1 -*-
# Copyright (C) 2005 TTTech Computertechnik AG. All rights reserved
# Schönbrunnerstraße 7, A--1040 Wien, Austria. office@mexx.mobile
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
#
#++
# Name
#    review
#
# Purpose
#    All Online Peer Review related detectors
#
# Revision Dates
#     6-Apr-2005 (MPH) Creation
#    ««revision-date»»···
#--
#

from roundup import roundupdb, hyperdb
from roundup.exceptions import Reject

def union (* lists) :
    """Compute the union of lists.
    """
    tab = {}
    for l in lists :
        map (lambda x, tab = tab : tab.update  ({x : 1}), l)
    return tab.keys ()
# end def union

def audit (db, cl, nodeid, new_values) :
    pass

def react (db, cl, nodeid, old_values) :
    pass

def update_nosy_review (db, cl, nodeid, new_values) :
    # update the nosy list
    # nosy list is all links to users + who's already in the nosy list.
    nv    =  new_values
    nosy  =  nv.get ("nosy", [])
    if nodeid is None :
        nosy +=  nv.get ("authors"          , [])
        nosy +=  nv.get ("peer_reviewers"   , [])
        nosy +=  nv.get ("opt_reviewers"    , [])
        nosy += [nv.get ("responsible"      , [])]
        nosy += [nv.get ("recorder"         , [])]
        nosy += [nv.get ("qa_representative", [])]
    else :
        nosy +=  cl.get (nodeid, "nosy")
        nosy +=  nv.get ("authors"          , cl.get (nodeid, "authors")       )
        nosy +=  nv.get ("peer_reviewers"   , cl.get (nodeid, "peer_reviewers"))
        nosy +=  nv.get ("opt_reviewers"    , cl.get (nodeid, "opt_reviewers") )
        nosy += [nv.get ("responsible"      , cl.get (nodeid, "responsible")   )]
        nosy += [nv.get ("recorder"         , cl.get (nodeid, "recorder")      )]
        nosy += [nv.get ("qa_representative", cl.get (nodeid, "qa_representative"))]

    new_values ["nosy"] = union (nosy)
# end def update_nosy_review

def new_announcement (db, cl, nodeid, new_values) :
    """auditor on announcement's create
    """
    if not new_values.get ("title") :
        raise Reject, "Required announcement property title not supplied"
    if not new_values.get ("version") :
        raise Reject, "Required announcement property version not supplied"
    if not new_values.get ("location") :
        raise Reject, "Required announcement property location not supplied"
    new_values ["status"] = db.review_status.lookup ("open")
# end def new_announcement

def backlink_announcement (db, cl, nodeid, old_values) :
    """reactor review.set

    scans all announcements attached to this review, and updates their
    `review` backlink
    """
    old_anns   = old_values.get ("announcements", [])
    new_anns   = cl.get (nodeid, "announcements")
    added_anns = [a for a in new_anns if a not in old_anns]
    anns_new_values = {}
    for new_ann_id in added_anns :
        anns_new_values.update        ({"review" : nodeid})

        # set nosy list on the announcement to review's nosy list
        reviews_nosy = db.review.get  (nodeid, "nosy")
        anns_new_values.update        ({"nosy" : reviews_nosy})

        # set responsible to creator
        creator = db.announcement.get (new_ann_id, "creator")
        anns_new_values.update        ({"responsible" : creator})

        print "anns_new_values", new_ann_id, anns_new_values
        db.announcement.set (new_ann_id, **anns_new_values)
# end def backlink_announcement

def backlink_comment (db, cl, nodeid, old_values) :
    """reactor announcement.set

    scans all comments attached to this announcement, and updates their
    `announcement` backlink
    """
    old_comments   = old_values.get ("comments", [])
    new_comments   = cl.get         (nodeid, "comments")
    added_comments = [c for c in new_comments if c not in old_comments]

    comments_new_values = {}
    for new_comment_id in added_comments :
        comments_new_values.update ({"announcement" : nodeid})

        # set nosy list on the comment to creator + review's authors
        review_id       = cl.get         (nodeid        , "review" )
        reviews_authors = db.review.get  (review_id     , "authors")
        creator         = db.comment.get (new_comment_id, "creator")
        comments_new_values.update \
            ({"nosy" : union (reviews_authors, [creator])})

        # set responsible to the first selected author
        comments_new_values.update ({"responsible" : reviews_authors [0]})

        # let comment point back to review, to make "easy" queries possible
        comments_new_values.update ({"review" : review_id})
        db.comment.set (new_comment_id, **comments_new_values)
# end def backlink_comment

def new_comment (db, cl, nodeid, new_values) :
    """auditor for new comment
    """
    if not new_values.get ("title") :
        raise Reject, "Required comment property title not supplied"
    if not new_values.get ("severity") :
        raise Reject, "Required comment property severity not supplied"
    new_values ["status"] = db.comment_status.lookup ("assigned")
# end def new_comment


def init (db) :
    # fire before changes are made
    db.review.audit       ("set"   , update_nosy_review)
    db.review.audit       ("create", update_nosy_review)
    db.review.react       ("set"   , backlink_announcement)
    db.announcement.audit ("create", new_announcement)
    db.announcement.react ("set"   , backlink_comment)
    db.comment.audit      ("create", new_comment)

### __END__ review


