properties = \
    [ ( 'department'
      , [ 'deputy'
        , 'description'
        , 'manager'
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
        , 'may_purchase'
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
        , 'deputy'
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
    , ( 'pr_currency'
      , [ 'max_sum'
        , 'min_sum'
        , 'name'
        , 'order'
        ]
      )
    , ( 'pr_offer_item'
      , [ 'add_to_las'
        , 'description'
        , 'index'
        , 'is_asset'
        , 'offer_number'
        , 'pr_currency'
        , 'pr_supplier'
        , 'price_per_unit'
        , 'purchase_type'
        , 'sap_cc'
        , 'supplier'
        , 'time_project'
        , 'units'
        , 'vat'
        ]
      )
    , ( 'pr_rating_category'
      , [ 'name'
        , 'order'
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
        , 'sap_ref'
        ]
      )
    , ( 'pr_supplier_rating'
      , [ 'organisation'
        , 'rating'
        , 'scope'
        , 'supplier'
        ]
      )
    , ( 'purchase_request'
      , [ 'continuous_obligation'
        , 'contract_term'
        , 'delivery_deadline'
        , 'department'
        , 'files'
        , 'frame_purchase'
        , 'frame_purchase_end'
        , 'intended_duration'
        , 'messages'
        , 'nosy'
        , 'offer_items'
        , 'organisation'
        , 'part_of_budget'
        , 'pr_currency'
        , 'purchase_type'
        , 'renegotiations'
        , 'requester'
        , 'responsible'
        , 'safety_critical'
        , 'sap_cc'
        , 'sap_reference'
        , 'status'
        , 'termination_date'
        , 'terms_conditions'
        , 'time_project'
        , 'title'
        , 'total_cost'
        ]
      )
    , ( 'purchase_type'
      , [ 'confidential'
        , 'description'
        , 'name'
        , 'order'
        , 'roles'
        , 'valid'
        , 'view_roles'
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
        , 'purchasing_agents'
        , 'responsible'
        , 'valid'
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
        , 'purchasing_agents'
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
        , 'guid'
        , 'hide_message_files'
        , 'org_location'
        , 'password'
        , 'queries'
        , 'realname'
        , 'roles'
        , 'status'
        , 'supervisor'
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
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
