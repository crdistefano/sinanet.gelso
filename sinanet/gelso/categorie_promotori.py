from five import grok

from z3c.form import group, field
from zope import schema
from zope.interface import invariant, Invalid

from plone.dexterity.content import Container
from plone.directives import dexterity, form

from sinanet.gelso import MessageFactory as _
from plone.indexer import indexer

# Interface class; used to define content-type schema.

class ICategoriaPromotori(form.Schema):
    """
    Contenitore promotori raggruppati per categoria
    """



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
class View(grok.View):
# sample view class 

    grok.context(ICategoriaPromotori)
    grok.require('zope2.View')
    
       
    def prova(self):
        import csv
        from zope.component.hooks import getSite
        from plone.dexterity.utils import createContent
        from Products.CMFPlone.utils import safe_unicode
        from plone.i18n.normalizer import idnormalizer
        from plone.dexterity.utils import addContentToContainer
        
        path = "/home/cristian/Plone/zinstance/src/sinanet.gelso/sinanet/gelso/entiPromotori.csv"
        csvfile = open(path, 'rU')
        reader = csv.reader(csvfile, delimiter='\t')
        stringa=""
        for elemento in reader:
            site = getSite()
            catalog = site.portal_catalog
            valore = str(elemento[0])
            results = catalog.searchResults({'identificativo_promotore':valore})
            for result in results:
                folder = result.getObject()
            
            titolo = safe_unicode(elemento[1])
            id = idnormalizer.normalize(titolo)
            
            context = createContent('sinanet.gelso.promotori', title=titolo, id=id)
            #folder[id] = context
            
            addContentToContainer(folder, context)
                
                
                
                
                
                
                
 """               
                
                
                
                
                
                
                
                
 #       folder = site["banca-dati"]["associazione"]
       
#from zope.schema.vocabulary import SimpleVocabulary

#dummy_vocabulary_instance = SimpleVocabulary.fromItems([(1, 'a'), (2, 'c')])
