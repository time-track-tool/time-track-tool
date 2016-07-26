properties = \
    [ ( 'area'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'category'
      , [ 'cert_sw'
        , 'default_part_of'
        , 'description'
        , 'name'
        , 'nosy'
        , 'prodcat'
        , 'responsible'
        , 'valid'
        ]
      )
    , ( 'file'
      , [ 'content'
        , 'name'
        , 'type'
        ]
      )
    , ( 'issue'
      , [ 'area'
        , 'category'
        , 'closed'
        , 'composed_of'
        , 'confidential'
        , 'cur_est_begin'
        , 'cur_est_end'
        , 'deadline'
        , 'depends'
        , 'earliest_start'
        , 'effective_prio'
        , 'effort_hours'
        , 'files'
        , 'files_affected'
        , 'fixed_in'
        , 'keywords'
        , 'kind'
        , 'maturity_index'
        , 'messages'
        , 'needs'
        , 'nosy'
        , 'numeric_effort'
        , 'part_of'
        , 'planned_begin'
        , 'planned_end'
        , 'priority'
        , 'release'
        , 'responsible'
        , 'safety_level'
        , 'severity'
        , 'status'
        , 'superseder'
        , 'test_level'
        , 'title'
        ]
      )
    , ( 'keyword'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'kind'
      , [ 'description'
        , 'name'
        , 'simple'
        ]
      )
    , ( 'msg'
      , [ 'author'
        , 'content'
        , 'date'
        , 'files'
        , 'header'
        , 'inreplyto'
        , 'keywords'
        , 'messageid'
        , 'recipients'
        , 'subject'
        , 'summary'
        , 'type'
        ]
      )
    , ( 'msg_keyword'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'prodcat'
      , [ 'level'
        , 'name'
        , 'valid'
        ]
      )
    , ( 'query'
      , [ 'klass'
        , 'name'
        , 'private_for'
        , 'tmplate'
        , 'url'
        ]
      )
    , ( 'safety_level'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'severity'
      , [ 'abbreviation'
        , 'name'
        , 'order'
        ]
      )
    , ( 'status'
      , [ 'description'
        , 'name'
        , 'order'
        , 'simple_transitions'
        , 'transitions'
        ]
      )
    , ( 'status_transition'
      , [ 'name'
        , 'require_msg'
        , 'require_resp_change'
        , 'target'
        ]
      )
    , ( 'test_level'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'user'
      , [ 'address'
        , 'alternate_addresses'
        , 'password'
        , 'queries'
        , 'realname'
        , 'roles'
        , 'status'
        , 'timezone'
        , 'username'
        ]
      )
    , ( 'user_status'
      , [ 'description'
        , 'is_nosy'
        , 'name'
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
