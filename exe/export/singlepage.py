# ===========================================================================
# eXe 
# Copyright 2004-2005, University of Auckland
# Copyright 2004-2008 eXe Project, http://eXeLearning.org/
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# ===========================================================================
"""
This class transforms an eXe node into a page on a single page website
"""

import logging
import re
from cgi                      import escape
from urllib                   import quote
from exe.webui.blockfactory   import g_blockFactory
from exe.engine.error         import Error
from exe.engine.path          import Path
from exe.export.pages         import Page, uniquifyNames
from exe.webui                import common
from exe                      import globals as G

log = logging.getLogger(__name__)


# ===========================================================================
class SinglePage(Page):
    """
    This class transforms an eXe node into a page on a single page website
    """
        
    def save(self, filename, for_print=0):
        """
        Save page to a file.  
        'outputDir' is the directory where the filenames will be saved
        (a 'path' instance)
        """
        outfile = open(filename, "wb")
        outfile.write(self.render(self.node.package,for_print).encode('utf8'))
        outfile.close()
        
    def render(self, package, for_print=0):
	"""
        Returns an XHTML string rendering this page.
        """
        dT = common.getExportDocType()
        sectionTag = "div"
        headerTag = "div"
        if dT == "HTML5":
            sectionTag = "section"
            headerTag = "header"
        html  = self.renderHeader(package.title, for_print)
        if for_print:
            # include extra onload bit:
            html += u'<body onload="print_page()">'
        else:
            html += u"<body>"
        html += u"<"+sectionTag+" id=\"content\">"
        html += u"<"+headerTag+" id=\"header\">"
        html += "<h1>"+escape(package.title)+"</h1>"
        html += u"</"+headerTag+">"
        html += u"<"+sectionTag+" id=\"main\">"
        html += self.renderNode(package.root, 1)
        html += u"</"+sectionTag+">"
        html += self.renderLicense()
        html += self.renderFooter()
        html += u"</"+sectionTag+">"
        html += u"</body></html>"
        
        # JR: Eliminamos los atributos de las ecuaciones
        aux = re.compile("exe_math_latex=\"[^\"]*\"")
	html = aux.sub("", html)
	aux = re.compile("exe_math_size=\"[^\"]*\"")
	html = aux.sub("", html)
	#JR: Cambio la ruta de los enlaces del glosario y el &
	html = html.replace("../../../../../mod/glossary", "../../../../mod/glossary")
	html = html.replace("&concept", "&amp;concept")
    # Remove "resources/" from data="resources/ and the url param
	html = html.replace("video/quicktime\" data=\"resources/", "video/quicktime\" data=\"")
	html = html.replace("application/x-mplayer2\" data=\"resources/", "application/x-mplayer2\" data=\"")
	html = html.replace("audio/x-pn-realaudio-plugin\" data=\"resources/", "audio/x-pn-realaudio-plugin\" data=\"")
	html = html.replace("<param name=\"url\" value=\"resources/", "<param name=\"url\" value=\"")
	
	return html


    def renderHeader(self, name, for_print=0):
        """
        Returns an XHTML string for the header of this page.
        """
        def hasGalleryIdevice(node):
            hasGallery = common.hasGalleryIdevice(node)
            if not hasGallery:
                for child in node.children:
                    if hasGalleryIdevice(child):
                        return True
            return hasGallery
        
        hasGallery = hasGalleryIdevice(self.node)
        def hasWikipediaIdevice(node):
            hasWikipedia = common.hasWikipediaIdevice(node)
            if not hasWikipedia:
                for child in node.children:
                    if hasWikipediaIdevice(child):
                        return True
            return hasWikipedia
        
        hasWikipedia = hasWikipediaIdevice(self.node)
        lenguaje = G.application.config.locale
        dT = common.getExportDocType()
        if dT == "HTML5":
            html = '<!doctype html>'
            html += '<html lang="'+lenguaje+'">'
        else:
            html  = u"<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
            html += u'<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">'
            html += u"<html lang=\"" + lenguaje + "\" xml:lang=\"" + lenguaje + "\" xmlns=\"http://www.w3.org/1999/xhtml\">"
        html += u"<head>"
        html += u"<link rel=\"stylesheet\" type=\"text/css\" href=\"base.css\" />"
        if hasWikipedia:
            html += u"<link rel=\"stylesheet\" type=\"text/css\" href=\"exe_wikipedia.css\" />"
        if hasGallery:
            html += u"<link rel=\"stylesheet\" type=\"text/css\" href=\"exe_lightbox.css\" />"
        html += u"<link rel=\"stylesheet\" type=\"text/css\" href=\"content.css\" />"
        html += u"<title>"
        html += name
        html += "</title>"
        html += u"<link rel=\"shortcut icon\" href=\"favicon.ico\" type=\"image/x-icon\" />"
        html += u"<meta http-equiv=\"Content-Type\" content=\"text/html; "
        html += u" charset=utf-8\" />";
        html += '<meta name="generator" content="eXeLearning - exelearning.net" />'
        if dT == "HTML5":
            html += u'<!--[if lt IE 9]><script type="text/javascript" src="exe_html5.js"></script><![endif]-->'
        if hasGallery:
            html += u'<script type="text/javascript" src="exe_lightbox.js"></script>'
        html += u'<script type="text/javascript" src="common.js"></script>'
        if common.hasMagnifier(self.node):
            html += u'<script type="text/javascript" src="mojomagnify.js"></script>'
        if for_print:
            # include extra print-script for onload bit 
            html += u'<script type="text/javascript">'
            html += u'function print_page() {'
            html += u'     window.print();'
            html += u'     window.close();'
            html += u'}'
            html += u'</script>'
        html += u"</head>"
        return html
    
    #JR: modifico esta funcion para que ponga hX en cada nodo
    def renderNode(self, node, nivel):
        """
        Returns an XHTML string for this node and recurse for the children
        """
        dT = common.getExportDocType()
        sectionTag = "div"
        headerTag = "div"
        articleTag = "div"
        if dT == "HTML5":
            sectionTag = "section"
            headerTag = "header"
            articleTag = "article"
            nivel = 1
        
        html = ""
        html += '<'+articleTag+' class="node">'
        html += '<'+headerTag+' class=\"nodeDecoration\">'
        html += '<h' + str(nivel) + ' class=\"nodeTitle\">'
        html += escape(node.titleLong)
        html += '</h' + str(nivel) + '></'+headerTag+'>'
        
        style = self.node.package.style

        for idevice in node.idevices:
            if idevice.klass != 'NotaIdevice':
                e=" em_iDevice"
                if unicode(idevice.emphasis)=='0':
                    e=""            
                html += u'<'+sectionTag+' class="iDevice_wrapper %s%s" id="id%s">' % (idevice.klass, e, (idevice.id+"-"+node.id))
                block = g_blockFactory.createBlock(None, idevice)
                if not block:
                    log.critical("Unable to render iDevice.")
                    raise Error("Unable to render iDevice.")
                if hasattr(idevice, "isQuiz"):
                    html += block.renderJavascriptForWeb()
                html += self.processInternalLinks(block.renderView(style))
                html = html.replace('href="#auto_top"', 'href="#"')
                html += u'</'+sectionTag+'>' # iDevice div

        html += '</'+articleTag+'>' # node div

        for child in node.children:
            html += self.renderNode(child, nivel+1)

        return html



    def processInternalLinks(self, html):
        """
        take care of any internal links which are in the form of:
           href="exe-node:Home:Topic:etc#Anchor"
        For this SinglePage Export, go ahead and keep the #Anchor portion,
        but remove the 'exe-node:Home:Topic:etc', since it is all 
        exported into the same file.
        """
        return common.removeInternalLinkNodes(html)
        
        

