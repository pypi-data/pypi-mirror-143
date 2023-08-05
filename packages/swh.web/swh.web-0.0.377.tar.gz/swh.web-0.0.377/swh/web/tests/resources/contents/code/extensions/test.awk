BEGIN {
  POPService  = "/inet/tcp/0/emailhost/pop3"
  RS = ORS = "\r\n"
  print "user name"            |& POPService
  POPService                    |& getline
  print "pass password"         |& POPService
  POPService                    |& getline
  print "retr 1"                |& POPService
  POPService                    |& getline
  if ($1 != "+OK") exit
  print "quit"                  |& POPService
  RS = "\r\n\\.\r\n"
  POPService |& getline
  print $0
  close(POPService)
}