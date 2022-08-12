#! /usr/bin/python
# Copyright (C) 2006-21 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
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

import re
if __name__ != "__main__" :
    from roundup.date import Date

from roundup.exceptions             import Reject
from roundup.cgi.TranslationService import get_translation
from common                         import user_has_role

_fixed_in_patterns = \
    [ re.compile (r"^\s*[hH][eE][aA][dD]\s*$")
    , re.compile (r"^\s*0\.0(\.0)?\s*$")
    , re.compile (r"[bB][rR][aA][nN][cC][hH]")
    ]

def initial_status_ok (db, status_id, cat_id, is_simple) :
    """ Allow "escalated" when submitting new issue. This is allowed in
        case the analysis was done in advance. The first (submission)
        message should contain the analysis results.

        Allow "open" when submitting new non-cert issue. This is allowed
        in case the analysis and decision about implementation was made
        in advance, the first message should contain the analysis
        results and decision.

        Allow open for simple kind (the ones using simple_transitions).
    """
    status = db.status.get (status_id, 'name')
    if status == 'escalated' and not is_simple :
        return True
    if status == 'open' and is_simple :
        return True
    if  (   status == 'open'
        and cat_id
        and     db.category.get (cat_id, 'valid')
        and not db.category.get (cat_id, 'cert_sw')
        ) :
        return True
    return False
# end def initial_status_ok

def limit_new_entry (db, cl, nodeid, newvalues) :
    """Limit creation of new issues, check on entered fields,
       and correctly complete missing fields.
    """
    title       = newvalues.get    ("title")
    category    = None
    catid       = newvalues.get    ("category")
    if catid :
        category = db.category.getnode (catid)
    area        = newvalues.get    ("area")
    kindid      = newvalues.get    ("kind")
    responsible = newvalues.get    ("responsible")
    msg         = newvalues.get    ("messages")
    severity    = newvalues.get    ("severity")
    effort      = newvalues.get    ("effort_hours")
    part_of     = newvalues.get    ("part_of")
    try :
        bug     = db.kind.lookup   ('Bug')
    except KeyError :
        bug     = db.kind.lookup   ('Defect')
    bugname     = db.kind.get      (bug, 'name')
    analyzing   = db.status.lookup ("analyzing")

    if not kindid :
        kindid  = newvalues ['kind'] = bug
    kind        = db.kind.getnode (kindid)
    if  (  "status" not in newvalues
        or not initial_status_ok (db, newvalues ["status"], catid, kind.simple)
        ) :
        if kind.simple :
            newvalues ["status"] = db.status.lookup ('open')
        else :
            newvalues ["status"] = analyzing
    status = newvalues ["status"]

    # Default to no action for doc_issue_status for simple issues
    if kind.simple and 'doc_issue_status' not in newvalues :
        newvalues ['doc_issue_status'] = \
            db.doc_issue_status.lookup ('no documentation')

    if not category :
        catid = newvalues ['category'] = db.category.lookup ('pending')
        category = db.category.getnode (catid)
    if not area :
        try :
            area = newvalues ['area']     = db.area.lookup ('SW')
        except KeyError : pass
    if not severity :
        severity = newvalues ['severity'] = db.severity.lookup ('Minor')
    if not title :
        raise Reject (_ ('You must enter a "title".'))
    if not msg :
        field = _ ('msg')
        raise Reject \
            ( _ ("A detailed description must be given in %(field)s")
            % locals ()
            )
    if kindid == bug and 'release' not in newvalues :
        raise Reject \
            ( _ ("For a %(bugname)s you have to specify the release")
            % locals ()
            )
    if not kind.simple and status != analyzing and not effort :
        raise Reject \
            (_ ("An effort estimation is required for "
                "issues to skip analyzing"
               )
            )

    # Set `part_of` to the category default if not given.
    if not part_of :
        newvalues ["part_of"] = category.default_part_of

    # Set `responsible` to the category's responsible.
    if not responsible :
        responsible = category.responsible
        if not responsible :
            raise Reject \
                (_ ('No responsible for category "%s"') % category.name)
        newvalues ["responsible"] = responsible

    if not user_has_role (db, responsible, 'Nosy') :
        raise Reject \
            ( _ ("'%s' is not a valid user (need 'Nosy' role)!")
            % (db.user.get (responsible, "username"))
            )

    # Set `nosy` to contain the creator, the responsible,
    # and the category's nosy list.
    nosy     = newvalues.get   ("nosy", [])
    cat_nosy = category.nosy
    cat_resp = category.responsible
    addnosy  = []
    if responsible :
        addnosy.append (responsible)
    if cat_resp :
        addnosy.append (cat_resp)
    nosy     = list (set (nosy).union (cat_nosy).union (addnosy))
    newvalues ["nosy"] = nosy

    # It is meaningless to create obsolete or mistaken issues.
    if kind.name in ["Mistaken", "Obsolete"] :
        raise Reject \
            ( '[%s] It is stupid to create a new issue with a '
              'kind of "Mistaken" or "Obsolete".'
            % nodeid
            )
# end def limit_new_entry

def may_not_vanish (db, cl, nodeid, newvalues, new_status_name) :
    """Ensure that certain fields do not vanish.
    """
    for k, except_analyzing in \
        ( ('title',          False)
        , ('category',       False)
        , ('area',           False)
        , ('kind',           False)
        , ('responsible',    False)
        , ('effort_hours',   True )
        , ('severity',       False)
        ) :
        old = cl.get (nodeid, k)
        new = newvalues.get (k, old)
        if new != old and (new is None or new == '') :
            if not (except_analyzing and new_status_name == "analyzing") :
                raise Reject (_ ('The field "%s" must remain filled.') % _ (k))
# end def may_not_vanish

def limit_transitions (db, cl, nodeid, newvalues) :
    """Enforce (i.e. limit) status transitions
    """
    cur_status      = cl.get        (nodeid, "status")
    cur_status_name = db.status.get (cur_status, "name")
    new_status      = newvalues.get ("status", cur_status)
    new_status_name = db.status.get (new_status, "name")

    may_not_vanish (db, cl, nodeid, newvalues, new_status_name)

    kindid          = newvalues.get ("kind", cl.get (nodeid, "kind"))
    kind            = kind_name = None
    is_simple       = False
    if kindid :
        kind        = db.kind.getnode (kindid)
        kind_name   = kind.name
        is_simple   = kind.simple
    old_responsible = cl.get        (nodeid, "responsible")
    new_responsible = newvalues.get ("responsible", old_responsible)
    superseder      = newvalues.get ("superseder", cl.get(nodeid,"superseder"))
    is_container    = db.issue.get  (nodeid, "composed_of")
    fixed           = newvalues.get ("fixed_in", cl.get (nodeid, "fixed_in"))
    cat_id          = newvalues.get ("category", cl.get (nodeid, "category"))
    category        = db.category.getnode (cat_id)
    affected        = newvalues.get \
        ("files_affected", cl.get (nodeid, "files_affected"))
    effort          = newvalues.get \
                      ("effort_hours", cl.get (nodeid, "effort_hours"))
    msg             = newvalues.get ("messages", None)
    severity        = newvalues.get ("severity", cl.get (nodeid, "severity"))
    dis_name        = 'doc_issue_status'
    if dis_name in db.classes and dis_name in cl.properties :
        dis_id_old  = cl.get (nodeid, dis_name)
        dis_id      = newvalues.get (dis_name, dis_id_old)
        di_status   = db.doc_issue_status.getnode (dis_id)

    ############ complete the form ############

    # If a Superseder is/has been set, automatically close this issue.
    # Also close if "Obsolete" or "Mistaken".
    if superseder or kind_name in ["Mistaken", "Obsolete"] :
        if is_container :
            if  (   newvalues.get ('kind')
                and kind_name in ["Mistaken", "Obsolete"]
                ) :
                raise Reject \
                    ("A container may not be set to Mistaken or Obsolete.")
            if newvalues.get ('superseder') :
                raise Reject \
                    ("A container may not be a duplicate of another issue.")
        new_status_name = "closed"
        newvalues ["status"] = new_status = db.status.lookup (new_status_name)

    # Set `closed_date` when a bug report is being closed
    # and reset it if re-opened
    if new_status_name == "closed" and cur_status_name != "closed" :
        newvalues ["closed"] = Date (".")
    if new_status_name != "closed" and cur_status_name == "closed" :
        newvalues ["closed"] = None

    # Automatically set status "feedback" to "open" when responsible changes.
    if  (old_responsible != new_responsible) \
    and (cur_status_name == "feedback") and (new_status_name == "feedback") :
        new_status_name = "open"
        newvalues ["status"] = new_status = db.status.lookup (new_status_name)

    # Automatically clear the `fixed_in` field if testing failed.
    if cur_status_name == "testing" and new_status_name == "open" :
        newvalues ["fixed_in"] = fixed = "" # active delete

    ############ prohibit invalid changes ############

    # Direct close only allowed if mistaken, obsolete or duplicate,
    # or if it is a container or simple kind.
    if (   cur_status_name in ["open", "feedback", "suspended", "analyzing"]
       and new_status_name == "closed" and not is_simple
       ) :
        if not (  kind_name in ["Mistaken", "Obsolete"]
               or superseder
               or is_container
               ) :
            raise Reject \
                ( "[%s] To close this issue, kind must be set to "
                  "`Mistaken` or `Obsolete`, <br>or this issue must "
                  "be a duplicate of another issue or a container."
                % nodeid
                )
        if (kind_name in ["Mistaken", "Obsolete"] or superseder) and not msg :
            raise Reject \
                ("[%s] A reason in `message` must be given here." % nodeid)

    # Don't allow state change if doc_issue_status doesn't allow it
    if  (   dis_name in db.classes and dis_name in cl.properties
        and new_status_name != cur_status_name
        and not (  kind_name in ["Mistaken", "Obsolete"]
                or superseder
                or is_container
                )
        and new_status not in di_status.may_change_state_to
        ) :
            dis_name_l = _ (dis_name)
            st         = di_status.name
            raise Reject \
                ( "[%(nodeid)s] %(dis_name_l)s = %(st)s "
                  "doesn't allow state change to %(new_status_name)s"
                % locals ()
                )

    if  (   cur_status_name == "analyzing"
        and new_status_name != "analyzing"
        and not is_container
        and not is_simple
        ) :
        if new_status_name != 'closed' :
            if not kind :
                raise Reject ("Kind must be filled in for status change")
            if effort is None :
                raise Reject ("Effort must be filled in for status change")
        if new_status_name == "open" and category.cert_sw :
            if kind_name == 'Change-Request' :
                raise Reject ("No State-change to open for Change-Request")
            max_effort = int (getattr (db.config.ext, 'LIMIT_EFFORT', 8))
            if effort > max_effort :
                raise Reject \
                    (_ ("State-change to open only for "
                        "effort <= %(max_effort)s"
                       )
                    % locals ()
                    )

    # A `message` must be given whenever `responsible` changes.
    if old_responsible != new_responsible :
        if not msg :
            raise Reject \
                ( "[%s] A reason in `message` must be given to "
                  "change the `responsible`."
                % nodeid
                )
        if not user_has_role (db, new_responsible, 'Nosy') :
            raise Reject \
                ( _ ("'%s' is not a valid user (need 'Nosy' role)!")
                % (db.user.get (new_responsible, "username"))
                )

    if  (   new_status_name != cur_status_name
        and kind_name not in ('Mistaken', 'Obsolete')
        and not superseder
        and not is_container
        and not kind.simple
        ) :
        # Check if the `fixed_in` field is filled in when moving to
        # `testing` or `closed`.
        if not fixed and new_status_name in ("testing", "closed") :
            raise Reject \
                ( "[%s] The 'fixed_in' field must be set for "
                  "a transition to 'testing' or 'closed'."
                % nodeid
                )
        if not severity :
            raise Reject \
                ( "[%s] The 'severity' field must be set for this transition"
                % nodeid
                )
        if category.name == 'pending' :
            raise Reject \
                ("[%s] No status change for category 'pending'" % nodeid)

    # Check that fixed_in does not contain illegal pattern
    if 'fixed_in' in newvalues and fixed :
        for p in _fixed_in_patterns :
            if p.search (fixed) :
                raise Reject \
                    ( "[%s] %s is not allowed for the fixed_in field"
                    % (nodeid, fixed)
                    )

    # Ensure `files_affected` to be filled on certifyable products.
    if (   (  cur_status_name == "testing" and new_status_name == "closed"
           or cur_status_name == "open"    and new_status_name == "testing"
           )
       and category.cert_sw
       and not affected
       ) :
        raise Reject \
            ( "[%s] The `files_affected` field must be (or remain) "
              "set for certified software."
            % nodeid
            )

    if  (   not is_container
        and (new_status_name != cur_status_name or 'severity' in newvalues)
        ) :
        newvalues ['maturity_index'] = None # Force recomputation
# end def limit_transitions

def validate_composed_of (db, cl, nodeid) :
    """Check consistency of  `composed_of`.
       If `part_of` points not to me, remove this issue from my `composed_of`.
    """
    old_parts  = cl.get (nodeid, "composed_of")
    new_parts  = old_parts [:] # copy
    my_part_of = cl.get (nodeid, "part_of")
    for part_id in old_parts :
        if cl.get (part_id, "part_of") != nodeid \
        or part_id == nodeid \
        or part_id == my_part_of :
            new_parts.remove (part_id)
    # only set if parts really have changed
    if old_parts != new_parts :
        cl.set (nodeid, composed_of = new_parts)
# end def validate_composed_of

def part_of_changed (db, cl, nodeid, newvalues) :
    """Remove this issue from the old `part_of`.`composed_of` and
       check the old/new `part_of`.`composed_of` for consistency.
    """
    if "part_of" in newvalues :
        old_part_of_id = cl.get (nodeid, "part_of")
        new_part_of_id = newvalues.get ("part_of")
        if old_part_of_id != new_part_of_id :
            # schedule maturity_index for update
            if 'maturity_index' in cl.properties :
                newvalues ['maturity_index'] = None
            if new_part_of_id == nodeid :
                raise Reject \
                    ("[%s] `Part of` cannot point to itself." % nodeid)
            if new_part_of_id in cl.get (nodeid, "composed_of") :
                raise Reject \
                    ( "[%s] `Part of` cannot be set to an item "
                      "already in this issue's `Composed of`."
                    % nodeid
                    )
            if old_part_of_id :
                # remove this issue from old_part_of's composed_of
                parts = cl.get (old_part_of_id, "composed_of")
                # remove multiples
                parts = [x for x in parts if x != nodeid]
                cl.set (old_part_of_id, composed_of = parts)
                validate_composed_of (db, cl, old_part_of_id)
            if new_part_of_id :
                validate_composed_of (db, cl, new_part_of_id)
# end def part_of_changed

def set_default_responsible (db, cl, nodeid, newvalues) :
    """Set admin as responsible if responsible is empty.
       This auditor should be tried *after* other methods of setting a
       responsible person have failed (or are unavailable).
    """
    if 'responsible' not in newvalues :
        responsible = db.user.lookup ("admin")
        newvalues ["responsible"] = responsible
# end def set_default_responsible

def set_default_prio (db, cl, nodeid, newvalues) :
    """Set maximum prio if not yet set for a new issue.
       This auditor should be tried *after* other methods of setting a
       priority have failed.
    """
    if 'priority' not in newvalues :
        prio = db.prio.filter (None, {}, sort = ('-', 'order'))
        newvalues ['priority'] = prio [0]
# end def set_default_prio

def set_default_status (db, cl, nodeid, newvalues) :
    """Set minimum status if not yet set for a new issue.
       This auditor should be tried *after* other methods of setting a
       status have failed.
    """
    if 'status' not in newvalues :
        status = db.status.filter (None, {}, sort = ('+', 'order'))
        newvalues ['status'] = status [0]
# end def set_default_status

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    if 'issue' in db.classes :
        if 'kind' in db.classes :
            db.issue.audit ("create", limit_new_entry)
            db.issue.audit ("set",    limit_transitions)
        elif 'prio' in db.classes :
            db.issue.audit ("create", set_default_responsible, priority = 200)
            db.issue.audit ("create", set_default_status,      priority = 200)
            db.issue.audit ("create", set_default_prio,        priority = 200)
        if 'part_of' in db.issue.properties :
            db.issue.audit ("set",    part_of_changed)
    if 'it_issue' in db.classes :
        if 'part_of' in db.it_issue.properties :
            db.it_issue.audit ("set",    part_of_changed)
# end def init
