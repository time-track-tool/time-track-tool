properties = \
    [ ( 'address'
      , [ ( 'adr_type'
          , ["adr_readonly", "user"]
          )
        , ( 'city'
          , ["adr_readonly", "user"]
          )
        , ( 'country'
          , ["adr_readonly", "user"]
          )
        , ( 'files'
          , ["adr_readonly", "user"]
          )
        , ( 'lookalike_city'
          , ["adr_readonly", "user"]
          )
        , ( 'lookalike_street'
          , ["adr_readonly", "user"]
          )
        , ( 'messages'
          , ["adr_readonly", "user"]
          )
        , ( 'opening_hours'
          , ["adr_readonly", "user"]
          )
        , ( 'postalcode'
          , ["adr_readonly", "user"]
          )
        , ( 'street'
          , ["adr_readonly", "user"]
          )
        , ( 'valid'
          , ["adr_readonly", "user"]
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
    , ( 'bank_account'
      , [ ( 'act_number'
          , ["user"]
          )
        , ( 'bank'
          , ["user"]
          )
        , ( 'bank_code'
          , ["user"]
          )
        , ( 'bic'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'iban'
          , ["user"]
          )
        ]
      )
    , ( 'contact'
      , [ ( 'contact'
          , ["adr_readonly", "user"]
          )
        , ( 'contact_type'
          , ["adr_readonly", "user"]
          )
        , ( 'description'
          , ["adr_readonly", "user"]
          )
        , ( 'person'
          , ["adr_readonly", "user"]
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
    , ( 'cust_supp'
      , [ ( 'attendant'
          , ["user"]
          )
        , ( 'bank_account'
          , ["user"]
          )
        , ( 'credit_limit'
          , ["user"]
          )
        , ( 'currency'
          , ["user"]
          )
        , ( 'customer_group'
          , ["user"]
          )
        , ( 'customer_status'
          , ["user"]
          )
        , ( 'customer_type'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'discount_group'
          , ["user"]
          )
        , ( 'dispatch_type'
          , ["user"]
          )
        , ( 'files'
          , ["user"]
          )
        , ( 'invoice_dispatch'
          , ["user"]
          )
        , ( 'invoice_text'
          , ["user"]
          )
        , ( 'lookalike_name'
          , ["user"]
          )
        , ( 'messages'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'nosy'
          , ["user"]
          )
        , ( 'order_text'
          , ["user"]
          )
        , ( 'pharma_ref'
          , ["user"]
          )
        , ( 'sales_conditions'
          , ["user"]
          )
        , ( 'supplier_group'
          , ["user"]
          )
        , ( 'supplier_status'
          , ["user"]
          )
        , ( 'tax_id'
          , ["user"]
          )
        ]
      )
    , ( 'customer_group'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'discount_group'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'customer_status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'display'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'valid'
          , ["user"]
          )
        ]
      )
    , ( 'customer_type'
      , [ ( 'code'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        ]
      )
    , ( 'discount_group'
      , [ ( 'currency'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'group_discount'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'overall_discount'
          , ["user"]
          )
        ]
      )
    , ( 'dispatch_type'
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
    , ( 'group_discount'
      , [ ( 'discount'
          , ["user"]
          )
        , ( 'product_group'
          , ["user"]
          )
        ]
      )
    , ( 'invoice'
      , [
        ]
      )
    , ( 'invoice_dispatch'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
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
        , ( 'messages'
          , ["user"]
          )
        , ( 'subject'
          , ["user"]
          )
        ]
      )
    , ( 'measuring_unit'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
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
    , ( 'opening_hours'
      , [ ( 'from_hour'
          , ["user"]
          )
        , ( 'from_minute'
          , ["user"]
          )
        , ( 'to_hour'
          , ["user"]
          )
        , ( 'to_minute'
          , ["user"]
          )
        , ( 'weekday'
          , ["user"]
          )
        ]
      )
    , ( 'overall_discount'
      , [ ( 'discount'
          , ["user"]
          )
        , ( 'price'
          , ["user"]
          )
        ]
      )
    , ( 'packaging_unit'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
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
    , ( 'person'
      , [ ( 'address'
          , ["user"]
          )
        , ( 'affix'
          , ["user"]
          )
        , ( 'birthdate'
          , ["user"]
          )
        , ( 'contacts'
          , ["user"]
          )
        , ( 'cust_supp'
          , ["user"]
          )
        , ( 'description'
          , ["user"]
          )
        , ( 'files'
          , ["user"]
          )
        , ( 'firstname'
          , ["user"]
          )
        , ( 'function'
          , ["user"]
          )
        , ( 'initial'
          , ["user"]
          )
        , ( 'lastname'
          , ["user"]
          )
        , ( 'lettertitle'
          , ["user"]
          )
        , ( 'lookalike_firstname'
          , ["user"]
          )
        , ( 'lookalike_function'
          , ["user"]
          )
        , ( 'lookalike_lastname'
          , ["user"]
          )
        , ( 'messages'
          , ["user"]
          )
        , ( 'person_type'
          , ["user"]
          )
        , ( 'salutation'
          , ["user"]
          )
        , ( 'title'
          , ["user"]
          )
        ]
      )
    , ( 'person_type'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        ]
      )
    , ( 'pharma_ref'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'proceeds_group'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'product'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'files'
          , ["user"]
          )
        , ( 'measuring_unit'
          , ["user"]
          )
        , ( 'messages'
          , ["user"]
          )
        , ( 'minimum_inventory'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'packaging_unit'
          , ["user"]
          )
        , ( 'proceeds_group'
          , ["user"]
          )
        , ( 'product_group'
          , ["user"]
          )
        , ( 'product_price'
          , ["user"]
          )
        , ( 'shelf_life_code'
          , ["user"]
          )
        , ( 'status'
          , ["user"]
          )
        , ( 'use_lot'
          , ["user"]
          )
        ]
      )
    , ( 'product_group'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        ]
      )
    , ( 'product_price'
      , [ ( 'currency'
          , []
          )
        , ( 'price'
          , []
          )
        , ( 'vat_percent'
          , []
          )
        ]
      )
    , ( 'product_status'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'order'
          , ["user"]
          )
        , ( 'valid'
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
    , ( 'sales_conditions'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'discount_days'
          , ["user"]
          )
        , ( 'discount_percent'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'payment_days'
          , ["user"]
          )
        ]
      )
    , ( 'shelf_life_code'
      , [ ( 'description'
          , ["user"]
          )
        , ( 'name'
          , ["user"]
          )
        , ( 'shelf_life'
          , ["user"]
          )
        ]
      )
    , ( 'stock'
      , [ ( 'description'
          , []
          )
        , ( 'name'
          , []
          )
        , ( 'storage'
          , []
          )
        ]
      )
    , ( 'stocked_product'
      , [ ( 'lot'
          , []
          )
        , ( 'on_stock'
          , []
          )
        , ( 'product'
          , []
          )
        , ( 'storage_location'
          , []
          )
        ]
      )
    , ( 'storage'
      , [ ( 'description'
          , []
          )
        , ( 'name'
          , []
          )
        , ( 'storage_locations'
          , []
          )
        ]
      )
    , ( 'storage_location'
      , [
        ]
      )
    , ( 'supplier_group'
      , [ ( 'description'
          , []
          )
        , ( 'name'
          , []
          )
        ]
      )
    , ( 'supplier_status'
      , [ ( 'description'
          , []
          )
        , ( 'display'
          , []
          )
        , ( 'name'
          , []
          )
        , ( 'order'
          , []
          )
        , ( 'valid'
          , []
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
          , ["user"]
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
          , ["user"]
          )
        , ( 'order'
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
