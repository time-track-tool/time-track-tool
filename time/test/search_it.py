properties = \
    [ ( 'file'
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
    , ( 'it_category'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'it_issue'
      , [ ( 'category'
          , ["it", "itview", "user"]
          )
        , ( 'confidential'
          , ["it", "itview", "user"]
          )
        , ( 'deadline'
          , ["it", "itview", "user"]
          )
        , ( 'files'
          , ["it", "itview", "user"]
          )
        , ( 'it_prio'
          , ["it", "itview", "user"]
          )
        , ( 'it_project'
          , ["it", "itview", "user"]
          )
        , ( 'messages'
          , ["it", "itview", "user"]
          )
        , ( 'nosy'
          , ["it", "itview", "user"]
          )
        , ( 'responsible'
          , ["it", "itview", "user"]
          )
        , ( 'stakeholder'
          , ["it", "itview", "user"]
          )
        , ( 'status'
          , ["it", "itview", "user"]
          )
        , ( 'superseder'
          , ["it", "itview", "user"]
          )
        , ( 'title'
          , ["it", "itview", "user"]
          )
        ]
      )
    , ( 'it_issue_status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'relaxed'
          , ["user"]
          )
        , ( 'transitions'
          , ["user"]
          )
        ]
      )
    , ( 'it_prio'
      , [ ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        ]
      )
    , ( 'it_project'
      , [ ( 'category'
          , ["it", "itview", "user"]
          )
        , ( 'confidential'
          , ["it", "itview", "user"]
          )
        , ( 'deadline'
          , ["it", "itview", "user"]
          )
        , ( 'files'
          , ["it", "itview", "user"]
          )
        , ( 'it_prio'
          , ["it", "itview", "user"]
          )
        , ( 'messages'
          , ["it", "itview", "user"]
          )
        , ( 'nosy'
          , ["it", "itview", "user"]
          )
        , ( 'responsible'
          , ["it", "itview", "user"]
          )
        , ( 'stakeholder'
          , ["it", "itview", "user"]
          )
        , ( 'status'
          , ["it", "itview", "user"]
          )
        , ( 'title'
          , ["it", "itview", "user"]
          )
        ]
      )
    , ( 'it_project_status'
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
        , ( 'inreplyto'
          , ["user"]
          )
        , ( 'messageid'
          , ["user"]
          )
        , ( 'recipients'
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
    , ( 'user'
      , [ ( 'address'
          , ["user"]
          )
        , ( 'alternate_addresses'
          , ["user"]
          )
        , ( 'csv_delimiter'
          , []
          )
        , ( 'password'
          , ["user"]
          )
        , ( 'phone'
          , ["user"]
          )
        , ( 'queries'
          , ["user"]
          )
        , ( 'realname'
          , ["user"]
          )
        , ( 'roles'
          , []
          )
        , ( 'status'
          , ["user"]
          )
        , ( 'timezone'
          , ["user"]
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
