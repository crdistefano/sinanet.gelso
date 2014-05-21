# -*- coding: utf-8 -*-


from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid
from zope.schema.interfaces import IContextSourceBinder
from z3c.relationfield.schema import RelationList, RelationChoice

from plone.formwidget.autocomplete import AutocompleteFieldWidget
from plone.formwidget.contenttree import ObjPathSourceBinder
from plone.dexterity.content import Container
from plone.directives import dexterity, form
from plone.app.textfield import RichText
from plone.namedfile.field import NamedImage, NamedFile
from plone.namedfile.field import NamedBlobImage, NamedBlobFile

from sinanet.gelso.anagrafica_contatti import IAnagraficaContatti

from sinanet.gelso import MessageFactory as _

from zope.schema.vocabulary import SimpleVocabulary, SimpleTerm
from zope.schema.interfaces import IVocabularyFactory

from plone.i18n.normalizer import idnormalizer
from plone.indexer import indexer

from Products.CMFCore.utils import getToolByName
from sinanet.gelso.obiettivi import IObiettivi

from collective import dexteritytextindexer


def make_terms(items):
    """ Create zope.schema terms for vocab from tuples """
    terms = [ SimpleTerm(value=pair[0], token=pair[0], title=pair[1]) for pair in items ]
    return terms



class Localizzazioni(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
     terms = []
     for term in ['Area boschiva', 'Area collinare','Area industriale', 'Area marina e costiera', 
                     'Area montana', 'Area periferica', 'Area protetta', 'Area residenziale', 
                     'Area rurale', 'Area turistica', 'Area umida', 'Area urbana', 'Centro Storico', 
                     'Territorio provinciale', 'Territorio regionale', 'Territorio nazionale']:
         terms.append(SimpleTerm(unicode(term, "utf-8", errors="ignore"), unicode(term, "utf-8", errors="ignore")))
     return SimpleVocabulary(terms)

grok.global_utility(Localizzazioni, name=u"localizzazioni")


class Ambiti(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
     terms = []
     for term in ['Ambito nazionale', 'Area Marina Protetta', 'Associazione', 'Autorità di bacino', 
                  'Comune', 'Comuni (più di uno)', 'Comunità montana', 'Distretto industriale', 
                  'G.A.L. gruppo di azione locale', 'Parco Nazionale', 'Parco Regionale', 
                  'Provincia', 'Regione', 'Riserva Naturale Statale o Regionale', 'Scuola']:
        token=idnormalizer.normalize(term)
        terms.append(SimpleVocabulary.createTerm(term, token, term))
     return SimpleVocabulary(terms)

grok.global_utility(Ambiti, name=u"ambiti")


class Obiettivi(object):
    grok.implements(IVocabularyFactory)
    
    def __call__(self, context):
        catalog = getToolByName(context, 'portal_catalog')
        brains = catalog.searchResults({'portal_type': 'sinanet.gelso.obiettivi'})
        result = [ (brain["UID"], brain["Title"]) for brain in brains ]
        terms = make_terms(result)
        return SimpleVocabulary(terms)
        
grok.global_utility(Obiettivi, name=u"obiettivi")
    
    
class SettoriIntervento(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
     terms = []
     for term in ['Strategie partecipate e integrate', 'Agricoltura', 'Edilizia e Urbanistica', 
                'Energia', 'Industria', 'Mobilità', 'Rifiuti', 'Territorio e Paesaggio', 'Turismo']:
        token=idnormalizer.normalize(term)
        terms.append(SimpleVocabulary.createTerm(term, token, term))
     return SimpleVocabulary(terms)

grok.global_utility(SettoriIntervento, name=u"settori_intervento")


class StrumentiFinanziamento(object):
    grok.implements(IVocabularyFactory)

    def __call__(self, context):
     terms = []
     for term in ['Bando Agenda 21 Locale 2000', 'Bando Agenda 21 Locale 2002', 'Cultura 2000', 
                'Intelligent Energy Europe', 'Fondi propri', 'Fondo Sociale Europeo', 'INTERREG', 
                'LEADER', 'LIFE', 'Piani di Sviluppo Rurale', 'Programma Quadro Ricerca e Sviluppo Tecnologico', 
                'Programmi di ricerca di Rilevante Interesse Nazionale', 'SMAP']:
        token=idnormalizer.normalize(term)
        terms.append(SimpleVocabulary.createTerm(term, token, term))
     return SimpleVocabulary(terms)

grok.global_utility(StrumentiFinanziamento, name=u"strumenti_finanziamento")


# Interface class; used to define content-type schema.

class ISchedaProgetto(form.Schema):
    
    """
    scheda buona pratica
    """
    dexteritytextindexer.searchable('title')
    title = schema.TextLine(
            title=_(u"Titolo"),
            required=True,
        )

    dexteritytextindexer.searchable('abstract')
    abstract = RichText(
    title=_(u"Abstract"),
    description=_(""),
    required=False,
    )

 #   dexteritytextindexer.searchable('commento')
    commento = RichText(
    title=_(u"Commento"),
    description=_(""),
    required=False,
    )
  
    partner= schema.TextLine(
            title=_(u"Partner"),
            required=False,
        )  

    localizzazione = schema.Choice(
        title=u"Localizzazione",
        vocabulary=u"localizzazioni", 
        required=False, )

    dimensioni_amministrazione = schema.Choice(
    title=_(u"Dimensioni amministrazione"), 
    description=_(""), 
    values=(u"Oltre 1.000.000 abitanti", u"Da 100.000 a 1.000.000 abitanti", u"Da 10.000 a 100.000 abitanti", u"Inferiore a 10.000 abitanti"), 
    required=False, 
    )

    ambito = schema.Choice(
        title=u"Ambito",
        vocabulary=u"ambiti", 
        required=False, )
        

    settore_intervento = schema.List(
        title=u"Settori d'intervento",
        value_type=schema.Choice(vocabulary=u"settori_intervento"), 
        required=False, )

    obiettivo = RelationList(
    title=u"Obiettivi",
    default=[],
    value_type=RelationChoice(title=_(u"Obiettivi"),
         source=ObjPathSourceBinder(path={ "query": "/Plone/vocabolari" }, 
                                                        object_provides= IObiettivi.__identifier__
                                                             )
                  ),
    required=False,
        )	

    datainizio = schema.Date(
            title=_(u"Data inizio lavori"),
            required=False,
        )
        
    temporealizzazione = schema.Int(
            title=_(u"Tempo di realizzazione (mesi)"),
            required=False,
        )

    costo = schema.TextLine(
            title=_(u"Costo"),
            required=False,
        )

    finanziatore = schema.TextLine(
            title=_(u"Finanziatore"),
            required=False,
        )

    strumento_finanziamento = schema.Choice(
        title=u"Strumento di finanziamento",
        vocabulary=u"strumenti_finanziamento", 
        required=False, )


 #   dexteritytextindexer.searchable('note_finanziamenti')
    note_finanziamenti = RichText(
    title=_(u"Note ai finanziamenti"),
    description=_(""),
    required=False,
    )


    form.widget(referente=AutocompleteFieldWidget)
    referente = RelationChoice(
    title=_(u"Referente progetto"),
    source=ObjPathSourceBinder(
                                        object_provides=IAnagraficaContatti.__identifier__
                                        ),
    required=False,
    )
    
    email= schema.TextLine(
            title=_(u"e-mail"),
            required=False,
        )  
   
    url= schema.TextLine(
            title=_(u"URL"),
            required=False,
        )  


    documenti_aggiuntivi_uno = NamedBlobFile(
    title=u'Documenti aggiuntivi', 
    required=False, 
    )

    documenti_aggiuntivi_due = NamedBlobFile(
    title=u'Documenti aggiuntivi', 
    required=False, 
    )

    documenti_aggiuntivi_tre = NamedBlobFile(
    title=u'Documenti aggiuntivi', 
    required=False, 
    )
    
    documenti_aggiuntivi_quattro = NamedBlobFile(
    title=u'Documenti aggiuntivi', 
    required=False, 
    )
    
@grok.adapter(ISchedaProgetto,  name='settore_intervento')
@indexer(ISchedaProgetto)
def settore_intervento_indexer(context):
    return context.settore_intervento

@grok.adapter(ISchedaProgetto,  name='dimensioni_amministrazione')
@indexer(ISchedaProgetto)
def dimensioni_amministrazione_indexer(context):
    return context.dimensioni_amministrazione

@grok.adapter(ISchedaProgetto,  name='strumento_finanziamento')
@indexer(ISchedaProgetto)
def strumento_finanziamento_indexer(context):
    return context.strumento_finanziamento

@grok.adapter(ISchedaProgetto,  name='localizzazione')
@indexer(ISchedaProgetto)
def localizzazione_indexer(context):
    return context.localizzazione

@grok.adapter(ISchedaProgetto,  name='ambito')
@indexer(ISchedaProgetto)
def ambito_indexer(context):
    return context.ambito
    
@indexer(ISchedaProgetto)
def data_inizio_indexer(context):
        anno = ""
        if context.datainizio is not None:
                anno = context.datainizio.strftime('%Y')
        return anno

    



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


#    grok.context(ISchedaProgetto)
#    grok.require('zope2.View')

    # grok.name('view')

    # Add view methods here
#    def prova(self):
#       return "ciao"

#from zope.schema.vocabulary import SimpleVocabulary

#dummy_vocabulary_instance = SimpleVocabulary.fromItems([(1, 'a'), (2, 'c')])
