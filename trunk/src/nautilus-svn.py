"""
This file should be copied to wherever nautilus-python looks for files.
"""
import nautilus

import urllib
import os

SCRIPT_PATH= '/home/laz/src/nautilus-svn/src/'

import sys
sys.path.append(SCRIPT_PATH)
import svn_client
svnClient = svn_client.GnomeClient()

_debugfile = None
def DEBUG(str):
    global _debugfile
    if not _debugfile:
        _debugfile = file('/tmp/nautilus-svn.debug', 'w')

    _debugfile.write(str)
    _debugfile.write('\n')
    _debugfile.flush()

def get_filenames(files):
    """
    Strip leading file://
    """
    return map(lambda x: urllib.unquote(x.get_uri()[7:]), files)
    
class NautilusExtension(nautilus.MenuProvider):
    def __init__(self):
        self._scriptpath = '/home/laz/src/nautilus-svn/src/'
        DEBUG('nautilus-svn initiated.')
        
    def commit_cb(self, menu, files):
        DEBUG('Execute on: %r' % map(lambda x:x.get_uri(), files))

        # We can't commit files that no longer exist, so
        # remove them
        files = filter(lambda x:not x.is_gone(), files)
        if len(files) == 0:
            return

        cmdarr = [self._scriptpath + 'nautilus-svn-commit.py']
        cmdarr.extend(get_filenames(files))
        DEBUG('Command array: %r' % (cmdarr,))
        os.spawnv(os.P_NOWAIT, cmdarr[0], cmdarr)
        
    def get_file_items(self, window, files):
        if not files:
            return
        
        for fileOb in files:
            ## TODO: Check if the files are in a subversion working copy
            if fileOb.get_uri_scheme() != 'file':
                DEBUG('URI for %s is not file, aborting.' % fileOb.get_uri())
                return

        global svnClient
        items = []

        for filename in get_filenames(files):
            if not (svnClient.is_working_copy(filename) and
                    svnClient.is_committable(filename)):
                break
        else:
            item = nautilus.MenuItem('Nautilus::svn_commit',
                                     'SVN Commit',
                                     'Commit file(s) to the Subversion '
                                     'repository')
            item.connect('activate', self.commit_cb, files)
            items.append(item)
        return items
