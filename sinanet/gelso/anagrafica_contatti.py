# -*- coding: utf-8 -*-

from Products.CMFPlone.utils import safe_unicode

from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid, alsoProvides, Interface
from plone.directives import dexterity, form

from plone.supermodel import model

from plone.formwidget.masterselect import (
    _, 
    MasterSelectField, 
)

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory

from z3c.relationfield.schema import RelationChoice, RelationList
from plone.formwidget.contenttree import ObjPathSourceBinder

from sinanet.gelso import MessageFactory as _
from sinanet.gelso.storico_comunicazioni import IStoricoComunicazioni
from sinanet.gelso.promotori import IPromotori

from redturtle.entiterritoriali import EntiVocabulary as EV
from redturtle.entiterritoriali.vocabulary import mapDisplayList




def getSlaveVocabProvince(master):
    """recupera il vocabolario delle province per regione selezionata"""
    results =[]
    lista=[]
    tupla=()
    for a in mapDisplayList(EV.allRegioni()):
       if master == a[1]:
           results = [b for b in mapDisplayList((EV.province4regione(a[0])))]
    for result in results:
        lista.append(result[1])
    return lista

def getSlaveVocabComuni(master2):
    """recupera il vocabolario dei comuni per provincia selezionata
    """
    results=[]
    lista=[]
    tupla=()
    for a in mapDisplayList(EV.allProvince()):
        if master2 == a[1]:
            results = [a for a in EV.comuni4provincia(a[0])]
    for result in results:
        tupla = (result.comune)
        lista.append(tupla)
    return lista



# Interface class; used to define content-type schema.

class IAnagraficaContatti(form.Schema):
    """
    Anagrafica dei contatti referenti
    """
    title = schema.TextLine(
    title=_(u"Referente Progetto"),
    description=_("Nome e cognome del referente"),
    required=True,
    )

    unita_organizzativa = schema.TextLine(
        title=_(u"Unità organizzativa"),
        description=_(""),
        required=False,
        )
    
    ruolo = schema.TextLine(
        title=_("Ruolo"), 
        description=_(""), 
        required=False,                         
        )
    

    
    regione = MasterSelectField(
        title=_(u"Regione"),
        description=_(u""),
        values=(a[1] for a in mapDisplayList(EV.allRegioni())), 
        #values=('a', 'b', 'c', 'd', 'e', 'f'),
        slave_fields=(
            # Controls the vocab of slaveMasterField
            {'name': 'slaveMasterFieldProvincia',
             'action': 'vocabulary',
             'vocab_method': getSlaveVocabProvince,
             'control_param': 'master',
            },
        ),
        required=False,
    )

    slaveMasterFieldProvincia = MasterSelectField(
        title=_(u"Provincia"),
        description=_(u""),
        values=(u""),
        slave_fields=(
            {'name': 'slaveFieldComune',
             'action': 'vocabulary',
             'vocab_method': getSlaveVocabComuni,
             'control_param': 'master2',
            },
        ),
        required=False,
    )

    slaveFieldComune = schema.Choice(
        title=_(u"Comune"),
        description=_(u""),
        values=(u""),
        required=False,
    )
    
     
    indirizzo = schema.Text(
    title=_(u"Indirizzo"),
    description=_(""),
    required=False,
    )

    email = schema.TextLine(
    title=_(u"email"),
    description=_(""),
    required=False,
    )

    telefono = schema.TextLine(
        title=_(u"Telefono"),
        description=_(""),
        required=False,
        )

    skype = schema.TextLine(
        title=_(u"Skype"),
        description=_(""),
        required=False,
        )
    
    relatedItems = RelationList(
    title=u"Comunicazioni avute",
    default=[],
    value_type=RelationChoice(title=_(u"Related"),
         source=ObjPathSourceBinder(object_provides=IStoricoComunicazioni.__identifier__)),
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



class Alternativa(grok.View):

   
    grok.context(IAnagraficaContatti)
    grok.require('zope2.View')

#    grok.name('view')

    # Add view methods here
    def prova(self):
            from zope.component import getMultiAdapter
            from zope.component.hooks import getSite


            site = getSite()
            catalog = site.portal_catalog                    
            context = self.context
            request = self.request
            context_state = getMultiAdapter((context, request,), name=u"plone_context_state")
            results = catalog.searchResults({'Title':context_state.object_title(), \
                                                                'portal_type':'sinanet.gelso.anagraficacontatti'})
       
            for result in results:
                    context = result.getObject()

            
            return context
