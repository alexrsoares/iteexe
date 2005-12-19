# ===========================================================================
# eXe 
# Copyright 2004-2005, University of Auckland
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
A Forum Idevice is one built up from forum imformation ans discussion.
"""
import copy
import logging
from exe.engine.idevice import Idevice
from exe.engine.persist import Persistable

log = logging.getLogger(__name__)

# ===========================================================================
class ForumIdevice(Idevice):
    """
    A Forum Idevice is one built up from forum imformation ans discussion.
    """
    
    persistenceVersion = 2

    def __init__(self):
        Idevice.__init__(self, x_(u"Discussion Activity"), 
                         x_(u"University of Auckland"), 
                         "", "", u"discussion")
        self.forum               = Forum()
        self.discussion          = Discussion()
        self.isNewForum          = False
        self.noForum             = True
        self.isNewTopic          = False
        self.message             = ""
        self.refCount            = 1
        self.forumsCache         = None
        self.isAdded             = False
        self.emphasis            = Idevice.SomeEmphasis

    
    def clone(self):
        """
        Clone an iDevice and share one forums cache
        """
        newIdevice             = Idevice.clone(self)
        newIdevice.forumsCache = self.forumsCache
        return newIdevice
    
    def delete(self):
        """
        delete an iDevice from it's parentNode and forums cache
        """
        self.forumsCache.deleteForum(self.forum)
        Idevice.delete(self)
        
    
   
    def upgradeToVersion1(self):
        """
        Upgrades exe to v0.10
        """
        self._upgradeIdeviceToVersion1()
    

    def upgradeToVersion2(self):
        """
        Upgrades to v0.12
        """
        self._upgradeIdeviceToVersion2()


# ===========================================================================
class Forum(Persistable):
            
    def __init__(self):
        
        """
        Initialize 
        """
            
        self.forumName           = ""
        self.lms                 = ""
        self.introduction        = ""
        self.nameInstruc         = _(u"Type a forum name here")
        self.lms                 = Lms()
        self.lms.idevice         = self
        self.subjectInstruc      = ""
        self.messageInstruc      = ""
        self.discussions         = []
        self.lmsInstruc          = "Choose a LMS"
        
        self.refCount            = 1
        
#============================================================================
class Discussion(Persistable):
    def __init__(self):
                 
        """
        Initialize 
        """
        self.name = _(u"Discussion topic/Thread")
        self.isNone = True
        self.topic = ""
        self.intro = ""
        self.instruc = _(u"Type a discussion topic here.")
        self.isAdded = False
        self.refCount = 1
#============================================================================     
class Lms(Persistable):
    def __init__(self):
        """
        Initialize 
        """
        self.name = _("Learning Management System")
        self.lms = ""        
        self.otherUrl = ""
        self.otherLabel = "Link to forum"
        self.type                = "general"
        self.studentpost         = "2"
        self.subscription        = "0"
        self.groupmode           = "0"
        self.visible             = "1"
        self.typeInstruc         = ""
        self.introInstruc        = ""
        self.postInstruc         = ""
        self.subscInstruc        = ""
        self.groupInstruc        = ""
        self.visibleInstruc      = ""
