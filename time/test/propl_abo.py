properties = \
    [ ( 'abo'
      , [ 'aboprice'
        , 'amount'
        , 'begin'
        , 'end'
        , 'invoices'
        , 'messages'
        , 'payer'
        , 'subscriber'
        ]
      )
    , ( 'abo_price'
      , [ 'abotype'
        , 'amount'
        , 'currency'
        , 'invoice_group'
        , 'invoice_template'
        , 'name'
        , 'valid'
        ]
      )
    , ( 'abo_type'
      , [ 'adr_type'
        , 'description'
        , 'name'
        , 'order'
        , 'period'
        ]
      )
    , ( 'address'
      , [ 'abos'
        , 'adr_type'
        , 'affix'
        , 'birthdate'
        , 'city'
        , 'contacts'
        , 'country'
        , 'files'
        , 'firstname'
        , 'function'
        , 'initial'
        , 'invoices'
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
        , 'payed_abos'
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
    , ( 'currency'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'file'
      , [ 'content'
        , 'name'
        , 'type'
        ]
      )
    , ( 'invoice'
      , [ 'abo'
        , 'amount'
        , 'amount_payed'
        , 'balance_open'
        , 'currency'
        , 'invoice_group'
        , 'invoice_no'
        , 'last_sent'
        , 'letters'
        , 'n_sent'
        , 'open'
        , 'payer'
        , 'payment'
        , 'period_end'
        , 'period_start'
        , 'send_it'
        , 'subscriber'
        ]
      )
    , ( 'invoice_group'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'invoice_template'
      , [ 'interval'
        , 'invoice_level'
        , 'name'
        , 'tmplate'
        ]
      )
    , ( 'letter'
      , [ 'address'
        , 'date'
        , 'files'
        , 'invoice'
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
    , ( 'payment'
      , [ 'amount'
        , 'date_payed'
        , 'invoice'
        , 'receipt_no'
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
        , 'password'
        , 'phone'
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
