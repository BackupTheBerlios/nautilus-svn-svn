#!/usr/bin/env python

##
## gsvn_commit.py - a Gnome/GTK interface to svn commit
## (c) 2005 Fredrik Juhlin <juhlin@gmail.com>
##
## Usage: gsvn_commit.py path [path2] ...
##

import sys

import pygtk
pygtk.require("2.0")

import gtk
import gtk.glade
import gobject

import svn_client

class CommitApp:
    def __init__(self, svnClient):
        self._svnClient = svnClient

        gladefile = "/home/laz/src/nautilus-svn/src/nautilus-svn.glade"
        windowname = "svn_commit"

        self._wTree = gtk.glade.XML(gladefile, windowname)

        signalDict = { "on_svn_commit_destroy": gtk.main_quit,
                       "on_cancelButton_clicked": gtk.main_quit,
                       "on_okButton_clicked": self._ok_button_clicked
                       }
        self._wTree.signal_autoconnect(signalDict)

        self._view = self._wTree.get_widget('commitFileList')
        self._commit_textview = self._wTree.get_widget('commit_comment')

        ## The model columns are:
        ## 0. path of file
        ## 1. Status string (Added, Modified, Not Modified...)
        ## 2. If it CAN be committed (e.g. is changed somehow)
        ## 3. If the user wants it committed
        self._model = gtk.ListStore(gobject.TYPE_STRING, gobject.TYPE_STRING,
                                    gobject.TYPE_BOOLEAN, gobject.TYPE_BOOLEAN)
        self._view.set_model(self._model)

        renderer = gtk.CellRendererToggle()
        column = gtk.TreeViewColumn("Commit", renderer, activatable=2,
                                    active=3)
        self._view.append_column(column)
        renderer.connect('toggled', self._view_toggled)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("File", renderer, text=0)
        column.set_expand(True)
        self._view.append_column(column)

        renderer = gtk.CellRendererText()
        column = gtk.TreeViewColumn("Status", renderer, text=1)
        self._view.append_column(column)

    def addFiles(self, paths):
        """
        """
        model = self._model
        for path in paths:
            iter = self._model.insert_before(None)
            committable = self._svnClient.is_committable(path)
            model.set_value(iter, 0, path)
            model.set_value(iter, 1, self._svnClient.status_string(path))
            model.set_value(iter, 2, committable)
            model.set_value(iter, 3, committable)
            
    def _view_toggled(self, renderer, path):
        model = self._model
        iter = model.get_iter(path)
        currentValue = model.get_value(iter, 4)
        model.set_value(iter, 4, not currentValue)

    def _ok_button_clicked(self, button):
        self._commit()
        gtk.main_quit()
        
    def _commit(self):
        files_to_commit = [x[1] for x in iter(self._model) if x[4]]
        if len(files_to_commit) == 0:
            return
                
        buff = self._commit_textview.get_buffer()
        message = buff.get_text(*buff.get_bounds())
        print 'Committing...', 
        self._svnClient.checkin(files_to_commit, message, recurse=False)
        print 'Done.'

def main(argv):
    paths = argv[1:]

    client = svn_client.GnomeClient()
    w = CommitApp(client)
    w.addFiles(paths)
    
    gtk.main()

if __name__ == "__main__":
    main(sys.argv)
