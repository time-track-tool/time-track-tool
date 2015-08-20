properties = \
    [ ( 'department'
      , [ 'description'
        , 'name'
        , 'part_of'
        ]
      )
    , ( 'file'
      , [ 'content'
        , 'name'
        , 'type'
        ]
      )
    , ( 'location'
      , [ 'country'
        , 'name'
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
    , ( 'org_location'
      , [ 'location'
        , 'name'
        , 'organisation'
        ]
      )
    , ( 'organisation'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'part_of_budget'
      , [ 'description'
        , 'name'
        , 'order'
        ]
      )
    , ( 'pr_approval'
      , [ 'by'
        , 'date'
        , 'description'
        , 'msg'
        , 'order'
        , 'purchase_request'
        , 'role'
        , 'status'
        , 'user'
        ]
      )
    , ( 'pr_approval_order'
      , [ 'order'
        , 'role'
        ]
      )
    , ( 'pr_approval_status'
      , [ 'name'
        , 'order'
        , 'transitions'
        ]
      )
    , ( 'pr_offer_item'
      , [ 'add_to_las'
        , 'description'
        , 'index'
        , 'offer_number'
        , 'pr_supplier'
        , 'price_per_unit'
        , 'supplier'
        , 'units'
        , 'vat_country'
        ]
      )
    , ( 'pr_status'
      , [ 'name'
        , 'order'
        , 'relaxed'
        , 'transitions'
        ]
      )
    , ( 'pr_supplier'
      , [ 'name'
        , 'org_location'
        , 'sap_ref'
        , 'vat_country'
        ]
      )
    , ( 'purchase_request'
      , [ 'continuous_obligation'
        , 'contract_term'
        , 'delivery_deadline'
        , 'department'
        , 'files'
        , 'frame_purchase'
        , 'messages'
        , 'nosy'
        , 'offer_items'
        , 'organisation'
        , 'part_of_budget'
        , 'purchase_type'
        , 'renegotiations'
        , 'requester'
        , 'responsible'
        , 'safety_critical'
        , 'sap_cc'
        , 'status'
        , 'termination_date'
        , 'terms_conditions'
        , 'terms_identical'
        , 'time_project'
        , 'title'
        , 'total_cost'
        ]
      )
    , ( 'purchase_type'
      , [ 'name'
        , 'order'
        , 'roles'
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
    , ( 'sap_cc'
      , [ 'deputy'
        , 'description'
        , 'name'
        , 'responsible'
        ]
      )
    , ( 'terms_conditions'
      , [ 'description'
        , 'name'
        , 'order'
        ]
      )
    , ( 'time_project'
      , [ 'department'
        , 'deputy'
        , 'description'
        , 'name'
        , 'organisation'
        , 'responsible'
        , 'status'
        ]
      )
    , ( 'time_project_status'
      , [ 'active'
        , 'description'
        , 'name'
        ]
      )
    , ( 'user'
      , [ 'address'
        , 'alternate_addresses'
        , 'csv_delimiter'
        , 'department'
        , 'org_location'
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
        , 'ldap_group'
        , 'name'
        , 'roles'
        ]
      )
    , ( 'vat_country'
      , [ 'country'
        , 'vat'
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
