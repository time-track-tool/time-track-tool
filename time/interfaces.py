import roundup.mailgw
from rsclib.autosuper import autosuper

class parsedMessage (roundup.mailgw.parsedMessage, autosuper) :
    def create_msg (self) :
        self.__super.create_msg ()
        if  (   'customer' in self.db.classes
            and self.classname == 'support'
            and 'messages' in self.props
            and 'header' in self.db.msg.properties
            ) :
            msgid = self.props ['messages'][-1]
            self.db.msg.set (msgid, header = ''.join (self.message.headers))
    # end def get_headers
# end class parsedMessage

class MailGW (roundup.mailgw.MailGW) :
    parsed_message_class = parsedMessage
# end class MailGW
