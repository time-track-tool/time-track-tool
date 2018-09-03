#! /usr/bin/python
# -*- coding: iso-8859-1 -*-
# Copyright (C) 2014-15 Dr. Ralf Schlatterbeck Open Source Consulting.
# Reichergasse 131, A-3411 Weidling.
# Web: http://www.runtux.com Email: office@runtux.com
# All rights reserved
# ****************************************************************************
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 675 Mass Ave, Cambridge, MA 02139, USA.
#++
# Name
#    interfaces
#
# Purpose
#    Override classes in roundup
#--
#
import roundup.mailgw
from rsclib.autosuper import autosuper

class parsedMessage (roundup.mailgw.parsedMessage, autosuper) :
    def create_msg (self) :
        self.__super.create_msg ()
        if  ('messages' in self.props and 'header' in self.db.msg.properties) :
            msgid = self.props ['messages'][-1]
            h = self.message.as_string().split ('\n\n', 1) [0]
            self.db.msg.set (msgid, header = h)
    # end def create_msg
# end class parsedMessage

class MailGW (roundup.mailgw.MailGW) :
    parsed_message_class = parsedMessage
# end class MailGW
