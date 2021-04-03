classdict = \
    { 'abo' :
        [ 'aboprice.abotype'
        , 'aboprice.abotype.adr_type'
        , 'subscriber.lastname'
        , 'subscriber.firstname'
        , 'subscriber.function'
        , 'subscriber.lookalike_lastname'
        , 'subscriber.lookalike_firstname'
        , 'subscriber.lookalike_function'
        , 'subscriber.valid'
        , 'payer.lastname'
        , 'payer.firstname'
        , 'payer.function'
        , 'payer.lookalike_lastname'
        , 'payer.lookalike_firstname'
        , 'payer.lookalike_function'
        , 'payer.valid'
        ]

    , 'abo_price' :
        [ 'abotype.adr_type'
        ]

    , 'address' :
        [ 'address.street'
        , 'address.lookalike_street'
        , 'address.country'
        , 'address.postalcode'
        , 'address.city'
        , 'address.lookalike_city'
        , 'cust_supp.customer_type'
        ]

    , 'contact' :
        [ 'address.lastname'
        , 'address.firstname'
        , 'address.function'
        , 'address.lookalike_lastname'
        , 'address.lookalike_firstname'
        , 'address.lookalike_function'
        , 'customer.lastname'
        , 'customer.firstname'
        , 'customer.function'
        , 'customer.lookalike_lastname'
        , 'customer.lookalike_firstname'
        , 'customer.lookalike_function'
        , 'person.lastname'
        , 'person.firstname'
        , 'person.function'
        , 'person.lookalike_lastname'
        , 'person.lookalike_firstname'
        , 'person.lookalike_function'
        ]

    , 'cost_center' :
        [ 'organisation.id'
        , 'cost_center_group.id'
        ]

    , 'customer' :
        [ 'address.street'
        , 'address.lookalike_street'
        , 'address.country'
        , 'address.postalcode'
        , 'address.city'
        , 'address.lookalike_city'
        , 'cust_supp.customer_type'
        ]

    , 'discount_group' :
        [ 'group_discount.product_group'
        ]

    , 'invoice' :
        [ 'subscriber.lastname'
        , 'subscriber.firstname'
        , 'subscriber.function'
        , 'subscriber.lookalike_lastname'
        , 'subscriber.lookalike_firstname'
        , 'subscriber.lookalike_function'
        , 'subscriber.valid'
        , 'payer.lastname'
        , 'payer.firstname'
        , 'payer.function'
        , 'payer.lookalike_lastname'
        , 'payer.lookalike_firstname'
        , 'payer.lookalike_function'
        , 'payer.valid'
        , 'abo.aboprice'
        , 'abo.aboprice.abotype'
        , 'abo.aboprice.abotype.adr_type'
        ]

    , 'issue' :
        [ 'depends.id'
        , 'needs.id'
        , 'composed_of.id'
        , 'part_of.id'
        ]

    , 'letter' :
        [ 'address.lastname'
        , 'address.firstname'
        , 'address.function'
        , 'address.lookalike_lastname'
        , 'address.lookalike_firstname'
        , 'address.lookalike_function'
        , 'address.valid'
        ]

    , 'measurement' :
        [ 'sensor.device.device_group'
        , 'sensor.device.transceiver'
        , 'sensor.device.adr'
        , 'sensor.device.order'
        , 'sensor.device'
        , 'sensor.device.dev'
        , 'sensor.device.cls'
        , 'sensor.device.name'
        , 'sensor.adr'
        , 'sensor.type'
        , 'sensor.name'
        , 'sensor.unit'
        , 'sensor.order'
        , 'sensor.do_logging'
        , 'sensor.is_actuator'
        , 'sensor.is_app_sensor'
        ]

    , 'payment' :
        [ 'invoice.period_start'
        , 'invoice.period_end'
        , 'invoice.currency'
        , 'invoice.amount'
        , 'invoice.open'
        , 'invoice.subscriber.lastname'
        , 'invoice.subscriber.firstname'
        , 'invoice.subscriber.function'
        , 'invoice.subscriber.lookalike_lastname'
        , 'invoice.subscriber.lookalike_firstname'
        , 'invoice.subscriber.lookalike_function'
        , 'invoice.subscriber.valid'
        , 'invoice.payer.lastname'
        , 'invoice.payer.firstname'
        , 'invoice.payer.function'
        , 'invoice.payer.lookalike_lastname'
        , 'invoice.payer.lookalike_firstname'
        , 'invoice.payer.lookalike_function'
        , 'invoice.payer.valid'
        , 'invoice.abo'
        , 'invoice.abo.aboprice'
        , 'invoice.abo.aboprice.abotype'
        , 'invoice.invoice_group'
        ]

    , 'person' :
        [ 'address.street'
        , 'address.lookalike_street'
        , 'address.country'
        , 'address.postalcode'
        , 'address.city'
        , 'address.lookalike_city'
        , 'cust_supp.customer_type'
        ]

    , 'sensor' :
        [ 'device.device_group'
        , 'device.transceiver'
        , 'device'
        , 'device.adr'
        , 'device.order'
        , 'device.dev'
        , 'device.cls'
        , 'device.name'
        ]

    , 'support' :
        [ 'related_issues.id'
        ]

    , 'time_project' :
        [ 'organisation.id'
        , 'wps.bookers'
        ]

    , 'time_record' :
        [ 'daily_record.user'
        , 'daily_record.date'
        , 'daily_record.status'
        , 'wp.project'
        ]
    , 'user' :
        [ 'planning_role.functional_role'
        ]
    }
