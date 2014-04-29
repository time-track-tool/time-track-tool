properties = \
    [ ( 'abo'
      , [ ( 'aboprice'
          , ["abo", "abo+invoice", "admin", "invoice", "product"]
          )
        , ( 'amount'
          , ["abo", "abo+invoice", "admin", "invoice", "product"]
          )
        , ( 'begin'
          , ["abo", "abo+invoice", "admin", "invoice", "product"]
          )
        , ( 'end'
          , ["abo", "abo+invoice", "admin", "invoice", "product"]
          )
        , ( 'invoices'
          , ["abo+invoice", "admin", "invoice"]
          )
        , ( 'messages'
          , ["abo", "abo+invoice", "admin", "invoice", "product"]
          )
        , ( 'payer'
          , ["abo", "abo+invoice", "admin", "invoice", "product"]
          )
        , ( 'subscriber'
          , ["abo", "abo+invoice", "admin", "invoice", "product"]
          )
        ]
      )
    , ( 'abo_price'
      , [ ( 'abotype'
          , ['abo', 'abo+invoice', 'admin', 'invoice', 'product']
          )
        , ( 'amount'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'currency'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'invoice_group'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'invoice_template'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'valid'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'abo_type'
      , [ ( 'adr_type'
          , ['abo', 'abo+invoice', 'admin', 'invoice', 'product']
          )
        , ( 'description'
          , ['abo', 'abo+invoice', 'admin', 'invoice', 'product']
          )
        , ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'invoice', 'product']
          )
        , ( 'order'
          , ['abo', 'abo+invoice', 'admin', 'invoice', 'product']
          )
        , ( 'period'
          , ['abo', 'abo+invoice', 'admin', 'invoice', 'product']
          )
        ]
      )
    , ( 'address'
      , [ ( 'abos'
          , ['abo', 'abo+invoice', 'admin', 'invoice', 'product']
          )
        , ( 'adr_type'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'affix'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'birthdate'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'city'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'contacts'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'country'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'files'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'firstname'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'function'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'initial'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'invoices'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'lastname'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'letters'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'lettertitle'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'lookalike_city'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'lookalike_firstname'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'lookalike_function'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'lookalike_lastname'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'lookalike_street'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'messages'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'opening_hours'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'parent'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'payed_abos'
          , ['abo', 'abo+invoice', 'admin', 'invoice', 'product']
          )
        , ( 'postalcode'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'salutation'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'street'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'title'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'valid'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'adr_type'
      , [ ( 'code'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'description'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'typecat'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'adr_type_cat'
      , [ ( 'code'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'description'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'type_valid'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'contact'
      , [ ( 'address'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'contact'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'contact_type'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'description'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'contact_type'
      , [ ( 'description'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'order'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'url_template'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'currency'
      , [ ( 'description'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'file'
      , [ ( 'content'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'type'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'invoice'
      , [ ( 'abo'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'amount'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'amount_payed'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'balance_open'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'currency'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'invoice_group'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'invoice_no'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'last_sent'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'letters'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'n_sent'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'open'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'payer'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'payment'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'period_end'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'period_start'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'send_it'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'subscriber'
          , ['abo+invoice', 'admin', 'invoice']
          )
        ]
      )
    , ( 'invoice_group'
      , [ ( 'description'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'name'
          , ['abo+invoice', 'admin', 'invoice']
          )
        ]
      )
    , ( 'invoice_template'
      , [ ( 'interval'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'invoice_level'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'name'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'tmplate'
          , ['abo+invoice', 'admin', 'invoice']
          )
        ]
      )
    , ( 'letter'
      , [ ( 'address'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'date'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'files'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'invoice'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'messages'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'subject'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'msg'
      , [ ( 'author'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'content'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'date'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'files'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'inreplyto'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'messageid'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'recipients'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'summary'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'type'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'opening_hours'
      , [ ( 'from_hour'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'from_minute'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'to_hour'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'to_minute'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'weekday'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'payment'
      , [ ( 'amount'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'date_payed'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'invoice'
          , ['abo+invoice', 'admin', 'invoice']
          )
        , ( 'receipt_no'
          , ['abo+invoice', 'admin', 'invoice']
          )
        ]
      )
    , ( 'query'
      , [ ( 'klass'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'private_for'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'tmplate'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'url'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'tmplate'
      , [ ( 'files'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'tmplate_status'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'tmplate_status'
      , [ ( 'description'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'order'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'use_for_invoice'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'use_for_letter'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'user'
      , [ ( 'address'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'alternate_addresses'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'csv_delimiter'
          , ['admin']
          )
        , ( 'password'
          , ['admin']
          )
        , ( 'queries'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'realname'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'roles'
          , ['admin']
          )
        , ( 'status'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'timezone'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'username'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'user_status'
      , [ ( 'description'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'is_nosy'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'valid'
      , [ ( 'description'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    , ( 'weekday'
      , [ ( 'name'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        , ( 'order'
          , ['abo', 'abo+invoice', 'admin', 'adr_readonly', 'contact', 'invoice', 'letter', 'product', 'type', 'user']
          )
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
