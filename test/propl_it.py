properties = \
    [ ( 'file'
      , [ 'content'
        , 'name'
        , 'type'
        ]
      )
    , ( 'it_category'
      , [ 'description'
        , 'name'
        , 'valid'
        ]
      )
    , ( 'it_int_prio'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'it_issue'
      , [ 'category'
        , 'confidential'
        , 'deadline'
        , 'files'
        , 'int_prio'
        , 'it_prio'
        , 'it_project'
        , 'it_request_type'
        , 'messages'
        , 'nosy'
        , 'responsible'
        , 'stakeholder'
        , 'status'
        , 'superseder'
        , 'title'
        ]
      )
    , ( 'it_issue_status'
      , [ 'description'
        , 'name'
        , 'order'
        , 'relaxed'
        , 'transitions'
        ]
      )
    , ( 'it_prio'
      , [ 'default'
        , 'must_change'
        , 'name'
        , 'order'
        ]
      )
    , ( 'it_project'
      , [ 'category'
        , 'confidential'
        , 'deadline'
        , 'files'
        , 'it_prio'
        , 'messages'
        , 'nosy'
        , 'responsible'
        , 'stakeholder'
        , 'status'
        , 'title'
        ]
      )
    , ( 'it_project_status'
      , [ 'description'
        , 'name'
        , 'order'
        , 'transitions'
        ]
      )
    , ( 'it_request_type'
      , [ 'close_immediately'
        , 'log_template'
        , 'name'
        , 'order'
        , 'title_regex'
        ]
      )
    , ( 'msg'
      , [ 'author'
        , 'content'
        , 'date'
        , 'files'
        , 'inreplyto'
        , 'messageid'
        , 'recipients'
        , 'summary'
        , 'type'
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
    , ( 'user'
      , [ 'address'
        , 'alternate_addresses'
        , 'csv_delimiter'
        , 'hide_message_files'
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
