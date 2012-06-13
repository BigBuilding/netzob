# -*- coding: utf-8 -*-

#+---------------------------------------------------------------------------+
#|          01001110 01100101 01110100 01111010 01101111 01100010            |
#|                                                                           |
#|               Netzob : Inferring communication protocols                  |
#+---------------------------------------------------------------------------+
#| Copyright (C) 2011 Georges Bossert and Frédéric Guihéry                   |
#| This program is free software: you can redistribute it and/or modify      |
#| it under the terms of the GNU General Public License as published by      |
#| the Free Software Foundation, either version 3 of the License, or         |
#| (at your option) any later version.                                       |
#|                                                                           |
#| This program is distributed in the hope that it will be useful,           |
#| but WITHOUT ANY WARRANTY; without even the implied warranty of            |
#| MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the              |
#| GNU General Public License for more details.                              |
#|                                                                           |
#| You should have received a copy of the GNU General Public License         |
#| along with this program. If not, see <http://www.gnu.org/licenses/>.      |
#+---------------------------------------------------------------------------+
#| @url      : http://www.netzob.org                                         |
#| @contact  : contact@netzob.org                                            |
#| @sponsors : Amossys, http://www.amossys.fr                                |
#|             Supélec, http://www.rennes.supelec.fr/ren/rd/cidre/           |
#+---------------------------------------------------------------------------+

#+----------------------------------------------
#| Global Imports
#+----------------------------------------------
from gettext import gettext as _
import gtk
import pygtk
import logging
pygtk.require('2.0')

#+----------------------------------------------
#| Local Imports
#+----------------------------------------------
from netzob.Export.TreeViews.TreeSymbolGenerator import TreeSymbolGenerator


#+----------------------------------------------
#| ScapyExport:
#|     Class for building a scapy dissector
#+----------------------------------------------
class ScapyExport:

    #+----------------------------------------------
    #| Called when user select a new trace
    #+----------------------------------------------
    def new(self):
        pass

    def update(self):
        self.treesymbolGenerator.update()

    def clear(self):
        pass

    def kill(self):
        pass

    #+----------------------------------------------
    #| Constructor:
    #| @param netzob: the main netzob object
    #+----------------------------------------------
    def __init__(self, netzob):
        self.netzob = netzob
        self.log = logging.getLogger('netzob.Export.ScapyExport.py')

        self.init()

        self.dialog = gtk.Dialog(title=_("Export project as Scapy dissector"), flags=0, buttons=None)
        self.dialog.show()
        self.dialog.vbox.pack_start(self.getPanel(), True, True, 0)
        self.dialog.set_size_request(800, 700)
        self.update()

    def init(self):

        self.selectedSymbol = None

        # First we create an VPaned which hosts the two main children
        self.panel = gtk.HBox()
        self.panel.show()

        # Create the symbol selection treeview
        self.treeSymbolGenerator = TreeSymbolGenerator(self.netzob)
        self.treeSymbolGenerator.initialization()
        self.panel.pack_start(self.treeSymbolGenerator.getScrollLib(), True, True, 0)
        self.treeSymbolGenerator.getTreeview().connect("cursor-changed", self.symbolSelected)

        # Create the hbox content in order to display dissector data
        bottomFrame = gtk.Frame()
        bottomFrame.show()
        bottomFrame.set_size_request(550, -1)
        self.panel.add(bottomFrame)
        sw = gtk.ScrolledWindow()
        sw.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.textarea = gtk.TextView()
        self.textarea.get_buffer().create_tag("normalTag", family="Courier")
        self.textarea.show()
        self.textarea.set_editable(False)
        sw.add(self.textarea)
        sw.show()
        bottomFrame.add(sw)

    def symbolSelected(self, treeview):
        (model, iter) = treeview.get_selection().get_selected()
        if(iter):
            if(model.iter_is_valid(iter)):
                idSymbol = model.get_value(iter, 0)
                self.selectedSymbol = idSymbol
                self.updateTextareaWithDissector()

    def updateTextareaWithDissector(self):
        if self.selectedSymbol == None:
            self.textarea.get_buffer().set_text(_("Select a symbol to see its Scapy dissector"))
        else:
            found = False
            for symbol in self.netzob.getCurrentProject().getVocabulary().getSymbols():
                if str(symbol.getID()) == self.selectedSymbol:
                    self.textarea.get_buffer().set_text("")
                    self.textarea.get_buffer().insert_with_tags_by_name(self.textarea.get_buffer().get_start_iter(), symbol.getScapyDissector(), "normalTag")
                    found = True
            if found == False:
                self.log.warning(_("Impossible to retrieve the symbol having the id {0}").format(str(self.selectedSymbol)))

    #+----------------------------------------------
    #| GETTERS
    #+----------------------------------------------
    def getPanel(self):
        return self.panel
