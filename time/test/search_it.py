properties = \
    [ ( 'file'
      , [ ( 'content'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'type'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'it_category'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'it_issue'
      , [ ( 'category'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'confidential'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'deadline'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'files'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'it_prio'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'it_project'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'messages'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'nosy'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'responsible'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'stakeholder'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'status'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'superseder'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'title'
          , ["admin", "it", "itview", "user"]
          )
        ]
      )
    , ( 'it_issue_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'relaxed'
          , ["admin", "user"]
          )
        , ( 'transitions'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'it_prio'
      , [ ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'it_project'
      , [ ( 'category'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'confidential'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'deadline'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'files'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'it_prio'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'messages'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'nosy'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'responsible'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'stakeholder'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'status'
          , ["admin", "it", "itview", "user"]
          )
        , ( 'title'
          , ["admin", "it", "itview", "user"]
          )
        ]
      )
    , ( 'it_project_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'transitions'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'msg'
      , [ ( 'author'
          , ["admin", "user"]
          )
        , ( 'content'
          , ["admin", "user"]
          )
        , ( 'date'
          , ["admin", "user"]
          )
        , ( 'files'
          , ["admin", "user"]
          )
        , ( 'inreplyto'
          , ["admin", "user"]
          )
        , ( 'messageid'
          , ["admin", "user"]
          )
        , ( 'recipients'
          , ["admin", "user"]
          )
        , ( 'summary'
          , ["admin", "user"]
          )
        , ( 'type'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'query'
      , [ ( 'klass'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'private_for'
          , ["admin", "user"]
          )
        , ( 'tmplate'
          , ["admin", "user"]
          )
        , ( 'url'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'user'
      , [ ( 'address'
          , ["admin", "user"]
          )
        , ( 'alternate_addresses'
          , ["admin", "user"]
          )
        , ( 'csv_delimiter'
          , ["admin"]
          )
        , ( 'password'
          , ["admin", "user"]
          )
        , ( 'phone'
          , ["admin", "user"]
          )
        , ( 'queries'
          , ["admin", "user"]
          )
        , ( 'realname'
          , ["admin", "user"]
          )
        , ( 'roles'
          , ["admin"]
          )
        , ( 'status'
          , ["admin", "user"]
          )
        , ( 'timezone'
          , ["admin", "user"]
          )
        , ( 'username'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'user_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
