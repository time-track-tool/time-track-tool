#!/usr/bin/python

from user_dynamic import find_user_dynamic, next_user_dynamic
from user_dynamic import first_user_dynamic
from roundup.date import Date
from freeze       import freeze_date
from common       import pretty_range, ymd

def is_correct_dyn (dyn, auto_wp) :
    """ Check that the given dynamic user record matches this
        org_location and has do_auto_wp turned on.
    """
    if dyn.org_location != auto_wp.org_location :
        return False
    if dyn.contract_type != auto_wp.contract_type :
        return False
    if not auto_wp.all_in and dyn.all_in :
        return False
    return dyn.do_auto_wp
# end def is_correct_dyn

def auto_wp_duration_end (db, auto_wp, uid) :
    """ If this auto_wp has a duration, need to find when we started.
        We start from the first dyn. user record: Note that we use the
        very first record even if it's a different org_location or
        doesn't have do_auto_wp set.
    """
    duration_end = None
    if auto_wp.duration :
        dyn = first_user_dynamic (db, uid)
        if dyn :
            duration_end = dyn.valid_from + auto_wp.duration
    return duration_end
# end def auto_wp_duration_end

def check_auto_wp (db, auto_wp_id, userid) :
    """ Get latest non-frozen dynamic user record for this user and then
        look through auto WPs and check if they conform: There should be
        a WP for each contiguous time a dynamic user record with
        do_auto_wp set is available for this user.
    """
    user   = db.user.getnode (userid)
    snam   = str (user.username).split ('@') [0]
    desc   = "Automatic wp for user %s" % snam
    # Very early default should we not find any freeze records
    start  = Date ('1970-01-01')
    freeze = freeze_date (db, userid)
    if freeze :
        start = freeze
    auto_wp = db.auto_wp.getnode (auto_wp_id)
    duration_end = auto_wp_duration_end (db, auto_wp, userid)
    # Nothing todo if this ended all before freeze
    if duration_end and duration_end < start :
        return
    tp  = db.time_project.getnode (auto_wp.time_project)
    # Get dynamic user record on or after start
    dyn = find_user_dynamic (db, userid, start, ct = auto_wp.contract_type)
    # If auto_wp isn't valid, we set dyn to None this will invalidate
    # all WPs found:
    if not auto_wp.is_valid :
        dyn = None
    # Find first dyn with do_auto_wp and org_location properly set
    while dyn and not is_correct_dyn (dyn, auto_wp) :
        dyn = next_user_dynamic (db, dyn, use_ct = True)
    # Find all wps auto-created from this auto_wp after start.
    # Note that all auto wps have a start time. Only the very first wp
    # may start *before* start (if the time_end of the time_wp is either
    # empty or after start)
    d = dict \
        ( auto_wp    = auto_wp_id
        , time_start = pretty_range (start)
        , bookers    = userid
        )
    wps = db.time_wp.filter (None, d, sort = ('+', 'time_start'))
    wps = [db.time_wp.getnode (w) for w in wps]
    d ['time_start'] = pretty_range (None, start)
    wp1 = db.time_wp.filter (None, d, sort = ('-', 'time_start'), limit = 1)
    assert len (wp1) <= 1
    if wp1 :
        wp = db.time_wp.getnode (wp1 [0])
        is_same = wps and wps [0].id == wp.id
        if not is_same and not wp.end_time or wp.end_time > start :
            wps.insert (0, wp)
    # Now we have the first relevant dyn user record and a list of WPs
    # The list of WPs might be empty
    try :
        wp = wps.pop (0)
    except IndexError :
        wp = None

    while dyn :
        # Remember the start time of the first dyn
        dyn_start = dyn.valid_from
        # we compute the range of contiguous dyns with same do_auto_wp setting
        while dyn and dyn.valid_to :
            n = next_user_dynamic (db, dyn, use_ct = True)
            if  (   n
                and is_correct_dyn (n, auto_wp)
                and n.valid_from == dyn.valid_to
                ) :
                dyn = n
            else :
                break
        end_time = dyn.valid_to
        if duration_end and (not end_time or end_time > duration_end) :
            end_time = duration_end
        if end_time and end_time <= dyn_start :
            dyn = None
            break
        # Limit the first wp(s) if the start time of the dyn user record is
        # after the start time of the frozen range and the wp starts
        # before that.
        while wp and wp.time_start < start and dyn_start > start :
            if wp.time_end > start :
                n = '%s -%s' % (snam, start.pretty (ymd))
                d = dict (time_end = start, name = n)
                if wp.description != desc :
                    d ['description'] = desc
                db.time_wp.set (wp.id, **d)
            try :
                wp = wps.pop (0)
            except IndexError :
                wp = None
        assert not wp or wp.time_start > start

        # Check if there are wps that start before the validity of the
        # current dynamic user record
        while wp and wp.time_start < dyn_start :
            if wp.time_end and wp.time_end <= dyn_start :
                # Check that really nothing is booked on this WP
                d = dict (wp = wp.id)
                d ['daily_record.user'] = userid
                d ['daily_record.date'] = pretty_range \
                    (wp.time_start, wp.time_end)
                trs = db.time_record.filter (None, d)
                # If something is booked we set end = start
                # Otherwise we retire the wp
                if not trs :
                    db.time_wp.retire (wp.id)
                else :
                    n = '%s -%s' % (snam, wp.time_start.pretty (ymd))
                    d = dict (time_end = wp.time_start, name = n)
                    if wp.description != desc :
                        d ['description'] = desc
                    db.time_wp.set (wp.id, **d)
                try :
                    wp = wps.pop (0)
                except IndexError :
                    wp = None
            else :
                d = dict (time_start = dyn_start)
                if wp.description != desc :
                    d ['description'] = desc
                db.time_wp.set (wp.id, **d)
                break

        # We now either have a wp with correct start date or none
        if wp :
            # We may have not a single wp but a set of 'fragments'
            # before the end-date of the dyn user record (or an open
            # end)
            while (   wps
                  and (  end_time and wp.time_end < end_time
                      or not end_time and wp.time_end
                      )
                  ) :
                if wps [0].time_start > end_time :
                    break
                assert not wps [0].time_end or wp.time_end <= wps [0].time_end
                if wp.time_end != wps [0].time_start :
                    n = '%s -%s' % (snam, wps [0].time_start.pretty (ymd))
                    d = dict (time_end = wps [0].time_start, name = n)
                    if wp.description != desc :
                        d ['description'] = desc
                    db.time_wp.set (wp.id, ** d)
                wp = wps.pop (0)
            if end_time :
                if wp.time_end != end_time :
                    n = '%s -%s' % (snam, end_time.pretty (ymd))
                    d = dict (time_end = end_time, name = n)
                    if wp.description != desc :
                        d ['description'] = desc
                    db.time_wp.set (wp.id, **d)
            else :
                if wp.time_end :
                    d = dict (time_end = None, name = snam)
                    if wp.description != desc :
                        d ['description'] = desc
                    db.time_wp.set (wp.id, **d)
            try :
                wp = wps.pop (0)
            except IndexError :
                wp = None
        else :
            # If we have no wp, create one
            d = dict \
                ( auto_wp           = auto_wp_id
                , project           = auto_wp.time_project
                , durations_allowed = auto_wp.durations_allowed
                , bookers           = [userid]
                , description       = desc
                , name              = snam
                , time_start        = max (start, dyn_start)
                , is_public         = False
                , planned_effort    = 0
                , responsible       = tp.responsible
                )
            if end_time :
                d ['time_end'] = end_time
                d ['name']     = '%s -%s' % (snam, end_time.pretty (ymd))
            wpid = db.time_wp.create (**d)
        od  = dyn
        dyn = next_user_dynamic (db, dyn, use_ct = True)
        while dyn and not is_correct_dyn (dyn, auto_wp) :
            dyn = next_user_dynamic (db, dyn, use_ct = True)
        if not dyn :
            if not end_time :
                assert not wp and not wps
    if wp :
        wps.insert (0, wp)
        wp = None
        # Retire WPs that are left over but before that check that
        # nothing is booked.
        for wp in wps :
            d = dict (wp = wp.id)
            d ['daily_record.user'] = userid
            trs = db.time_record.filter (None, d)
            if not trs :
                db.time_wp.retire (wp.id)
            else :
                n = '%s -%s' % (snam, wp.time_start.pretty (ymd))
                d = dict (time_end = wp.time_start, name = n)
                if wp.description != desc :
                    d ['description'] = desc
                db.time_wp.set (wp.id, **d)
        wps = []
        wp  = None
# end def check_auto_wp
