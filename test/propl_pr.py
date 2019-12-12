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
    , ( 'infosec_level'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'internal_order'
      , [ 'name'
        , 'order_number'
        , 'valid'
        ]
      )
    , ( 'location'
      , [ 'country'
        , 'name'
        , 'sync_id'
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
        , 'sync_id'
        ]
      )
    , ( 'organisation'
      , [ 'company_code'
        , 'description'
        , 'may_purchase'
        , 'name'
        , 'sync_id'
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
        , 'role_id'
        , 'status'
        , 'user'
        ]
      )
    , ( 'pr_approval_config'
      , [ 'amount'
        , 'if_not_in_las'
        , 'infosec_amount'
        , 'organisations'
        , 'pr_ext_resource'
        , 'purchase_type'
        , 'role'
        , 'valid'
        ]
      )
    , ( 'pr_approval_order'
      , [ 'is_board'
        , 'is_finance'
        , 'order'
        , 'role'
        , 'users'
        ]
      )
    , ( 'pr_approval_status'
      , [ 'name'
        , 'order'
        , 'transitions'
        ]
      )
    , ( 'pr_currency'
      , [ 'exchange_rate'
        , 'key_currency'
        , 'min_sum'
        , 'name'
        , 'order'
        ]
      )
    , ( 'pr_ext_resource'
      , [ 'name'
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
        , 'date_approved'
        , 'date_ordered'
        , 'delivery_deadline'
        , 'department'
        , 'files'
        , 'frame_purchase'
        , 'frame_purchase_end'
        , 'infosec_level'
        , 'infosec_project'
        , 'infosec_pt'
        , 'intended_duration'
        , 'internal_order'
        , 'issue_ids'
        , 'messages'
        , 'nosy'
        , 'offer_items'
        , 'organisation'
        , 'part_of_budget'
        , 'pr_currency'
        , 'pr_ext_resource'
        , 'pr_justification'
        , 'pr_risks'
        , 'purchase_type'
        , 'purchasing_agents'
        , 'renegotiations'
        , 'requester'
        , 'responsible'
        , 'safety_critical'
        , 'sap_cc'
        , 'sap_reference'
        , 'special_approval'
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
        , 'forced_roles'
        , 'infosec_req'
        , 'name'
        , 'nosy'
        , 'order'
        , 'pr_forced_roles'
        , 'pr_roles'
        , 'pr_view_roles'
        , 'purchasing_agents'
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
        , 'organisation'
        , 'purchasing_agents'
        , 'responsible'
        , 'sync_id'
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
        , 'infosec_req'
        , 'name'
        , 'organisation'
        , 'purchasing_agents'
        , 'responsible'
        , 'status'
        , 'sync_id'
        ]
      )
    , ( 'time_project_status'
      , [ 'active'
        , 'description'
        , 'name'
        , 'sync_id'
        ]
      )
    , ( 'user'
      , [ 'address'
        , 'alternate_addresses'
        , 'clearance_by'
        , 'csv_delimiter'
        , 'guid'
        , 'hide_message_files'
        , 'password'
        , 'queries'
        , 'realname'
        , 'roles'
        , 'status'
        , 'subst_until'
        , 'substitute'
        , 'supervisor'
        , 'timezone'
        , 'username'
        , 'want_no_messages'
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
