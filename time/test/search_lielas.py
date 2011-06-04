properties = \
    [ ( 'device'
      , [ ( 'adr'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'cls'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'dev'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'device_group'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'gapint'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'mint'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'mint_pending'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'name'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'order'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'rec'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'sint'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'sint_pending'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'surrogate'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'transceiver'
          , ['admin', 'guest', 'logger', 'user']
          )
        , ( 'version'
          , ['admin', 'guest', 'logger', 'user']
          )
        ]
      )
    , ( 'device_group'
      , [ ( 'description'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'name'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'order'
          , ["admin", "guest", "logger", "user"]
          )
        ]
      )
    , ( 'dyndns'
      , [ ( 'fw_login'
          , ["admin"]
          )
        , ( 'fw_password'
          , ["admin"]
          )
        , ( 'fw_skip'
          , ["admin"]
          )
        , ( 'fw_url'
          , ["admin"]
          )
        , ( 'interface'
          , ["admin"]
          )
        , ( 'interface_skip'
          , ["admin"]
          )
        , ( 'local_hostname'
          , ["admin"]
          )
        , ( 'syslog'
          , ["admin"]
          )
        , ( 'web_skip'
          , ["admin"]
          )
        , ( 'web_url'
          , ["admin"]
          )
        ]
      )
    , ( 'dyndns_host'
      , [ ( 'description'
          , ["admin"]
          )
        , ( 'dyndns_service'
          , ["admin"]
          )
        , ( 'hostname'
          , ["admin"]
          )
        ]
      )
    , ( 'dyndns_protocol'
      , [ ( 'default_server'
          , ["admin"]
          )
        , ( 'description'
          , ["admin"]
          )
        , ( 'name'
          , ["admin"]
          )
        , ( 'order'
          , ["admin"]
          )
        ]
      )
    , ( 'dyndns_service'
      , [ ( 'dyndns'
          , ["admin"]
          )
        , ( 'login'
          , ["admin"]
          )
        , ( 'password'
          , ["admin"]
          )
        , ( 'protocol'
          , ["admin"]
          )
        , ( 'server'
          , ["admin"]
          )
        ]
      )
    , ( 'email'
      , [ ( 'password'
          , ["admin"]
          )
        , ( 'sender'
          , ["admin"]
          )
        , ( 'server'
          , ["admin"]
          )
        , ( 'user_name'
          , ["admin"]
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
    , ( 'logstyle'
      , [ ( 'description'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'name'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'order'
          , ["admin", "guest", "logger", "user"]
          )
        ]
      )
    , ( 'measurement'
      , [ ( 'date'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'sensor'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'val'
          , ["admin", "guest", "logger", "user"]
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
    , ( 'sensor'
      , [ ( 'adr'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'almax'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'almin'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'device'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'do_logging'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'is_actuator'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'is_app_sensor'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'name'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'order'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'surrogate'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'type'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'unit'
          , ["admin", "guest", "logger", "user"]
          )
        ]
      )
    , ( 'transceiver'
      , [ ( 'mint'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'mint_pending'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'name'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'sint'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'sint_pending'
          , ["admin", "guest", "logger", "user"]
          )
        , ( 'tty'
          , ["admin", "guest", "logger", "user"]
          )
        ]
      )
    , ( 'umts'
      , [ ( 'pin'
          , ["admin"]
          )
        , ( 'tty'
          , ["admin"]
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
        , ( 'csv_delimiter'
          , ["admin", "user"]
          )
        , ( 'password'
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
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
