properties = \
    [ ( 'area'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'category'
      , [ ( 'cert_sw'
          , ["user"]
          )
        , ( 'default_part_of'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'nosy'
          , ["user"]
          )
        , ( 'responsible'
          , ["user"]
          )
        , ( 'valid'
          , ["user"]
          )
        ]
      )
    , ( 'file'
      , [ ( 'content'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'type'
          , ["user"]
          )
        ]
      )
    , ( 'issue'
      , [ ( 'area'
          , ["issue_admin", "user"]
          )
        , ( 'category'
          , ["issue_admin", "user"]
          )
        , ( 'closed'
          , ["issue_admin", "user"]
          )
        , ( 'composed_of'
          , ["issue_admin", "user"]
          )
        , ( 'confidential'
          , ["issue_admin", "user"]
          )
        , ( 'cur_est_begin'
          , ["issue_admin", "user"]
          )
        , ( 'cur_est_end'
          , ["issue_admin", "user"]
          )
        , ( 'deadline'
          , ["issue_admin", "user"]
          )
        , ( 'depends'
          , ["issue_admin", "user"]
          )
        , ( 'earliest_start'
          , ["issue_admin", "user"]
          )
        , ( 'effective_prio'
          , ["issue_admin", "user"]
          )
        , ( 'files'
          , ["issue_admin", "user"]
          )
        , ( 'files_affected'
          , ["issue_admin", "user"]
          )
        , ( 'fixed_in'
          , ["issue_admin", "user"]
          )
        , ( 'keywords'
          , ["issue_admin", "user"]
          )
        , ( 'kind'
          , ["issue_admin", "user"]
          )
        , ( 'maturity_index'
          , ["issue_admin", "user"]
          )
        , ( 'messages'
          , ["issue_admin", "user"]
          )
        , ( 'needs'
          , ["issue_admin", "user"]
          )
        , ( 'needs_doc'
          , ["issue_admin", "user"]
          )
        , ( 'nosy'
          , ["issue_admin", "user"]
          )
        , ( 'numeric_effort'
          , ["issue_admin", "user"]
          )
        , ( 'part_of'
          , ["issue_admin", "user"]
          )
        , ( 'planned_begin'
          , ["issue_admin", "user"]
          )
        , ( 'planned_end'
          , ["issue_admin", "user"]
          )
        , ( 'priority'
          , ["issue_admin", "user"]
          )
        , ( 'release'
          , ["issue_admin", "user"]
          )
        , ( 'responsible'
          , ["issue_admin", "user"]
          )
        , ( 'severity'
          , ["issue_admin", "user"]
          )
        , ( 'status'
          , ["issue_admin", "user"]
          )
        , ( 'superseder'
          , ["issue_admin", "user"]
          )
        , ( 'title'
          , ["issue_admin", "user"]
          )
        ]
      )
    , ( 'keyword'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'kind'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'msg'
      , [ ( 'author'
          , ["user"]
          )
        , ( 'content'
          , ["user"]
          )
        , ( 'date'
          , ["user"]
          )
        , ( 'files'
          , ["user"]
          )
        , ( 'header'
          , ["user"]
          )
        , ( 'inreplyto'
          , ["user"]
          )
        , ( 'keywords'
          , ["user"]
          )
        , ( 'messageid'
          , ["user"]
          )
        , ( 'recipients'
          , ["user"]
          )
        , ( 'subject'
          , ["user"]
          )
        , ( 'summary'
          , ["user"]
          )
        , ( 'type'
          , ["user"]
          )
        ]
      )
    , ( 'msg_keyword'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'query'
      , [ ( 'klass'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'private_for'
          , ["user"]
          )
        , ( 'tmplate'
          , ["user"]
          )
        , ( 'url'
          , ["user"]
          )
        ]
      )
    , ( 'severity'
      , [ ( 'abbreviation'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        ]
      )
    , ( 'status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'transitions'
          , ["user"]
          )
        ]
      )
    , ( 'status_transition'
      , [ ( 'name'
          , ["user"]
          )
        , ( 'require_msg'
          , ["user"]
          )
        , ( 'require_resp_change'
          , ["user"]
          )
        , ( 'target'
          , ["user"]
          )
        ]
      )
    , ( 'user'
      , [ ( 'address'
          , []
          )
        , ( 'alternate_addresses'
          , []
          )
        , ( 'password'
          , []
          )
        , ( 'phone'
          , []
          )
        , ( 'queries'
          , []
          )
        , ( 'realname'
          , ["user"]
          )
        , ( 'roles'
          , []
          )
        , ( 'status'
          , []
          )
        , ( 'timezone'
          , []
          )
        , ( 'username'
          , ["user"]
          )
        ]
      )
    , ( 'user_status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
