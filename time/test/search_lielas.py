properties = \
    [ ( 'device'
      , [ ( 'adr'
          , ["guest", "logger", "user"]
          )
        , ( 'cls'
          , ["guest", "logger", "user"]
          )
        , ( 'dev'
          , ["guest", "logger", "user"]
          )
        , ( 'device_group'
          , ["guest", "logger", "user"]
          )
        , ( 'gapint'
          , ["guest", "logger", "user"]
          )
        , ( 'mint'
          , ["guest", "logger", "user"]
          )
        , ( 'name'
          , ["guest", "logger", "user"]
          )
        , ( 'order'
          , ["guest", "logger", "user"]
          )
        , ( 'rec'
          , ["guest", "logger", "user"]
          )
        , ( 'sint'
          , ["guest", "logger", "user"]
          )
        , ( 'surrogate'
          , ["guest", "logger", "user"]
          )
        , ( 'transceiver'
          , ["guest", "logger", "user"]
          )
        , ( 'version'
          , ["guest", "logger", "user"]
          )
        ]
      )
    , ( 'device_group'
      , [ ( 'description'
          , ["guest", "logger", "user"]
          )
        , ( 'name'
          , ["guest", "logger", "user"]
          )
        , ( 'order'
          , ["guest", "logger", "user"]
          )
        ]
      )
    , ( 'dyndns'
      , [ ( 'fw_login'
          , []
          )
        , ( 'fw_password'
          , []
          )
        , ( 'fw_skip'
          , []
          )
        , ( 'fw_url'
          , []
          )
        , ( 'interface'
          , []
          )
        , ( 'interface_skip'
          , []
          )
        , ( 'local_hostname'
          , []
          )
        , ( 'syslog'
          , []
          )
        , ( 'web_skip'
          , []
          )
        , ( 'web_url'
          , []
          )
        ]
      )
    , ( 'dyndns_host'
      , [ ( 'description'
          , []
          )
        , ( 'dyndns_service'
          , []
          )
        , ( 'hostname'
          , []
          )
        ]
      )
    , ( 'dyndns_protocol'
      , [ ( 'default_server'
          , []
          )
        , ( 'description'
          , []
          )
        , ( 'name'
          , []
          )
        , ( 'order'
          , []
          )
        ]
      )
    , ( 'dyndns_service'
      , [ ( 'dyndns'
          , []
          )
        , ( 'login'
          , []
          )
        , ( 'password'
          , []
          )
        , ( 'protocol'
          , []
          )
        , ( 'server'
          , []
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
    , ( 'logstyle'
      , [ ( 'description'
          , ["guest", "logger", "user"]
          )
        , ( 'name'
          , ["guest", "logger", "user"]
          )
        , ( 'order'
          , ["guest", "logger", "user"]
          )
        ]
      )
    , ( 'measurement'
      , [ ( 'date'
          , ["guest", "logger", "user"]
          )
        , ( 'sensor'
          , ["guest", "logger", "user"]
          )
        , ( 'val'
          , ["guest", "logger", "user"]
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
    , ( 'sensor'
      , [ ( 'adr'
          , ["guest", "logger", "user"]
          )
        , ( 'almax'
          , ["guest", "logger", "user"]
          )
        , ( 'almin'
          , ["guest", "logger", "user"]
          )
        , ( 'device'
          , ["guest", "logger", "user"]
          )
        , ( 'do_logging'
          , ["guest", "logger", "user"]
          )
        , ( 'is_actuator'
          , ["guest", "logger", "user"]
          )
        , ( 'is_app_sensor'
          , ["guest", "logger", "user"]
          )
        , ( 'name'
          , ["guest", "logger", "user"]
          )
        , ( 'order'
          , ["guest", "logger", "user"]
          )
        , ( 'surrogate'
          , ["guest", "logger", "user"]
          )
        , ( 'type'
          , ["guest", "logger", "user"]
          )
        , ( 'unit'
          , ["guest", "logger", "user"]
          )
        ]
      )
    , ( 'transceiver'
      , [ ( 'mint'
          , ["guest", "logger", "user"]
          )
        , ( 'name'
          , ["guest", "logger", "user"]
          )
        , ( 'sint'
          , ["guest", "logger", "user"]
          )
        , ( 'tty'
          , ["guest", "logger", "user"]
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
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
