properties = \
    [ ( 'department'
      , [ 'deputy'
        , 'description'
        , 'manager'
        , 'name'
        , 'part_of'
        ]
      )
    , ( 'domain_permission'
      , [ 'ad_domain'
        , 'clearance_by'
        , 'default_roles'
        , 'roles_enabled'
        , 'status'
        , 'timetracking_by'
        , 'users'
        ]
      )
    , ( 'file'
      , [ 'content'
        , 'name'
        , 'type'
        ]
      )
    , ( 'infosec_level'
      , [ 'is_consulting'
        , 'name'
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
      , [ 'city'
        , 'country'
        , 'name'
        , 'sync_id'
        , 'valid_from'
        , 'valid_to'
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
        , 'valid_from'
        , 'valid_to'
        ]
      )
    , ( 'organisation'
      , [ 'company_code'
        , 'description'
        , 'may_purchase'
        , 'name'
        , 'sync_id'
        , 'valid_from'
        , 'valid_to'
        ]
      )
    , ( 'part_of_budget'
      , [ 'description'
        , 'name'
        , 'order'
        ]
      )
    , ( 'payment_type'
      , [ 'name'
        , 'need_approval'
        , 'order'
        ]
      )
    , ( 'pg_category'
      , [ 'name'
        , 'sap_ref'
        ]
      )
    , ( 'pr_approval'
      , [ 'by'
        , 'date'
        , 'deputy'
        , 'deputy_gets_mail'
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
        , 'payment_type_amount'
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
        , 'want_no_messages'
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
        , 'infosec_level'
        , 'internal_order'
        , 'is_asset'
        , 'offer_number'
        , 'payment_type'
        , 'pr_currency'
        , 'pr_supplier'
        , 'price_per_unit'
        , 'product_group'
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
    , ( 'pr_supplier_risk'
      , [ 'organisation'
        , 'security_req_group'
        , 'supplier'
        , 'supplier_risk_category'
        ]
      )
    , ( 'product_group'
      , [ 'infosec_level'
        , 'name'
        , 'pg_category'
        , 'sap_ref'
        , 'security_req_group'
        ]
      )
    , ( 'purchase_request'
      , [ 'approvals'
        , 'continuous_obligation'
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
        , 'intended_duration'
        , 'internal_order'
        , 'issue_ids'
        , 'messages'
        , 'nosy'
        , 'offer_items'
        , 'organisation'
        , 'part_of_budget'
        , 'payment_type'
        , 'pr_currency'
        , 'pr_ext_resource'
        , 'pr_justification'
        , 'pr_risks'
        , 'purchase_risk_type'
        , 'purchase_type'
        , 'purchasing_agents'
        , 'renegotiations'
        , 'renew_until'
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
    , ( 'purchase_risk_type'
      , [ 'name'
        , 'order'
        ]
      )
    , ( 'purchase_security_risk'
      , [ 'infosec_level'
        , 'purchase_risk_type'
        , 'supplier_risk_category'
        ]
      )
    , ( 'purchase_type'
      , [ 'confidential'
        , 'description'
        , 'forced_roles'
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
        , 'deputy_gets_mail'
        , 'description'
        , 'name'
        , 'organisation'
        , 'purchasing_agents'
        , 'responsible'
        , 'sync_id'
        , 'valid'
        ]
      )
    , ( 'security_req_group'
      , [ 'is_consulting'
        , 'name'
        ]
      )
    , ( 'supplier_risk_category'
      , [ 'name'
        , 'order'
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
        , 'deputy_gets_mail'
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
      , [ 'ad_domain'
        , 'address'
        , 'alternate_addresses'
        , 'business_responsible'
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
        , 'is_internal'
        , 'is_nosy'
        , 'is_system'
        , 'ldap_group'
        , 'ldap_prio'
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
