#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2006 Dr. Ralf Schlatterbeck Open Source Consulting.
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

_effort_pattern = r"(\d+) \s* ([PM][DWM]) (?:\s+ \(([^)]+)\))?"
_effort_regex   = re.compile (_effort_pattern, re.VERBOSE)

_fixed_in_patterns = \
    [ re.compile (r"^\s*[hH][eE][aA][dD]\s*$")
    , re.compile (r"^\s*0\.0(\.0)?\s*$")
    , re.compile (r"[bB][rR][aA][nN][cC][hH]")
    ]

def union (* lists) :
    """Compute the union of lists.
    """
    tab = {}
    for l in lists :
        map (lambda x, tab = tab : tab.update  ({x : 1}), l)
    return tab.keys ()
# end def union

def initial_status_ok (db, status_id, cat_id) :
    """ Allow "escalated" when submitting new issue. This is allowed in
        case the analysis was done in advance. The first (submission)
        message should contain the analysis results.

        Allow "open" when submitting new non-cert issue. This is allowed
        in case the analysis and decision about implementation was made
        in advance, the first message should contain the analysis
        results and decision.
    """
    status = db.status.get (status_id, 'name')
    if status == 'escalated' :
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
    category    = newvalues.get    ("category")
    area        = newvalues.get    ("area")
    kind        = newvalues.get    ("kind")
    responsible = newvalues.get    ("responsible")
    msg         = newvalues.get    ("messages")
    severity    = newvalues.get    ("severity")
    effort      = newvalues.get    ("effort")
    bug         = db.kind.lookup   ('Bug')
    analyzing   = db.status.lookup ("analyzing")

    if  (  "status" not in newvalues
        or not initial_status_ok (db, newvalues ["status"], category)
        ) :
        newvalues ["status"] = analyzing
    status = newvalues ["status"]

    if not category :
        category = newvalues ['category'] = db.category.lookup ('pending')
    if not area :
        try :
            area = newvalues ['area']     = db.area.lookup ('SW')
        except KeyError : pass
    if not kind :
        kind     = newvalues ['kind']     = bug
    if not severity :
        severity = newvalues ['severity'] = db.severity.lookup ('Minor')
    if not title :
        raise Reject, _ ('You must enter a "title".')
    if not msg :
        field = _ ('msg')
        raise Reject, _ ("A detailed description must be given in %(field)s") \
                        % locals ()
    if kind == bug and 'release' not in newvalues :
        raise Reject, _ ("For bugs you have to specify the release")
    if status != analyzing and not effort :
        raise Reject, \
            _ ("An effort estimation is required for issues to skip analyzing")

    # Set `responsible` to the category's responsible.
    if not responsible :
        responsible = db.category.get (category, "responsible")
        newvalues ["responsible"] = responsible

    # Set `nosy` to contain the creator, the responsible,
    # and the category's nosy list.
    nosy     = newvalues.get   ("nosy", [])
    cat_nosy = db.category.get (category, "nosy")
    cat_resp = db.category.get (category, "responsible")
    creator  = newvalues.get   ("creator")
    nosy     = union (nosy, cat_nosy, [creator, responsible, cat_resp])
    newvalues ["nosy"] = filter (None, nosy)

    # It is meaningless to create obsolete or mistaken issues.
    kind_name = db.kind.get (kind, "name")
    if kind_name in ["Mistaken", "Obsolete"] :
        raise Reject, ( '[%s] It is stupid to create a new issue with a '
                        'kind of "Mistaken" or "Obsolete".'
                      % nodeid
                      )

    check_effort (newvalues)
    # Do not allow `files_affected` to be filled in initially.
    # XXX Maybe we need this somewhen in future.
# end def limit_new_entry

def check_effort (newvalues) :
    effort = newvalues.get ("effort")
    if effort and not _effort_regex.match (effort) :
        raise Reject, ( "The `effort` field must have the format "
                        "`\\d+ [PM][DWM]`, e.g. `12 PD`."
                      )
# end def check_effort

def may_not_vanish (db, cl, nodeid, newvalues, new_status_name) :
    """Ensure that certain fields do not vanish.
    """
    for k, except_analyzing in \
        ( ('title'      , False)
        , ('category'   , False)
        , ('area'       , False)
        , ('kind'       , False)
        , ('responsible', False)
        , ('effort'     , True )
        , ('severity'   , False)
        ) :
        old = cl.get (nodeid, k)
        new = newvalues.get (k, old)
        if new != old and not new :
            if not (except_analyzing and new_status_name == "analyzing") :
                raise Reject, _ ('The field "%s" must remain filled.') % _ (k)
# end def may_not_vanish

def limit_transitions (db, cl, nodeid, newvalues) :
    """Enforce (i.e. limit) status transitions
    """
    cur_status      = cl.get        (nodeid, "status")
    cur_status_name = db.status.get (cur_status, "name")
    new_status      = newvalues.get ("status", cur_status)
    new_status_name = db.status.get (new_status, "name")

    may_not_vanish (db, cl, nodeid, newvalues, new_status_name)

    kind            = newvalues.get ("kind", cl.get (nodeid, "kind"))
    kind_name       = kind and db.kind.get (kind, "name") or ""
    old_responsible = cl.get        (nodeid, "responsible")
    new_responsible = newvalues.get ("responsible", old_responsible)
    superseder      = newvalues.get ("superseder", cl.get(nodeid,"superseder"))
    is_container    = db.issue.get  (nodeid, "composed_of")
    fixed           = newvalues.get ("fixed_in", cl.get (nodeid, "fixed_in"))
    cat_id          = newvalues.get ("category", cl.get (nodeid, "category"))
    category        = db.category.getnode (cat_id)
    affected        = newvalues.get \
        ("files_affected", cl.get (nodeid, "files_affected"))
    effort          = newvalues.get ("effort", cl.get (nodeid, "effort"))
    msg             = newvalues.get ("messages", None)
    severity        = newvalues.get ("severity", cl.get (nodeid, "severity"))

    ############ complete the form ############

    # If a Superseder is/has been set, automatically close this issue.
    # Also close if "Obsolete" or "Mistaken".
    if superseder or kind_name in ["Mistaken", "Obsolete"] :
        new_status_name = "closed"
        newvalues ["status"] = new_status = db.status.lookup (new_status_name)

    # Set `closed_date` when a bug report is being closed.
    if new_status_name == "closed" and cur_status_name != "closed" :
        newvalues ["closed"] = Date (".")

    # Automatically set status "feedback" to "open" when responsible changes.
    if  (old_responsible != new_responsible) \
    and (cur_status_name == "feedback") and (new_status_name == "feedback") :
        new_status_name = "open"
        newvalues ["status"] = new_status = db.status.lookup (new_status_name)

    # Automatically clear the `fixed_in` field if testing failed.
    if cur_status_name == "testing" and new_status_name == "open" :
        newvalues ["fixed_in"] = fixed = "" # active delete

    check_effort (newvalues)

    ############ prohibit invalid changes ############

    # Direct close only allowed if mistaken, obsolete or duplicate,
    # or if it is a container.
    if (   cur_status_name in ["open", "feedback", "suspended", "analyzing"]
       and new_status_name == "closed"
       ) :
        if not (  kind_name in ["Mistaken", "Obsolete"]
               or superseder
               or is_container
               ) :
            raise Reject, ( "[%s] To close this issue, kind must be set to "
                            "`Mistaken` or `Obsolete`, <br>or this issue must "
                            "be a duplicate of another issue or a container."
                          % nodeid
                          )
        if (kind_name in ["Mistaken", "Obsolete"] or superseder) and not msg :
            raise Reject, ( "[%s] A reason in `message` must be given here."
                          % nodeid
                          )

    if  (   cur_status_name == "analyzing"
        and new_status_name != "analyzing"
        and not is_container
        ) :
        if new_status_name != 'closed' :
            if not kind :
                raise Reject, "Kind must be filled in for status change"
            if not effort :
                raise Reject, "Effort must be filled in for status change"
        if new_status_name == "open" and category.cert_sw :
            if kind_name == 'Change-Request' :
                raise Reject, "No State-change to open for Change-Request"
            m = _effort_regex.match (effort)
            # > 1 PD ?
            if not m.group (2).endswith ('D') or int (m.group (1)) > 1 :
                raise Reject, "State-change to open only for effort < 1PD"

    # A `message` must be given whenever `responsible` changes.
    if old_responsible != new_responsible and not msg :
        raise Reject, ( "[%s] A reason in `message` must be given to "
                        "change the `responsible`."
                      % nodeid
                      )

    if  (   new_status_name != cur_status_name
        and kind_name not in ('Mistaken', 'Obsolete')
        and not superseder
        and not is_container
        ) :
        # Check if the `fixed_in` field is filled in when moving to
        # `testing` or `closed`.
        if not fixed and new_status_name in ("testing", "closed") :
            raise Reject, ( "[%s] The 'fixed_in' field must be set for "
                            "a transition to 'testing' or 'closed'."
                          % nodeid
                          )
        if not severity :
            raise Reject, ( "[%s] The 'severity' field must be set for "
                            "this transition"
                          % nodeid
                          )
        if category.name == 'pending' :
            raise Reject, ( "[%s] No status change for category 'pending'"
                          % nodeid
                          )

    # Check that fixed_in does not contain illegal pattern
    if 'fixed_in' in newvalues and fixed :
        for p in _fixed_in_patterns :
            if p.search (fixed) :
                raise Reject, ( "[%s] %s is not allowed for the fixed_in field"
                              % (nodeid, fixed)
                              )

    # Ensure `files_affected` to be filled on certifyable products.
    if (   (  cur_status_name == "testing" and new_status_name == "closed"
           or cur_status_name == "open"    and new_status_name == "testing"
           )
       and category.cert_sw
       and not affected
       ) :
        raise Reject, ( "[%s] The `files_affected` field must be (or remain) "
                        "set for certified software."
                      % nodeid
                      )

    if  (   not is_container
        and (new_status_name != cur_status_name or 'severity' in newvalues)
        ) :
        newvalues ['maturity_index'] = None # Force recomputation

    # If the `files_affected` field ist filled, it must be in a certain manner.
    # XXX To be implemented when RMA or GST come up with the Regex needed here.
# end def limit_transitions

def validate_composed_of (db, nodeid) :
    """Check consistency of  `composed_of`.
       If `part_of` points not to me, remove this issue from my `composed_of`.
    """
    old_parts  = db.issue.get (nodeid, "composed_of")
    new_parts  = old_parts [:] # copy
    my_part_of = db.issue.get (nodeid, "part_of")
    for part_id in old_parts :
        if db.issue.get (part_id, "part_of") != nodeid \
        or part_id == nodeid \
        or part_id == my_part_of :
            new_parts.remove (part_id)
    # only set if parts really have changed
    if old_parts != new_parts :
        db.issue.set (nodeid, composed_of = new_parts)
# end def validate_composed_of

def part_of_changed (db, cl, nodeid, newvalues) :
    """Remove this issue from the old `part_of`.`composed_of` and
       check the old/new `part_of`.`composed_of` for consistency.
    """
    if newvalues.has_key ("part_of"):
        old_part_of_id = cl.get (nodeid, "part_of")
        new_part_of_id = newvalues.get ("part_of")
        if old_part_of_id != new_part_of_id :
            # schedule maturity_index for update
            newvalues ['maturity_index'] = None
            if new_part_of_id == nodeid :
                raise Reject, ( "[%s] `Part of` cannot point to itself."
                              % nodeid
                              )
            if new_part_of_id in db.issue.get (nodeid, "composed_of") :
                raise Reject, ( "[%s] `Part of` cannot be set to an item "
                                "already in this issue's `Composed of`."
                              % nodeid
                              )
            if old_part_of_id :
                # remove this issue from old_part_of's composed_of
                parts = db.issue.get (old_part_of_id, "composed_of")
                # remove multiples
                parts = filter (lambda x: x != nodeid, parts)
                db.issue.set (old_part_of_id, composed_of = parts)
                validate_composed_of (db, old_part_of_id)
            if new_part_of_id :
                validate_composed_of (db, new_part_of_id)
# end def part_of_changed

def init (db) :
    global _
    _   = get_translation \
        (db.config.TRACKER_LANGUAGE, db.config.TRACKER_HOME).gettext
    if 'issue' not in db.classes :
        return
    db.issue.audit ("create", limit_new_entry)
    db.issue.audit ("set",    limit_transitions)
    db.issue.audit ("set",    part_of_changed)
# end def init
