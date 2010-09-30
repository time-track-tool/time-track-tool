properties = \
    [ ( 'device'
      , [ 'adr'
        , 'cls'
        , 'dev'
        , 'device_group'
        , 'gapint'
        , 'mint'
        , 'name'
        , 'order'
        , 'rec'
        , 'sint'
        , 'surrogate'
        , 'transceiver'
        , 'version'
        ]
      )
    , ( 'device_group'
      , [ 'description'
        , 'name'
        , 'order'
        ]
      )
    , ( 'dyndns'
      , [ 'fw_login'
        , 'fw_password'
        , 'fw_skip'
        , 'fw_url'
        , 'interface'
        , 'interface_skip'
        , 'local_hostname'
        , 'syslog'
        , 'web_skip'
        , 'web_url'
        ]
      )
    , ( 'dyndns_host'
      , [ 'description'
        , 'dyndns_service'
        , 'hostname'
        ]
      )
    , ( 'dyndns_protocol'
      , [ 'default_server'
        , 'description'
        , 'name'
        , 'order'
        ]
      )
    , ( 'dyndns_service'
      , [ 'dyndns'
        , 'login'
        , 'password'
        , 'protocol'
        , 'server'
        ]
      )
    , ( 'file'
      , [ 'content'
        , 'name'
        , 'type'
        ]
      )
    , ( 'logstyle'
      , [ 'description'
        , 'name'
        , 'order'
        ]
      )
    , ( 'measurement'
      , [ 'date'
        , 'sensor'
        , 'val'
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
    , ( 'query'
      , [ 'klass'
        , 'name'
        , 'private_for'
        , 'tmplate'
        , 'url'
        ]
      )
    , ( 'sensor'
      , [ 'adr'
        , 'almax'
        , 'almin'
        , 'device'
        , 'do_logging'
        , 'is_actuator'
        , 'is_app_sensor'
        , 'name'
        , 'order'
        , 'surrogate'
        , 'type'
        , 'unit'
        ]
      )
    , ( 'transceiver'
      , [ 'mint'
        , 'name'
        , 'sint'
        , 'tty'
        ]
      )
    , ( 'user'
      , [ 'address'
        , 'alternate_addresses'
        , 'csv_delimiter'
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
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
