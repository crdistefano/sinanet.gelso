from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid

from plone.dexterity.content import Container
from plone.directives import dexterity, form

from plone.app.textfield import RichText

from sinanet.gelso import MessageFactory as _


# Interface class; used to define content-type schema.

class IObiettivi(form.Schema):
    """
    Obiettivi progetto
    """
    title = schema.TextLine(
    title=_(u"Obiettivo"),
    required=True,
    )

    descrizione = RichText(
    title=_(u"Descrizione"),
    description=_(""),
    required=False,
    )

# Custom content-type class; objects created for this content type will
# be instances of this class. Use this class to add content-type specific
# methods and properties. Put methods that are mainly useful for rendering
# in separate view classes.

#class SchedaProgetto(Container):
#    grok.implements(ISchedaProgetto)

    # Add your class methods and properties here


# View class
# The view will automatically use a similarly named template in
# scheda_progetto_templates.
# Template filenames should be all lower case.
# The view will render when you request a content object with this
# interface with "/@@sampleview" appended.
# You may make this the default view for content objects
# of this type by uncommenting the grok.name line below or by
# changing the view class name and template filename to View / view.pt.

#class View(grok.View):
    """ sample view class """

#    grok.context(ISchedaProgetto)
#    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
#    def prova(self):
#       return "ciao"

#from zope.schema.vocabulary import SimpleVocabulary

#dummy_vocabulary_instance = SimpleVocabulary.fromItems([(1, 'a'), (2, 'c')])

class View(grok.View):
   
    grok.context(IObiettivi)
    grok.require('zope2.View')

   # grok.name('view')

    # Add view methods here


    def generadizionario(self):
        from zope.component import getMultiAdapter
        from Products.CMFCore.utils import getToolByName
        
        context = self.context
        request = self.request
        catalog = getToolByName(context, 'portal_catalog')
        context_state = getMultiAdapter((context, request,), name=u"plone_context_state")
        titolo = context_state.object_title()
       
        results = catalog.searchResults({'portal_type':'sinanet.gelso.schedaprogetto'})
        dizionario ={}
        for result in results:
                    scheda = result.getObject()
                    for ob in scheda.obiettivo:
                        if ob.to_object.title == unicode(titolo,  "utf-8"):
				url = result.getPath().replace('Plone','demogelso')
                                dizionario[scheda.title] = url
                   
        return dizionario

"""
Nello script il result.getPath() restituisce il percorso con /Plone/banca-dati... che di solito 
APACHE riscrive con demogelso, ma in questo caso devo riscriverlo io, quindi faccio in modo che lo 
script produca un path di questo tipo: /demogelso/banca-dati/.... 
"""

