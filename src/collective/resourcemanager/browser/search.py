from plone import api
from Products.CMFCore.interfaces import IFolderish
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from ..interfaces import ICollectiveResourcemanagerLayer


def existing_copies(context):
    images = api.content.find(
        context=get_container(context),
        portal_type='Image')
    return [x.external_img_id for x in images if getattr(x, 'external_img_id', False)]


def get_container(self):
    """If we are on a non-folderish object, return the parent
       otherwise return the object
    """
    if IFolderish.providedBy(self):
        return self
    return self.aq_parent


class ResourceSearch(BrowserView):
    """Search selected resources
    """

    template = ViewPageTemplateFile('templates/rm_search.pt')

    def __init__(self, context, request):
        self.context = context
        self.request = request
        self.search_context = 'rm-search'
        self.resources = []
        for item in ICollectiveResourcemanagerLayer.dependents.keys():
            inherited = getattr(item, 'inherit', None)
            if not inherited:
                continue
            self.resources.append(inherited(context, request))

    def __call__(self):
        self.search_context = self.request._steps[-1]
        return self.template()


class ResourceCopy(BrowserView):
    """Copy selected media to the current folder
    """

    def __init__(self, context, request):
        self.context = context
        self.request = request
