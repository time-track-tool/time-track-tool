properties = \
    [ ( 'address'
      , [ ( 'adr_type'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'city'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'country'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'files'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'lookalike_city'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'lookalike_street'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'messages'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'opening_hours'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'postalcode'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'street'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'valid'
          , ["admin", "adr_readonly", "user"]
          )
        ]
      )
    , ( 'adr_type'
      , [ ( 'code'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'description'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'typecat'
          , ["admin", "adr_readonly", "user"]
          )
        ]
      )
    , ( 'adr_type_cat'
      , [ ( 'code'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'description'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'type_valid'
          , ["admin", "adr_readonly", "user"]
          )
        ]
      )
    , ( 'bank_account'
      , [ ( 'act_number'
          , ["admin", "user"]
          )
        , ( 'bank'
          , ["admin", "user"]
          )
        , ( 'bank_code'
          , ["admin", "user"]
          )
        , ( 'bic'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        , ( 'iban'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'contact'
      , [ ( 'contact'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'contact_type'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'description'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'person'
          , ["admin", "adr_readonly", "user"]
          )
        ]
      )
    , ( 'contact_type'
      , [ ( 'description'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'name'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'order'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'url_template'
          , ["admin", "adr_readonly", "user"]
          )
        ]
      )
    , ( 'currency'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'cust_supp'
      , [ ( 'attendant'
          , ["admin", "user"]
          )
        , ( 'bank_account'
          , ["admin", "user"]
          )
        , ( 'credit_limit'
          , ["admin", "user"]
          )
        , ( 'currency'
          , ["admin", "user"]
          )
        , ( 'customer_group'
          , ["admin", "user"]
          )
        , ( 'customer_status'
          , ["admin", "user"]
          )
        , ( 'customer_type'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        , ( 'discount_group'
          , ["admin", "user"]
          )
        , ( 'dispatch_type'
          , ["admin", "user"]
          )
        , ( 'files'
          , ["admin", "user"]
          )
        , ( 'invoice_dispatch'
          , ["admin", "user"]
          )
        , ( 'invoice_text'
          , ["admin", "user"]
          )
        , ( 'lookalike_name'
          , ["admin", "user"]
          )
        , ( 'messages'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'nosy'
          , ["admin", "user"]
          )
        , ( 'order_text'
          , ["admin", "user"]
          )
        , ( 'pharma_ref'
          , ["admin", "user"]
          )
        , ( 'sales_conditions'
          , ["admin", "user"]
          )
        , ( 'supplier_group'
          , ["admin", "user"]
          )
        , ( 'supplier_status'
          , ["admin", "user"]
          )
        , ( 'tax_id'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'customer_group'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'discount_group'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'customer_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'display'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'valid'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'customer_type'
      , [ ( 'code'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'discount_group'
      , [ ( 'currency'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        , ( 'group_discount'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'overall_discount'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'dispatch_type'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'file'
      , [ ( 'content'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'type'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'group_discount'
      , [ ( 'discount'
          , ["admin", "user"]
          )
        , ( 'product_group'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'invoice'
      , [
        ]
      )
    , ( 'invoice_dispatch'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'invoice_template'
      , [ ( 'interval'
          , ["admin", "invoice"]
          )
        , ( 'invoice_level'
          , ["admin", "invoice"]
          )
        , ( 'name'
          , ["admin", "invoice"]
          )
        , ( 'tmplate'
          , ["admin", "invoice"]
          )
        ]
      )
    , ( 'letter'
      , [ ( 'address'
          , ["admin", "user"]
          )
        , ( 'date'
          , ["admin", "user"]
          )
        , ( 'files'
          , ["admin", "user"]
          )
        , ( 'messages'
          , ["admin", "user"]
          )
        , ( 'subject'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'measuring_unit'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'msg'
      , [ ( 'author'
          , ["admin", "user"]
          )
        , ( 'content'
          , ["admin", "user"]
          )
        , ( 'date'
          , ["admin", "user"]
          )
        , ( 'files'
          , ["admin", "user"]
          )
        , ( 'inreplyto'
          , ["admin", "user"]
          )
        , ( 'messageid'
          , ["admin", "user"]
          )
        , ( 'recipients'
          , ["admin", "user"]
          )
        , ( 'summary'
          , ["admin", "user"]
          )
        , ( 'type'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'opening_hours'
      , [ ( 'from_hour'
          , ["admin", "user"]
          )
        , ( 'from_minute'
          , ["admin", "user"]
          )
        , ( 'to_hour'
          , ["admin", "user"]
          )
        , ( 'to_minute'
          , ["admin", "user"]
          )
        , ( 'weekday'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'overall_discount'
      , [ ( 'discount'
          , ["admin", "user"]
          )
        , ( 'price'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'packaging_unit'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'payment'
      , [ ( 'amount'
          , ["admin", "invoice"]
          )
        , ( 'date_payed'
          , ["admin", "invoice"]
          )
        , ( 'invoice'
          , ["admin", "invoice"]
          )
        , ( 'receipt_no'
          , ["admin", "invoice"]
          )
        ]
      )
    , ( 'person'
      , [ ( 'address'
          , ["admin", "user"]
          )
        , ( 'affix'
          , ["admin", "user"]
          )
        , ( 'birthdate'
          , ["admin", "user"]
          )
        , ( 'contacts'
          , ["admin", "user"]
          )
        , ( 'cust_supp'
          , ["admin", "user"]
          )
        , ( 'description'
          , ["admin", "user"]
          )
        , ( 'files'
          , ["admin", "user"]
          )
        , ( 'firstname'
          , ["admin", "user"]
          )
        , ( 'function'
          , ["admin", "user"]
          )
        , ( 'initial'
          , ["admin", "user"]
          )
        , ( 'lastname'
          , ["admin", "user"]
          )
        , ( 'lettertitle'
          , ["admin", "user"]
          )
        , ( 'lookalike_firstname'
          , ["admin", "user"]
          )
        , ( 'lookalike_function'
          , ["admin", "user"]
          )
        , ( 'lookalike_lastname'
          , ["admin", "user"]
          )
        , ( 'messages'
          , ["admin", "user"]
          )
        , ( 'person_type'
          , ["admin", "user"]
          )
        , ( 'salutation'
          , ["admin", "user"]
          )
        , ( 'title'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'person_type'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'pharma_ref'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'proceeds_group'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'product'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'files'
          , ["admin", "user"]
          )
        , ( 'measuring_unit'
          , ["admin", "user"]
          )
        , ( 'messages'
          , ["admin", "user"]
          )
        , ( 'minimum_inventory'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'packaging_unit'
          , ["admin", "user"]
          )
        , ( 'proceeds_group'
          , ["admin", "user"]
          )
        , ( 'product_group'
          , ["admin", "user"]
          )
        , ( 'product_price'
          , ["admin", "user"]
          )
        , ( 'shelf_life_code'
          , ["admin", "user"]
          )
        , ( 'status'
          , ["admin", "user"]
          )
        , ( 'use_lot'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'product_group'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'product_price'
      , [ ( 'currency'
          , ["admin"]
          )
        , ( 'price'
          , ["admin"]
          )
        , ( 'vat_percent'
          , ["admin"]
          )
        ]
      )
    , ( 'product_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'valid'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'query'
      , [ ( 'klass'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'private_for'
          , ["admin", "user"]
          )
        , ( 'tmplate'
          , ["admin", "user"]
          )
        , ( 'url'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'sales_conditions'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'discount_days'
          , ["admin", "user"]
          )
        , ( 'discount_percent'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'payment_days'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'shelf_life_code'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'shelf_life'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'stock'
      , [ ( 'description'
          , ["admin"]
          )
        , ( 'name'
          , ["admin"]
          )
        , ( 'storage'
          , ["admin"]
          )
        ]
      )
    , ( 'stocked_product'
      , [ ( 'lot'
          , ["admin"]
          )
        , ( 'on_stock'
          , ["admin"]
          )
        , ( 'product'
          , ["admin"]
          )
        , ( 'storage_location'
          , ["admin"]
          )
        ]
      )
    , ( 'storage'
      , [ ( 'description'
          , ["admin"]
          )
        , ( 'name'
          , ["admin"]
          )
        , ( 'storage_locations'
          , ["admin"]
          )
        ]
      )
    , ( 'storage_location'
      , [
        ]
      )
    , ( 'supplier_group'
      , [ ( 'description'
          , ["admin"]
          )
        , ( 'name'
          , ["admin"]
          )
        ]
      )
    , ( 'supplier_status'
      , [ ( 'description'
          , ["admin"]
          )
        , ( 'display'
          , ["admin"]
          )
        , ( 'name'
          , ["admin"]
          )
        , ( 'order'
          , ["admin"]
          )
        , ( 'valid'
          , ["admin"]
          )
        ]
      )
    , ( 'tmplate'
      , [ ( 'files'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'tmplate_status'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'tmplate_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        , ( 'use_for_invoice'
          , ["admin", "user"]
          )
        , ( 'use_for_letter'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'user'
      , [ ( 'address'
          , ["admin", "user"]
          )
        , ( 'alternate_addresses'
          , ["admin", "user"]
          )
        , ( 'password'
          , ["admin", "user"]
          )
        , ( 'phone'
          , ["admin", "user"]
          )
        , ( 'queries'
          , ["admin", "user"]
          )
        , ( 'realname'
          , ["admin", "user"]
          )
        , ( 'roles'
          , ["admin", "user"]
          )
        , ( 'status'
          , ["admin", "user"]
          )
        , ( 'timezone'
          , ["admin", "user"]
          )
        , ( 'username'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'user_status'
      , [ ( 'description'
          , ["admin", "user"]
          )
        , ( 'name'
          , ["admin", "user"]
          )
        ]
      )
    , ( 'valid'
      , [ ( 'description'
          , ["admin", "adr_readonly", "user"]
          )
        , ( 'name'
          , ["admin", "adr_readonly", "user"]
          )
        ]
      )
    , ( 'weekday'
      , [ ( 'name'
          , ["admin", "user"]
          )
        , ( 'order'
          , ["admin", "user"]
          )
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
