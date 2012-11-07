properties = \
    [ ( 'address'
      , [ 'adr_type'
        , 'affix'
        , 'birthdate'
        , 'city'
        , 'contacts'
        , 'country'
        , 'files'
        , 'firstname'
        , 'function'
        , 'initial'
        , 'lastname'
        , 'lettertitle'
        , 'lookalike_city'
        , 'lookalike_firstname'
        , 'lookalike_function'
        , 'lookalike_lastname'
        , 'lookalike_street'
        , 'messages'
        , 'opening_hours'
        , 'postalcode'
        , 'salutation'
        , 'street'
        , 'title'
        , 'valid'
        ]
      )
    , ( 'adr_type'
      , [ 'code'
        , 'description'
        , 'typecat'
        ]
      )
    , ( 'adr_type_cat'
      , [ 'code'
        , 'description'
        , 'type_valid'
        ]
      )
    , ( 'contact'
      , [ 'address'
        , 'contact'
        , 'contact_type'
        , 'description'
        ]
      )
    , ( 'contact_type'
      , [ 'description'
        , 'name'
        , 'order'
        , 'url_template'
        ]
      )
    , ( 'file'
      , [ 'content'
        , 'name'
        , 'type'
        ]
      )
    , ( 'it_category'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'it_issue'
      , [ 'category'
        , 'confidential'
        , 'deadline'
        , 'files'
        , 'it_prio'
        , 'it_project'
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
      , [ 'name'
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
    , ( 'opening_hours'
      , [ 'from_hour'
        , 'from_minute'
        , 'to_hour'
        , 'to_minute'
        , 'weekday'
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
    , ( 'valid'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'weekday'
      , [ 'name'
        , 'order'
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
