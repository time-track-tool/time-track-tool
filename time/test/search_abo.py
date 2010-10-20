properties = \
    [ ( 'abo'
      , [ ( 'aboprice'
          , ["abo", "invoice", "product"]
          )
        , ( 'amount'
          , ["abo", "invoice", "product"]
          )
        , ( 'begin'
          , ["abo", "invoice", "product"]
          )
        , ( 'end'
          , ["abo", "invoice", "product"]
          )
        , ( 'invoices'
          , ["abo", "invoice", "product"]
          )
        , ( 'messages'
          , ["abo", "invoice", "product"]
          )
        , ( 'payer'
          , ["abo", "invoice", "product"]
          )
        , ( 'subscriber'
          , ["abo", "invoice", "product"]
          )
        ]
      )
    , ( 'abo_price'
      , [ ( 'abotype'
          , ["user"]
          )
        , ( 'amount'
          , ["user"]
          )
        , ( 'currency'
          , ["user"]
          )
        , ( 'invoice_group'
          , ["user"]
          )
        , ( 'invoice_template'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'valid'
          , ["user"]
          )
        ]
      )
    , ( 'abo_type'
      , [ ( 'adr_type'
          , ["abo", "invoice", "product"]
          )
        , ( 'description'
          , ["abo", "invoice", "product"]
          )
        , ( 'name'
          , ["abo", "invoice", "product"]
          )
        , ( 'order'
          , ["abo", "invoice", "product"]
          )
        , ( 'period'
          , ["abo", "invoice", "product"]
          )
        ]
      )
    , ( 'address'
      , [ ( 'abos'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'adr_type'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'affix'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'birthdate'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'city'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'contacts'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'country'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'files'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'firstname'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'function'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'initial'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'invoices'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'lastname'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'letters'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'lettertitle'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'lookalike_city'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'lookalike_firstname'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'lookalike_function'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'lookalike_lastname'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'lookalike_street'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'messages'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'opening_hours'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'parent'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'payed_abos'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'postalcode'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'salutation'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'street'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'title'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'valid'
          , ["adr_readonly", "contact", "user"]
          )
        ]
      )
    , ( 'adr_type'
      , [ ( 'code'
          , ["adr_readonly", "user"]
          )
        , ( 'description'
          , ["adr_readonly", "user"]
          )
        , ( 'typecat'
          , ["adr_readonly", "user"]
          )
        ]
      )
    , ( 'adr_type_cat'
      , [ ( 'code'
          , ["adr_readonly", "user"]
          )
        , ( 'description'
          , ["adr_readonly", "user"]
          )
        , ( 'type_valid'
          , ["adr_readonly", "user"]
          )
        ]
      )
    , ( 'contact'
      , [ ( 'address'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'contact'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'contact_type'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'description'
          , ["adr_readonly", "contact", "user"]
          )
        ]
      )
    , ( 'contact_type'
      , [ ( 'description'
          , ["adr_readonly", "user"]
          )
        , ( 'name'
          , ["adr_readonly", "user"]
          )
        , ( 'order'
          , ["adr_readonly", "user"]
          )
        , ( 'url_template'
          , ["adr_readonly", "user"]
          )
        ]
      )
    , ( 'currency'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'file'
      , [ ( 'content'
          , ["adr_readonly", "user"]
          )
        , ( 'name'
          , ["adr_readonly", "user"]
          )
        , ( 'type'
          , ["adr_readonly", "user"]
          )
        ]
      )
    , ( 'invoice'
      , [ ( 'abo'
          , ["invoice"]
          )
        , ( 'amount'
          , ["invoice"]
          )
        , ( 'amount_payed'
          , ["invoice"]
          )
        , ( 'balance_open'
          , ["invoice"]
          )
        , ( 'currency'
          , ["invoice"]
          )
        , ( 'invoice_group'
          , ["invoice"]
          )
        , ( 'invoice_no'
          , ["invoice"]
          )
        , ( 'last_sent'
          , ["invoice"]
          )
        , ( 'letters'
          , ["invoice"]
          )
        , ( 'n_sent'
          , ["invoice"]
          )
        , ( 'open'
          , ["invoice"]
          )
        , ( 'payer'
          , ["invoice"]
          )
        , ( 'payment'
          , ["invoice"]
          )
        , ( 'period_end'
          , ["invoice"]
          )
        , ( 'period_start'
          , ["invoice"]
          )
        , ( 'send_it'
          , ["invoice"]
          )
        , ( 'subscriber'
          , ["invoice"]
          )
        ]
      )
    , ( 'invoice_group'
      , [ ( 'description'
          , ["invoice"]
          )
        , ( 'name'
          , ["invoice"]
          )
        ]
      )
    , ( 'invoice_template'
      , [ ( 'interval'
          , ["invoice"]
          )
        , ( 'invoice_level'
          , ["invoice"]
          )
        , ( 'name'
          , ["invoice"]
          )
        , ( 'tmplate'
          , ["invoice"]
          )
        ]
      )
    , ( 'letter'
      , [ ( 'address'
          , ["user"]
          )
        , ( 'date'
          , ["user"]
          )
        , ( 'files'
          , ["user"]
          )
        , ( 'invoice'
          , ["user"]
          )
        , ( 'messages'
          , ["user"]
          )
        , ( 'subject'
          , ["user"]
          )
        ]
      )
    , ( 'msg'
      , [ ( 'author'
          , ["adr_readonly", "user"]
          )
        , ( 'content'
          , ["adr_readonly", "user"]
          )
        , ( 'date'
          , ["adr_readonly", "user"]
          )
        , ( 'files'
          , ["adr_readonly", "user"]
          )
        , ( 'inreplyto'
          , ["adr_readonly", "user"]
          )
        , ( 'messageid'
          , ["adr_readonly", "user"]
          )
        , ( 'recipients'
          , ["adr_readonly", "user"]
          )
        , ( 'summary'
          , ["adr_readonly", "user"]
          )
        , ( 'type'
          , ["adr_readonly", "user"]
          )
        ]
      )
    , ( 'opening_hours'
      , [ ( 'from_hour'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'from_minute'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'to_hour'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'to_minute'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'weekday'
          , ["adr_readonly", "contact", "user"]
          )
        ]
      )
    , ( 'payment'
      , [ ( 'amount'
          , ["invoice"]
          )
        , ( 'date_payed'
          , ["invoice"]
          )
        , ( 'invoice'
          , ["invoice"]
          )
        , ( 'receipt_no'
          , ["invoice"]
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
    , ( 'tmplate'
      , [ ( 'files'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'tmplate_status'
          , ["user"]
          )
        ]
      )
    , ( 'tmplate_status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'use_for_invoice'
          , ["user"]
          )
        , ( 'use_for_letter'
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
          , ["adr_readonly", "user"]
          )
        , ( 'queries'
          , ["user"]
          )
        , ( 'realname'
          , ["adr_readonly", "user"]
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
          , ["adr_readonly", "user"]
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
    , ( 'valid'
      , [ ( 'description'
          , ["adr_readonly", "user"]
          )
        , ( 'name'
          , ["adr_readonly", "user"]
          )
        ]
      )
    , ( 'weekday'
      , [ ( 'name'
          , ["adr_readonly", "contact", "user"]
          )
        , ( 'order'
          , ["adr_readonly", "contact", "user"]
          )
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
