# -*- coding: utf-8 -*-

from five import grok
from z3c.form import group, field
from zope import schema
from zope.interface import Interface, invariant, Invalid
from plone.directives import dexterity, form
from plone.app.textfield import RichText

from sinanet.gelso import MessageFactory as _


# Interface class; used to define content-type schema.

class IStoricoComunicazioni(form.Schema):
    """
    Scheda per gestire le comunicazioni con i referenti
    """
    title = schema.TextLine(
    title=_(u"Titolo"),
    description=_("Titolo da assegnare alla nota"),
    required=True,
    )

    data_contatto = schema.Date(
        title=_(u"Data di contatto"),
        description=_(""),
        required=False,
        )
    
    Note = RichText(
    title=_(u"Note"),
    description=_(""),
    required=True,
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
