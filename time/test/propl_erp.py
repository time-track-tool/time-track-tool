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
    , ( 'bank_account'
      , [ 'act_number'
        , 'bank'
        , 'bank_code'
        , 'bic'
        , 'description'
        , 'iban'
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
    , ( 'cust_supp'
      , [ 'attendant'
        , 'bank_account'
        , 'contact_person'
        , 'credit_limit'
        , 'currency'
        , 'customer_group'
        , 'customer_status'
        , 'description'
        , 'discount_group'
        , 'dispatch_type'
        , 'files'
        , 'invoice_address'
        , 'invoice_dispatch'
        , 'invoice_text'
        , 'messages'
        , 'name'
        , 'nosy'
        , 'order_text'
        , 'pharma_ref'
        , 'sales_conditions'
        , 'shipping_address'
        , 'supplier_group'
        , 'supplier_status'
        , 'supply_address'
        , 'tax_id'
        ]
      )
    , ( 'customer_group'
      , [ 'description'
        , 'discount_group'
        , 'name'
        ]
      )
    , ( 'customer_status'
      , [ 'description'
        , 'display'
        , 'name'
        , 'order'
        , 'valid'
        ]
      )
    , ( 'discount_group'
      , [ 'currency'
        , 'description'
        , 'group_discount'
        , 'name'
        , 'overall_discount'
        ]
      )
    , ( 'dispatch_type'
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
    , ( 'group_discount'
      , [ 'discount'
        , 'product_group'
        ]
      )
    , ( 'invoice'
        ]
      )
    , ( 'invoice_dispatch'
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
        , 'messages'
        , 'subject'
        ]
      )
    , ( 'measuring_unit'
      , [ 'description'
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
    , ( 'opening_hours'
      , [ 'from_hour'
        , 'from_minute'
        , 'to_hour'
        , 'to_minute'
        , 'weekday'
        ]
      )
    , ( 'overall_discount'
      , [ 'discount'
        , 'price'
        ]
      )
    , ( 'packaging_unit'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'payment'
      , [ 'amount'
        , 'date_payed'
        , 'invoice'
        , 'receipt_no'
        ]
      )
    , ( 'pharma_ref'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'proceeds_group'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'product'
      , [ 'description'
        , 'files'
        , 'measuring_unit'
        , 'messages'
        , 'minimum_inventory'
        , 'name'
        , 'packaging_unit'
        , 'proceeds_group'
        , 'product_group'
        , 'product_price'
        , 'shelf_life_code'
        , 'status'
        , 'use_lot'
        ]
      )
    , ( 'product_group'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'product_price'
      , [ 'currency'
        , 'price'
        , 'vat_percent'
        ]
      )
    , ( 'product_status'
      , [ 'description'
        , 'name'
        , 'order'
        , 'valid'
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
    , ( 'sales_conditions'
      , [ 'description'
        , 'discount_days'
        , 'discount_percent'
        , 'name'
        , 'payment_days'
        ]
      )
    , ( 'shelf_life_code'
      , [ 'description'
        , 'name'
        , 'shelf_life'
        ]
      )
    , ( 'stock'
      , [ 'description'
        , 'name'
        , 'storage'
        ]
      )
    , ( 'stocked_product'
      , [ 'lot'
        , 'on_stock'
        , 'product'
        , 'storage_location'
        ]
      )
    , ( 'storage'
      , [ 'description'
        , 'name'
        , 'storage_locations'
        ]
      )
    , ( 'storage_location'
        ]
      )
    , ( 'supplier_group'
      , [ 'description'
        , 'name'
        ]
      )
    , ( 'supplier_status'
      , [ 'description'
        , 'display'
        , 'name'
        , 'order'
        , 'valid'
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
