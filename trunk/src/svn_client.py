"""
Gnome-enabled SVN client.
"""

import pysvn

def getStatusString(statusKind):
    """
    """
    if statusKind == pysvn.wc_status_kind.added:
        return 'Added'
    if statusKind == pysvn.wc_status_kind.conflicted:
        return 'Conflicted'
    if statusKind == pysvn.wc_status_kind.deleted:
        return 'Deleted'
    if statusKind == pysvn.wc_status_kind.external:
        return 'External'
    if statusKind == pysvn.wc_status_kind.ignored:
        return 'Ignored'
    if statusKind == pysvn.wc_status_kind.incomplete:
        return 'Incomplete'
    if statusKind == pysvn.wc_status_kind.merged:
        return 'Merged'
    if statusKind == pysvn.wc_status_kind.missing:
        return 'Missing'
    if statusKind == pysvn.wc_status_kind.modified:
        return 'Modified'
    if statusKind == pysvn.wc_status_kind.none:
        return 'None'
    if statusKind == pysvn.wc_status_kind.normal:
        return 'Normal'
    if statusKind == pysvn.wc_status_kind.obstructed:
        return 'Obstructed'
    if statusKind == pysvn.wc_status_kind.replaced:
        return 'Replaced'
    if statusKind == pysvn.wc_status_kind.unversioned:
        return 'Unversioned'

def isCommittable(statusKind):
    return  statusKind in (pysvn.wc_status_kind.added,
                           pysvn.wc_status_kind.deleted,
                           pysvn.wc_status_kind.merged,
                           pysvn.wc_status_kind.modified)


class GnomeClient(object):
    """
    """
    def __init__(self, *arg, **kwarg):
        self._client = pysvn.Client(*arg, **kwarg)
        
    def __getattr__(self, name):
        return getattr(self._client, name)

    def is_committable(self, path, recursive=False):
        """
        Checks wether or not a file or directory can be committed.

        path - The file or directory to test
        recursive - If "path" is a directory and "recursive" is True,
                    look recursively for files that can be committed

        Returns: True if "path" can be committed, otherwise False.
        """
        status = self._client.status(path)
        return isCommittable(status[0].text_status)

    def status_string(self, path):
        """
        Return a string that describes the status of path
        """
        status = self._client.status(path)
        return getStatusString(status[0].text_status)

    def is_working_copy(self, path):
        """
        Checks if path is in a working copy.
        path can be a file or a directory.
        """
        try:
            self._client.status(path)
        except pysvn.ClientError, e:
            return False
        return True
