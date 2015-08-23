properties = \
    [ ( 'alarm'
      , [ ( 'is_lower'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'last_triggered'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'sensor'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'timeout'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'val'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        ]
      )
    , ( 'device'
      , [ ( 'adr'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'cls'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'dev'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'device_group'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'gapint'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'mint'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'mint_pending'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'name'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'order'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'rec'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'sint'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'sint_pending'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'surrogate'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'transceiver'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'version'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        ]
      )
    , ( 'device_group'
      , [ ( 'description'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'name'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'order'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        ]
      )
    , ( 'dyndns'
      , [ ( 'fw_login'
          , ['admin']
          )
        , ( 'fw_password'
          , ['admin']
          )
        , ( 'fw_skip'
          , ['admin']
          )
        , ( 'fw_url'
          , ['admin']
          )
        , ( 'interface'
          , ['admin']
          )
        , ( 'interface_skip'
          , ['admin']
          )
        , ( 'local_hostname'
          , ['admin']
          )
        , ( 'syslog'
          , ['admin']
          )
        , ( 'web_skip'
          , ['admin']
          )
        , ( 'web_url'
          , ['admin']
          )
        ]
      )
    , ( 'dyndns_host'
      , [ ( 'description'
          , ['admin']
          )
        , ( 'dyndns_service'
          , ['admin']
          )
        , ( 'hostname'
          , ['admin']
          )
        ]
      )
    , ( 'dyndns_protocol'
      , [ ( 'default_server'
          , ['admin']
          )
        , ( 'description'
          , ['admin']
          )
        , ( 'name'
          , ['admin']
          )
        , ( 'order'
          , ['admin']
          )
        ]
      )
    , ( 'dyndns_service'
      , [ ( 'dyndns'
          , ['admin']
          )
        , ( 'login'
          , ['admin']
          )
        , ( 'password'
          , ['admin']
          )
        , ( 'protocol'
          , ['admin']
          )
        , ( 'server'
          , ['admin']
          )
        ]
      )
    , ( 'email'
      , [ ( 'password'
          , ['admin']
          )
        , ( 'sender'
          , ['admin']
          )
        , ( 'server'
          , ['admin']
          )
        , ( 'user_name'
          , ['admin']
          )
        ]
      )
    , ( 'file'
      , [ ( 'content'
          , ['admin', 'user', 'user_view']
          )
        , ( 'name'
          , ['admin', 'user', 'user_view']
          )
        , ( 'type'
          , ['admin', 'user', 'user_view']
          )
        ]
      )
    , ( 'logstyle'
      , [ ( 'description'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'name'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'order'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        ]
      )
    , ( 'measurement'
      , [ ( 'date'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'sensor'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'val'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        ]
      )
    , ( 'msg'
      , [ ( 'author'
          , ['admin', 'user', 'user_view']
          )
        , ( 'content'
          , ['admin', 'user', 'user_view']
          )
        , ( 'date'
          , ['admin', 'user', 'user_view']
          )
        , ( 'files'
          , ['admin', 'user', 'user_view']
          )
        , ( 'inreplyto'
          , ['admin', 'user', 'user_view']
          )
        , ( 'messageid'
          , ['admin', 'user', 'user_view']
          )
        , ( 'recipients'
          , ['admin', 'user', 'user_view']
          )
        , ( 'summary'
          , ['admin', 'user', 'user_view']
          )
        , ( 'type'
          , ['admin', 'user', 'user_view']
          )
        ]
      )
    , ( 'query'
      , [ ( 'klass'
          , ['admin', 'user', 'user_view']
          )
        , ( 'name'
          , ['admin', 'user', 'user_view']
          )
        , ( 'private_for'
          , ['admin', 'user', 'user_view']
          )
        , ( 'tmplate'
          , ['admin', 'user', 'user_view']
          )
        , ( 'url'
          , ['admin', 'user', 'user_view']
          )
        ]
      )
    , ( 'sensor'
      , [ ( 'adr'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'almax'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'almin'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'device'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'do_logging'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'is_actuator'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'is_app_sensor'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'name'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'order'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'surrogate'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'type'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'unit'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        ]
      )
    , ( 'transceiver'
      , [ ( 'mint'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'mint_pending'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'name'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'sint'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'sint_pending'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        , ( 'tty'
          , ['admin', 'guest', 'logger', 'user', 'user_view']
          )
        ]
      )
    , ( 'umts'
      , [ ( 'pin'
          , ['admin']
          )
        , ( 'tty'
          , ['admin']
          )
        ]
      )
    , ( 'user'
      , [ ( 'address'
          , ['admin', 'user', 'user_view']
          )
        , ( 'alternate_addresses'
          , ['admin', 'user', 'user_view']
          )
        , ( 'csv_delimiter'
          , ['admin', 'user', 'user_view']
          )
        , ( 'password'
          , ['admin', 'user', 'user_view']
          )
        , ( 'queries'
          , ['admin', 'user', 'user_view']
          )
        , ( 'realname'
          , ['admin', 'user', 'user_view']
          )
        , ( 'roles'
          , ['admin', 'user', 'user_view']
          )
        , ( 'status'
          , ['admin', 'user', 'user_view']
          )
        , ( 'timezone'
          , ['admin', 'user', 'user_view']
          )
        , ( 'username'
          , ['admin', 'user', 'user_view']
          )
        ]
      )
    , ( 'user_status'
      , [ ( 'description'
          , ['admin', 'user', 'user_view']
          )
        , ( 'is_nosy'
          , ['admin', 'user', 'user_view']
          )
        , ( 'name'
          , ['admin', 'user', 'user_view']
          )
        ]
      )
    ]

if __name__ == '__main__' :
    for cl, props in properties :
        print cl
        for p in props :
            print '    ', p
