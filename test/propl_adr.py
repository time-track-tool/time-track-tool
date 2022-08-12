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
        , 'letters'
        , 'lettertitle'
        , 'lookalike_city'
        , 'lookalike_firstname'
        , 'lookalike_function'
        , 'lookalike_lastname'
        , 'lookalike_street'
        , 'messages'
        , 'opening_hours'
        , 'parent'
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
        , 'order'
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
    , ( 'letter'
      , [ 'address'
        , 'date'
        , 'files'
        , 'messages'
        , 'subject'
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
    , ( 'tmplate'
      , [ 'files'
        , 'name'
        , 'tmplate_status'
        ]
      )
    , ( 'tmplate_status'
      , [ 'description'
        , 'name'
        , 'order'
        , 'use_for_invoice'
        , 'use_for_letter'
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
        , 'is_internal'
        , 'is_nosy'
        , 'is_system'
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
        print (cl)
        for p in props :
            print ('    ', p)
