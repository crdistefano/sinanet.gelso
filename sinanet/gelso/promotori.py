# -*- coding: utf-8 -*-

from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid

from plone.dexterity.content import Container
from plone.directives import dexterity, form

from sinanet.gelso import MessageFactory as _




# Interface class; used to define content-type schema.

class IPromotori(form.Schema):
    """
    Contenitore promotori raggruppati per categoria
    """
    title = schema.TextLine(
    title=_(u"Denominazione"),
    description=_(u"Denominazione del promotore"),
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


""""

View class di prova, il template si trova nella cartella promotori_templates e si 
deve chiamare importa.pt

Nel template poi richiamo la funzione prova

class Importa(grok.View):
    grok.context(IPromotori)
    grok.require('zope2.View')
    def prova(self):
        return "ciao"

"""
"""
class View(grok.View):

# sample view class 

    grok.context(IPromotori)
    grok.require('zope2.View')
    
     
    def importa(self):
        import csv
        from zope.component.hooks import getSite
        from plone.dexterity.utils import createContent
        from Products.CMFPlone.utils import safe_unicode
        from plone.i18n.normalizer import idnormalizer
        from plone.dexterity.utils import addContentToContainer
    
        path = "/home/cristian/Scrivania/anagraficaContatti.csv"
        csvfile = open(path, 'rU')
        reader = csv.reader(csvfile, delimiter='\t')
        stringa=""
        site = getSite()
        catalog = site.portal_catalog

        referente=""
        email=""
        indirizzo=""
        telefono=""
        unita=""
        regione=""
        provincia=""
        comune=""
        folder=None
        for elemento in reader:
            valore = str(elemento[5])
            for i, s in enumerate(valore):
                    if s=="(":
                        valore = valore[0:i]
            results = catalog.searchResults({'Title':valore})
            
            for result in results:
                folder = result.getObject()
                
            referente = str(elemento[0]) + " " + str(elemento[1])
            email = str(elemento[2])
            indirizzo = str(elemento[3])
            telefono = str(elemento[4])
            unita = str(elemento[6])
            titolo = safe_unicode(referente)
            id = idnormalizer.normalize(titolo)
            context = createContent('sinanet.gelso.anagraficacontatti', title=titolo, id=id, \
                                    unita_organizzativa=unita, indirizzo=indirizzo, email=email, telefono=telefono)
            addContentToContainer(folder, context)

"""
"""
class ImportaProgetti(grok.View):
    grok.context(IPromotori)
    grok.require('zope2.View')
   
    def importa(self):
        from zope.component.hooks import getSite
        from plone.dexterity.utils import createContent
        from Products.CMFPlone.utils import safe_unicode
        from plone.i18n.normalizer import idnormalizer
        from plone.dexterity.utils import addContentToContainer
        
        from zope.app.intid import IntIds
        from z3c.relationfield import RelationValue
        import datetime
        
        from plone.app.textfield.value import RichTextValue
        from z3c.relationfield import RelationValue
        
        from zope.component import getUtility
        from zope.intid.interfaces import IIntIds
        
        import csv

        path = "/home/cristian/Scrivania/progetti.csv"
        csvfile = open(path, 'rU')
        reader = csv.reader(csvfile, delimiter='\t')
        
        stringa=""
        site = getSite()
        catalog = site.portal_catalog        
        
        intids = getUtility(IIntIds)
        
        commento=""
        dimensioni_amministrazione=""
        localizzazione=""
        ambito=""
        settore_intervento=[]
        datainizio=""
        temporealizzazione=0
        costo=""
        finanziatore=""
        strumento_finanziamento=""
        partner=""
        obiettivo=[]
        referente=""
        title=""
        folder=None
        description=""
        identificativo_referente=None
        
        #importa i dati in una cartella "temporanei"
        results = catalog.searchResults({'Title':'temporanei'''})
            
        for result in results:
                folder = result.getObject()       
                
        for elemento in reader:
            title = str(elemento[1])
            if elemento[2]:
                    data = str(elemento[2])
                    d = data.split("-")
                    datainizio = datetime.date(int(d[0]), int(d[1]), int(d[2]))           
                    
            description = elemento[3]
            
            if (elemento[4]):
                    temporealizzazione = int(elemento[4])
                    
            if elemento[5]:
                    costo = str(elemento[5])
                    
            if elemento[6] and elemento[6] is not None:
                    note_finanziamenti = RichTextValue(unicode(elemento[6], "utf-8", "ignore"))
                    
            if elemento[7]:
                    commento = RichTextValue(unicode(elemento[7], "utf-8", "ignore"))
                    
            if elemento[8]:
                    partner = str(elemento[8])
                    
            if elemento[9]:
                    url = str(elemento[9])
                    
            if elemento[10] and elemento[10] != "0":
                    localizzazione = str(elemento[10])
                    
            if elemento[11] and elemento[11] != "0":
                    dimensioni_amministrazione = str(elemento[11])
                    
            if elemento[12] and elemento[12] != "0":
                    ambito = str(elemento[12])
                    
            if elemento[13] and elemento[13] != "0":
                    strumento_finanziamento = str(elemento[13])
                    
            if elemento[14]:
                    finanziatore = str(elemento[14])
                    
            if elemento[15]:
                    settori= elemento[15]
                    settori = settori.split(", ")
                    settore_intervento = settori
                    
            if elemento[16]:
                    obiettivi = elemento[16]
                    obiettivi = obiettivi.replace("(", " ")
                    obiettivi = obiettivi.replace(")", " ")
                    lista_obiettivi = obiettivi.split("; ")
                    ids_lista_obiettivi = []
                    
                    for obiettivo in lista_obiettivi:
                                results = catalog.searchResults({'Title':obiettivo})
                                for result in results:
                                            obiettivo_obj = result.getObject()
                                            to_id = intids.getId(obiettivo_obj)
                                            ids_lista_obiettivi.append(to_id)
                                            break
                        
                    ids_lista_obiettivi = list(set(ids_lista_obiettivi))
                    
            if elemento[17] != '0':
                    referente = elemento[17]
                    results = catalog.searchResults({'Title':referente})
                    for result in results:
                            identificativo_referente = result.getObject()
                            
            if elemento[18]:
                    tag=str(elemento[18])
                    tag=tag.split(", ")
                    categorie = tuple(tag)
                    

            results = catalog.searchResults({'Title':referente})
            for result in results:
                    identificativo_referente = result.getObject()

      
     #       titolo = safe_unicode(title)
       #     id = idnormalizer.normalize(titolo)
     
       #     id = elemento[0]
        
            context = createContent('sinanet.gelso.schedaprogetto', title=title, datainizio=datainizio, \
                                temporealizzazione=temporealizzazione, costo=costo, \
                                commento=commento, note_finanziamenti=note_finanziamenti, \
                                localizzazione=localizzazione, dimensioni_amministrazione=dimensioni_amministrazione, \
                                settore_intervento=settore_intervento, ambito=ambito, finanziatore=finanziatore, \
                                strumento_finanziamento=strumento_finanziamento, partner=partner, \
                                description=description, url=url)
                                
                          
            addContentToContainer(folder, context, checkConstraints=False)

            if identificativo_referente is not None:
                    to_id = intids.getId(identificativo_referente)
        
                    context.referente = RelationValue(to_id)

            nuova_lista = []
            for elemento in ids_lista_obiettivi:
                    nuova_lista.append(RelationValue(elemento))
        
            context.obiettivo = nuova_lista

            context.setSubject(tag) 
"""

class ImportaProgetti(grok.View):
    grok.context(IPromotori)
    grok.require('zope2.View')
   
    def importa(self):
        from zope.component.hooks import getSite
        from plone.app.textfield.value import RichTextValue
        from Products.CMFPlone.utils import safe_unicode

        site = getSite()
        catalog = site.portal_catalog        
        
        results = catalog.searchResults({'portal_type':'sinanet.gelso.schedaprogetto'})
        
        for result in results:
                scheda = result.getObject()
                if type(scheda.datainizio) == str:
                        scheda.datainizio = None
    #            if scheda.description is not None:
   #                     scheda.abstract = RichTextValue(safe_unicode(scheda.description))
