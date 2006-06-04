#! /usr/bin/python
# Copyright (C) 1998 TTTech Computertechnik GmbH. All rights reserved
# Schoenbrunnerstrasse 7, A--1040 Wien, Austria. office@@tttech.com
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

import re
if __name__ != "__main__" :
    from roundup.date import Date

Reject          = ValueError # see roundup/cgi/client.py, line 698
_effort_pattern = r"(\d+) \s* ([PM][DWM]) (?:\s+ \(([^)]+)\))?"
_effort_regex   = re.compile (_effort_pattern, re.VERBOSE)

_fixed_in_patterns = \
    [ re.compile (r"^\s*[hH][eE][aA][dD]\s*$")
    , re.compile (r"^\s*0\.0(\.0)?\s*$")
    , re.compile (r"[bB][rR][aA][nN][cC][hH]")
    ]

# <old_state> : [(<new_state>, <responsibility_change>, <require_msg>), ...]
sm = { "open"      : [ ("analyzed",   0, 1)
                     , ("feedback",   1, 1)
                     , ("testing",    1, 1)
                     , ("suspended",  0, 1)
                     , ("closed",     0, 0) # guarded by `limit_transitions`
                     ]
     , "analyzed"  : [ ("open",       0, 1)
                     , ("feedback",   1, 1)
                     , ("testing",    1, 1)
                     , ("suspended",  0, 1)
                     ]
     , "feedback"  : [ ("open",       1, 1)
                     , ("closed",     0, 1)
                     ]
     , "testing"   : [ ("open",       0, 1)
                     , ("closed",     0, 0)
                     ]
     , "suspended" : [ ("open",       0, 0)
                     , ("closed",     0, 1)
                     ]
     , "closed"    : [ ("open",       0, 1)
                     ]
     }

# Certified software categories which need special handling.
cert_sw = \
    [ "Bootloader"
    , "Cert-Bootloader"
    , "Cert-OS"
    , "Cert-Verify"
    , "Cert-Chip"
    , "TTP-OS"
    , "TTP-Verify"
    , "BSP"
    ]

def union (* lists) :
    """Compute the union of lists.
    """
    tab = {}
    for l in lists :
        map (lambda x, tab = tab : tab.update  ({x : 1}), l)
    return tab.keys ()
# end def union

def limit_new_entry (db, cl, nodeid, newvalues) :
    """Limit creation of new issues, check on entered fields,
       and correctly complete missing fields.
    """
    title       = newvalues.get ("title",       None)
    category    = newvalues.get ("category",    None)
    area        = newvalues.get ("area",        None)
    kind        = newvalues.get ("kind",        None)
    responsible = newvalues.get ("responsible", None)
    msg         = newvalues.get ("messages",    None)

    # Ensure that `title`, `category`, `area`, `kind`, and `message` are set.
    if not category :
        category = newvalues ['category'] = db.category.lookup ('pending')
    if not area :
        area     = newvalues ['area']     = db.area.lookup ('SW')
    if not kind :
        kind     = newvalues ['kind']     = db.kind.lookup ('Bug')
    if not title :
        raise Reject, '[%s] You must enter a "title".' % nodeid
    if not msg :
        raise Reject, ( "[%s] A detailed description must be given in "
                        "`message`."
                      % nodeid
                      )

    # For IT issues in category 'helpdesk-it' we want them to be part_of
    # issue 11600 automagically. We can't do this in the email gateway
    # due to a bug in the installed version of roundup, so we do it
    # here.
    
    if  (   category == db.category.lookup ('helpdesk-it')
        and not newvalues.has_key ('part_of')
        ) :
        newvalues ['part_of'] = '11600'

    # Set `responsible` to the category's responsible.
    if not responsible :
        responsible = db.category.get (category, "responsible")
        newvalues ["responsible"] = responsible

    # Set `nosy` to contain the creator, the responsible,
    # and the category's nosy list.
    nosy     = newvalues.get   ("nosy", [])
    cat_nosy = db.category.get (category, "nosy")
    creator  = newvalues.get   ("creator", None)
    nosy     = union (nosy, cat_nosy, [creator, responsible])
    if None in nosy :
        nosy.remove (None)
    newvalues ["nosy"] = nosy

    # Set `status` strictly to "open"
    newvalues ["status"]   = db.status.lookup ("open")

    # It is meaningless to create obsolete or mistaken issues.
    kind_name = db.kind.get (kind, "name")
    if kind_name in ["Mistaken", "Obsolete"] :
        raise Reject, ( '[%s] It is stupid to create a new issue with a '
                        'kind of "Mistaken" or "Obsolete".'
                      % nodeid
                      )

    # Check for correct format of `effort`. (same as in `limit_transitions`)
    effort = newvalues.get ("effort", None)
    if effort and not _effort_regex.match (effort) :
        raise Reject, ( "[%s] The `effort` field must have the format "
                        "`\\d+ [PM][DWM]`, e.g. `12 PD`."
                      % nodeid
                      )
    # Do not allow `files_affected` to be filled in initially.
    # XXX Maybe we need this somewhen in future.
# end def limit_new_entry

def may_not_vanish (db, cl, nodeid, newvalues) :
    """Ensure that certain fields do not vanish.
    """
    title       = newvalues.get ("title",       cl.get (nodeid, "title"))
    category    = newvalues.get ("category",    cl.get (nodeid, "category"))
    area        = newvalues.get ("area",        cl.get (nodeid, "area"))
    kind        = newvalues.get ("kind",        cl.get (nodeid, "kind"))
    responsible = newvalues.get ("responsible", cl.get (nodeid, "responsible"))
    if not title or not category or not area or not kind or not responsible :
        raise Reject, ( "[%s] The fields `title`, `category`, `area`, "
                        "`kind` <br> and `responsible` must remain filled."
                      % nodeid
                      )
# end def may_not_vanish

def limit_transitions (db, cl, nodeid, newvalues) :
    """Enforce (i.e. limit) status transitions to what is defined in the
       state machine `sm`.
    """
    may_not_vanish (db, cl, nodeid, newvalues)

    cur_status      = cl.get        (nodeid, "status")
    cur_status_name = db.status.get (cur_status, "name")
    new_status      = newvalues.get ("status", cur_status)
    new_status_name = db.status.get (new_status, "name")
    kind            = newvalues.get ("kind", cl.get (nodeid, "kind"))
    kind_name       = kind and db.kind.get (kind, "name") or ""
    old_responsible = cl.get        (nodeid, "responsible")
    new_responsible = newvalues.get ("responsible", old_responsible)
    superseder      = newvalues.get ("superseder", cl.get(nodeid,"superseder"))
    is_container    = db.issue.get  (nodeid, "composed_of")
    fixed           = newvalues.get ("fixed_in", cl.get (nodeid, "fixed_in"))
    category        = newvalues.get ("category", cl.get (nodeid, "category"))
    category_name   = category and db.category.get (category, "name") or ""
    affected        = newvalues.get \
        ("files_affected", cl.get (nodeid, "files_affected"))
    effort          = newvalues.get ("effort", None)
    msg             = newvalues.get ("messages", None)

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

    ############ prohibit invalid changes ############
    
    # Prohibit invalid transitions of `status`.
    to_stati = [s for (s, r, m) in sm [cur_status_name]]
    if  new_status != cur_status \
    and new_status not in [db.status.lookup (s) for s in to_stati] :
        raise Reject, ( "[%s] Transition only allowed from `%s` to one "
                        "out of %s."
                      % (nodeid, cur_status_name, to_stati)
                      )

    # Direct close only allowed if mistaken, obsolete or duplicate,
    # or if it is a container.
    if (cur_status_name in ["open", "feedback", "suspended"] \
    and new_status_name == "closed") :
        if not (  kind_name in ["Mistaken", "Obsolete"]
               or superseder
               or is_container
               ) :
            raise Reject, ( "[%s] To close this issue, kind must be set to "
                            "`Mistaken` or `Obsolete`, <br>or this issue must "
                            "be a duplicate of another issue or a container."
                          % nodeid
                          )
        if kind_name in ["Mistaken", "Obsolete"] and not (msg) :
            raise Reject, ( "[%s] A reason in `message` must be given here."
                          % nodeid
                          )

    # The responsible person must change on certain transitions of `status`.
    to_change = [s for (s, r, m) in sm [cur_status_name] if r]
    if  new_status != cur_status \
    and new_status in [db.status.lookup (s) for s in to_change] \
    and old_responsible == new_responsible \
    and not is_container :
            raise Reject, ( "[%s] The responsible person must be changed for " 
                            "this transition (%s to %s)."
                          % (nodeid, cur_status_name, new_status_name)
                          )

    # A `message` must be given on certain transitions of `status`,
    # but not for a container.
    to_change = [s for (s, r, m) in sm [cur_status_name] if m]
    if  not is_container \
    and new_status != cur_status \
    and new_status in [db.status.lookup (s) for s in to_change] \
    and not msg :
        raise Reject, ( "[%s] A reason in `message` must be given here."
                      % nodeid
                      )

    # A `message` must be given whenever `responsible` changes.
    if old_responsible != new_responsible and not msg :
        raise Reject, ( "[%s] A reason in `message` must be given to "
                        "change the `responsible`."
                      % nodeid
                      )

    # Check if the `fixed_in` field is filled in when moving to `testing`.
    if new_status_name == "testing" and not fixed :
        raise Reject, ( "[%s] The `fixed_in` field must be set for "
                        "a transition to `testing`."
                      % nodeid
                      )

    # Check that fixed_in does not contain illegal pattern when moving
    # to testing or moving to closed.
    if (  (cur_status_name == "testing" and new_status_name == "closed")
       or (cur_status_name == "open"    and new_status_name == "testing")
       ) :
        for p in _fixed_in_patterns :
            if p.search (fixed) :
                raise Reject, ( "[%s] %s is not allowed for the fixed_in field"
                              % (nodeid, fixed)
                              )

    # Ensure the info in which version a bug was fixed keeps alive.
    if  cur_status_name == "testing" \
    and new_status_name == "closed" \
    and not fixed :
        raise Reject, ( "[%s] The `fixed_in` field must be (or remain) set."
                      % nodeid
                      )

    # Check for correct format of the `effort` field.
    if effort and not _effort_regex.match (effort) :
        raise Reject, ( "[%s] The `effort` field must have the format "
                        "`\\d+ [PM][DWM]`, e.g. `12 PD`."
                      % nodeid
                      )
    
    # Ensure `files_affected` to be filled on certifyable products.
    if (  (cur_status_name == "testing" and new_status_name == "closed")
       or (cur_status_name == "open"    and new_status_name == "testing")
       ) \
    and category_name in cert_sw \
    and not affected :
        raise Reject, ( "[%s] The `files_affected` field must be (or remain) "
                        "set for certified software."
                      % nodeid
                      )
    
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
    if 'issue' not in db.classes :
        return
    db.issue.audit ("create", limit_new_entry)
    db.issue.audit ("set",    limit_transitions)
    db.issue.audit ("set",    part_of_changed)
# end def init
