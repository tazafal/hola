#!/usr/bin/python
#
# Copyright (C) 2006 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


# TODO:
#   add text=none to all inits


"""Contains extensions to ElementWrapper objects used with Google Calendar."""

__author__ = 'api.vli (Vivian Li), api.rboyd (Ryan Boyd)'

try:
  from xml.etree import cElementTree as ElementTree
except ImportError:
  try:
    import cElementTree as ElementTree
  except ImportError:
    from elementtree import ElementTree
import atom
import gdata


# XML namespaces which are often used in Google Calendar entities.
GCAL_NAMESPACE = 'http://schemas.google.com/gCal/2005'
GCAL_TEMPLATE = '{http://schemas.google.com/gCal/2005}%s'
WEB_CONTENT_LINK_REL = '%s/%s' % (GCAL_NAMESPACE, 'webContent')
GACL_NAMESPACE = 'http://schemas.google.com/acl/2007'
GACL_TEMPLATE = '{http://schemas.google.com/acl/2007}%s'



class ValueAttributeContainer(atom.AtomBase):
  """A parent class for all Calendar classes which have a value attribute.

  Children include Color, AccessLevel, Hidden
  """

  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['value'] = 'value'

  def __init__(self, value=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

class Color(ValueAttributeContainer):
  """The Google Calendar color element"""

  _tag = 'color'
  _namespace = GCAL_NAMESPACE
  _children = ValueAttributeContainer._children.copy()
  _attributes = ValueAttributeContainer._attributes.copy()
  


class AccessLevel(ValueAttributeContainer):
  """The Google Calendar accesslevel element"""

  _tag = 'accesslevel'
  _namespace = GCAL_NAMESPACE
  _children = ValueAttributeContainer._children.copy()
  _attributes = ValueAttributeContainer._attributes.copy()
  

class Hidden(ValueAttributeContainer):
  """The Google Calendar hidden element"""

  _tag = 'hidden'
  _namespace = GCAL_NAMESPACE
  _children = ValueAttributeContainer._children.copy()
  _attributes = ValueAttributeContainer._attributes.copy()
  

class Selected(ValueAttributeContainer):
  """The Google Calendar selected element"""

  _tag = 'selected'
  _namespace = GCAL_NAMESPACE
  _children = ValueAttributeContainer._children.copy()
  _attributes = ValueAttributeContainer._attributes.copy()


class Timezone(ValueAttributeContainer):
  """The Google Calendar timezone element"""

  _tag = 'timezone'
  _namespace = GCAL_NAMESPACE
  _children = ValueAttributeContainer._children.copy()
  _attributes = ValueAttributeContainer._attributes.copy()


class Where(atom.AtomBase):
  """The Google Calendar Where element"""

  _tag = 'where'
  _namespace = gdata.GDATA_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['valueString'] = 'value_string'

  def __init__(self, value_string=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.value_string = value_string 
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


class CalendarListEntry(gdata.GDataEntry, gdata.LinkFinder):
  """A Google Calendar meta Entry flavor of an Atom Entry """

  _tag = gdata.GDataEntry._tag
  _namespace = gdata.GDataEntry._namespace
  _children = gdata.GDataEntry._children.copy()
  _attributes = gdata.GDataEntry._attributes.copy()
  _children['{%s}color' % GCAL_NAMESPACE] = ('color', Color)
  _children['{%s}accesslevel' % GCAL_NAMESPACE] = ('access_level', 
                                                   AccessLevel)
  _children['{%s}hidden' % GCAL_NAMESPACE] = ('hidden', Hidden)
  _children['{%s}selected' % GCAL_NAMESPACE] = ('selected', Selected)
  _children['{%s}timezone' % GCAL_NAMESPACE] = ('timezone', Timezone)
  _children['{%s}where' % gdata.GDATA_NAMESPACE] = ('where', Where)
  
  def __init__(self, author=None, category=None, content=None,
      atom_id=None, link=None, published=None, 
      title=None, updated=None, 
      color=None, access_level=None, hidden=None, timezone=None,
      selected=None,
      where=None,
      extension_elements=None, extension_attributes=None, text=None):
    gdata.GDataEntry.__init__(self, author=author, category=category, 
                        content=content, atom_id=atom_id, link=link, 
                        published=published, title=title, 
                        updated=updated, text=None)

    self.color = color
    self.access_level = access_level
    self.hidden = hidden 
    self.selected = selected
    self.timezone = timezone
    self.where = where 


class CalendarListFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Calendar meta feed flavor of an Atom Feed"""

  _tag = gdata.GDataFeed._tag
  _namespace = gdata.GDataFeed._namespace
  _children = gdata.GDataFeed._children.copy()
  _attributes = gdata.GDataFeed._attributes.copy()
  _children['{%s}entry' % atom.ATOM_NAMESPACE] = ('entry', [CalendarListEntry])
  #_attributes = {}


class Scope(atom.AtomBase):
  """The Google ACL scope element"""

  _tag = 'scope'
  _namespace = GACL_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['value'] = 'value'
  _attributes['type'] = 'type'
  
  def __init__(self, extension_elements=None, value=None, scope_type=None,
      extension_attributes=None, text=None):
    self.value = value
    self.type = scope_type
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


class Role(ValueAttributeContainer):
  """The Google Calendar timezone element"""

  _tag = 'role'
  _namespace = GACL_NAMESPACE
  _children = ValueAttributeContainer._children.copy()
  _attributes = ValueAttributeContainer._attributes.copy()


class CalendarAclEntry(gdata.GDataEntry, gdata.LinkFinder):
  """A Google Calendar ACL Entry flavor of an Atom Entry """

  _tag = gdata.GDataEntry._tag
  _namespace = gdata.GDataEntry._namespace
  _children = gdata.GDataEntry._children.copy()
  _attributes = gdata.GDataEntry._attributes.copy()
  _children['{%s}scope' % GACL_NAMESPACE] = ('scope', Scope)
  _children['{%s}role' % GACL_NAMESPACE] = ('role', Role)
  
  def __init__(self, author=None, category=None, content=None,
      atom_id=None, link=None, published=None, 
      title=None, updated=None,
      scope=None, role=None,
      extension_elements=None, extension_attributes=None, text=None):
    gdata.GDataEntry.__init__(self, author=author, category=category, 
                        content=content, atom_id=atom_id, link=link, 
                        published=published, title=title, 
                        updated=updated, text=None)

    self.scope = scope
    self.role = role



class CalendarAclFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Calendar ACL feed flavor of an Atom Feed"""

  _tag = gdata.GDataFeed._tag
  _namespace = gdata.GDataFeed._namespace
  _children = gdata.GDataFeed._children.copy()
  _attributes = gdata.GDataFeed._attributes.copy()
  _children['{%s}entry' % atom.ATOM_NAMESPACE] = ('entry', [CalendarAclEntry])


class CalendarEventCommentEntry(gdata.GDataEntry, gdata.LinkFinder):
  """A Google Calendar event comments entry flavor of an Atom Entry"""

  _tag = gdata.GDataEntry._tag
  _namespace = gdata.GDataEntry._namespace
  _children = gdata.GDataEntry._children.copy()
  _attributes = gdata.GDataEntry._attributes.copy()


class CalendarEventCommentFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Calendar event comments feed flavor of an Atom Feed"""

  _tag = gdata.GDataFeed._tag
  _namespace = gdata.GDataFeed._namespace
  _children = gdata.GDataFeed._children.copy()
  _attributes = gdata.GDataFeed._attributes.copy()
  _children['{%s}entry' % atom.ATOM_NAMESPACE] = ('entry', 
      [CalendarEventCommentEntry])


class ExtendedProperty(atom.AtomBase):
  """The Google Calendar extendedProperty element"""

  _tag = 'extendedProperty'
  _namespace = gdata.GDATA_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['name'] = 'name'
  _attributes['value'] = 'value'

  def __init__(self, name=None, value=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.name = name 
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

    
class Reminder(atom.AtomBase):
  """The Google Calendar reminder element"""
  
  _tag = 'reminder'
  _namespace = gdata.GDATA_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['absoluteTime'] = 'absolute_time'
  _attributes['days'] = 'days'
  _attributes['hours'] = 'hours'
  _attributes['minutes'] = 'minutes'

  def __init__(self, absolute_time=None,
      days=None, hours=None, minutes=None, 
      extension_elements=None,
      extension_attributes=None, text=None):
    self.absolute_time = absolute_time
    if days is not None: 
      self.days = str(days)
    else:
      self.days = None
    if hours is not None:
      self.hours = str(hours)
    else:
      self.hours = None
    if minutes is not None:
      self.minutes = str(minutes)
    else:
      self.minutes = None
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    

class When(atom.AtomBase):
  """The Google Calendar When element"""

  _tag = 'when'
  _namespace = gdata.GDATA_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _children['{%s}reminder' % gdata.GDATA_NAMESPACE] = ('reminder', [Reminder])
  _attributes['startTime'] = 'start_time'
  _attributes['endTime'] = 'end_time'

  def __init__(self, start_time=None, end_time=None, reminder=None, 
      extension_elements=None, extension_attributes=None, text=None):
    self.start_time = start_time 
    self.end_time = end_time 
    self.reminder = reminder or []
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}


class Recurrence(atom.AtomBase):
  """The Google Calendar Recurrence element"""

  _tag = 'recurrence'
  _namespace = gdata.GDATA_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()

  
class UriEnumElement(atom.AtomBase):

  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()

  def __init__(self, tag, enum_map, attrib_name='value', 
      extension_elements=None, extension_attributes=None, text=None):
    self.tag=tag
    self.enum_map=enum_map
    self.attrib_name=attrib_name
    self.value=None
    self.text=text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
     
  def findKey(self, value):
     res=[item[0] for item in self.enum_map.items() if item[1] == value]
     if res is None or len(res) == 0:
       return None
     return res[0]

  def _ConvertElementAttributeToMember(self, attribute, value):
    # Special logic to use the enum_map to set the value of the object's value member.
    if attribute == self.attrib_name and value != '':
      self.value = self.enum_map[value]
      return
    # Find the attribute in this class's list of attributes.
    if self.__class__._attributes.has_key(attribute):
      # Find the member of this class which corresponds to the XML attribute
      # (lookup in current_class._attributes) and set this member to the
      # desired value (using self.__dict__).
      setattr(self, self.__class__._attributes[attribute], value)
    else:
      # The current class doesn't map this attribute, so try to parent class.
      atom.ExtensionContainer._ConvertElementAttributeToMember(self, 
                                                               attribute,
                                                               value)
 
  def _AddMembersToElementTree(self, tree):
    # Convert the members of this class which are XML child nodes.
    # This uses the class's _children dictionary to find the members which
    # should become XML child nodes.
    member_node_names = [values[0] for tag, values in
                                       self.__class__._children.iteritems()]
    for member_name in member_node_names:
      member = getattr(self, member_name)
      if member is None:
        pass
      elif isinstance(member, list):
        for instance in member:
          instance._BecomeChildElement(tree)
      else:
        member._BecomeChildElement(tree)
    # Special logic to set the desired XML attribute.
    key = self.findKey(self.value)
    if key is not None:
      tree.attrib[self.attrib_name]=key
    # Convert the members of this class which are XML attributes.
    for xml_attribute, member_name in self.__class__._attributes.iteritems():
      member = getattr(self, member_name)
      if member is not None:
        tree.attrib[xml_attribute] = member
    # Lastly, call the parent's _AddMembersToElementTree to get any
    # extension elements.
    atom.ExtensionContainer._AddMembersToElementTree(self, tree)
    
    

class AttendeeStatus(UriEnumElement):
  """The Google Calendar attendeeStatus element"""
  
  _tag = 'attendeeStatus'
  _namespace = gdata.GDATA_NAMESPACE
  _children = UriEnumElement._children.copy()
  _attributes = UriEnumElement._attributes.copy()
  
  attendee_enum = { 
      'http://schemas.google.com/g/2005#event.accepted' : 'ACCEPTED',
      'http://schemas.google.com/g/2005#event.declined' : 'DECLINED',
      'http://schemas.google.com/g/2005#event.invited' : 'INVITED',
      'http://schemas.google.com/g/2005#event.tentative' : 'TENTATIVE'}
  
  def __init__(self, extension_elements=None, 
      extension_attributes=None, text=None):
    UriEnumElement.__init__(self, 'attendeeStatus', AttendeeStatus.attendee_enum,
                            extension_elements=extension_elements,
                            extension_attributes=extension_attributes, 
                            text=text)


class AttendeeType(UriEnumElement):
  """The Google Calendar attendeeType element"""
  
  _tag = 'attendeeType'
  _namespace = gdata.GDATA_NAMESPACE
  _children = UriEnumElement._children.copy()
  _attributes = UriEnumElement._attributes.copy()
  
  attendee_type_enum = { 
      'http://schemas.google.com/g/2005#event.optional' : 'OPTIONAL',
      'http://schemas.google.com/g/2005#event.required' : 'REQUIRED' }
  
  def __init__(self, extension_elements=None,
      extension_attributes=None, text=None):
    UriEnumElement.__init__(self, 'attendeeType', 
        AttendeeType.attendee_type_enum,
        extension_elements=extension_elements,
        extension_attributes=extension_attributes,text=text)


class Visibility(UriEnumElement):
  """The Google Calendar Visibility element"""
  
  _tag = 'visibility'
  _namespace = gdata.GDATA_NAMESPACE
  _children = UriEnumElement._children.copy()
  _attributes = UriEnumElement._attributes.copy()
  
  visibility_enum = { 
      'http://schemas.google.com/g/2005#event.confidential' : 'CONFIDENTIAL',
      'http://schemas.google.com/g/2005#event.default' : 'DEFAULT',
      'http://schemas.google.com/g/2005#event.private' : 'PRIVATE',
      'http://schemas.google.com/g/2005#event.public' : 'PUBLIC' }

  def __init__(self, extension_elements=None,
      extension_attributes=None, text=None):
    UriEnumElement.__init__(self, 'visibility', Visibility.visibility_enum,
                            extension_elements=extension_elements,
                            extension_attributes=extension_attributes, 
                            text=text)


class Transparency(UriEnumElement):
  """The Google Calendar Transparency element"""
  
  _tag = 'transparency'
  _namespace = gdata.GDATA_NAMESPACE
  _children = UriEnumElement._children.copy()
  _attributes = UriEnumElement._attributes.copy()
  
  transparency_enum = { 
      'http://schemas.google.com/g/2005#event.opaque' : 'OPAQUE',
      'http://schemas.google.com/g/2005#event.transparent' : 'TRANSPARENT' }
  
  def __init__(self, extension_elements=None,
      extension_attributes=None, text=None):
    UriEnumElement.__init__(self, tag='transparency', 
                            enum_map=Transparency.transparency_enum,
                            extension_elements=extension_elements,
                            extension_attributes=extension_attributes, 
                            text=text)


class Comments(atom.AtomBase):
  """The Google Calendar comments element"""
  
  _tag = 'comments'
  _namespace = gdata.GDATA_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _children['{%s}feedLink' % gdata.GDATA_NAMESPACE] = ('feed_link', 
                                                       gdata.FeedLink)
  _attributes['rel'] = 'rel'

  def __init__(self, rel=None, feed_link=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.rel = rel 
    self.feed_link = feed_link
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}






class EventStatus(UriEnumElement):
  """The Google Calendar eventStatus element"""
  
  _tag = 'eventStatus'
  _namespace = gdata.GDATA_NAMESPACE
  _children = UriEnumElement._children.copy()
  _attributes = UriEnumElement._attributes.copy()
  
  status_enum = { 'http://schemas.google.com/g/2005#event.canceled' : 'CANCELED',
                 'http://schemas.google.com/g/2005#event.confirmed' : 'CONFIRMED',
                 'http://schemas.google.com/g/2005#event.tentative' : 'TENTATIVE'}
  
  def __init__(self, extension_elements=None,
      extension_attributes=None, text=None):
    UriEnumElement.__init__(self, tag='eventStatus', 
        enum_map=EventStatus.status_enum,
        extension_elements=extension_elements,
        extension_attributes=extension_attributes, 
        text=text)
    
class Who(UriEnumElement):
  """The Google Calendar Who element"""

  _tag = 'who'
  _namespace = gdata.GDATA_NAMESPACE
  _children = UriEnumElement._children.copy()
  _attributes = UriEnumElement._attributes.copy()
  _children['{%s}attendeeStatus' % gdata.GDATA_NAMESPACE] = (
      'attendee_status', AttendeeStatus)
  _children['{%s}attendeeType' % gdata.GDATA_NAMESPACE] = ('attendee_type',
                                                           AttendeeType)
  _attributes['valueString'] = 'name'
  _attributes['email'] = 'email'

  relEnum = { 'http://schemas.google.com/g/2005#event.attendee' : 'ATTENDEE',
              'http://schemas.google.com/g/2005#event.organizer' : 'ORGANIZER',
              'http://schemas.google.com/g/2005#event.performer' : 'PERFORMER',
              'http://schemas.google.com/g/2005#event.speaker' : 'SPEAKER',
              'http://schemas.google.com/g/2005#message.bcc' : 'BCC',
              'http://schemas.google.com/g/2005#message.cc' : 'CC',
              'http://schemas.google.com/g/2005#message.from' : 'FROM',
              'http://schemas.google.com/g/2005#message.reply-to' : 'REPLY_TO',
              'http://schemas.google.com/g/2005#message.to' : 'TO' }
  
  def __init__(self, extension_elements=None, 
    extension_attributes=None, text=None):
    UriEnumElement.__init__(self, 'who', Who.relEnum, attrib_name='rel',
                            extension_elements=extension_elements,
                            extension_attributes=extension_attributes, 
                            text=text)
    self.name=None
    self.email=None
    self.attendee_status=None
    self.attendee_type=None
    self.rel=None


class OriginalEvent(atom.AtomBase):
  """The Google Calendar OriginalEvent element"""
  
  _tag = 'originalEvent'
  _namespace = gdata.GDATA_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  # TODO: The when tag used to map to a EntryLink, make sure it should really be a When.
  _children['{%s}when' % gdata.GDATA_NAMESPACE] = ('when', When)
  _attributes['id'] = 'id'
  _attributes['href'] = 'href'

  def __init__(self, id=None, href=None, when=None, 
      extension_elements=None, extension_attributes=None, text=None):
    self.id = id
    self.href = href 
    self.when = when
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}    
  

def GetCalendarEventEntryClass():
  return CalendarEventEntry
  
# This class is not completely defined here, because of a circular reference
# in which CalendarEventEntryLink and CalendarEventEntry refer to one another.
class CalendarEventEntryLink(gdata.EntryLink):
  """An entryLink which contains a calendar event entry
  
  Within an event's recurranceExceptions, an entry link
  points to a calendar event entry. This class exists
  to capture the calendar specific extensions in the entry.
  """

  _tag = 'entryLink'
  _namespace = gdata.GDATA_NAMESPACE
  _children = gdata.EntryLink._children.copy()
  _attributes = gdata.EntryLink._attributes.copy()
  # The CalendarEventEntryLink should like CalendarEventEntry as a child but
  # that class hasn't been defined yet, so we will wait until after defining
  # CalendarEventEntry to list it in _children.

  
class RecurrenceException(atom.AtomBase):
  """The Google Calendar RecurrenceException element"""

  _tag = 'recurrenceException'
  _namespace = gdata.GDATA_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _children['{%s}entryLink' % gdata.GDATA_NAMESPACE] = ('entry_link', 
      CalendarEventEntryLink)
  _children['{%s}originalEvent' % gdata.GDATA_NAMESPACE] = ('original_event',
                                                            OriginalEvent)
  _attributes['specialized'] = 'specialized'
  
  def __init__(self, specialized=None, entry_link=None, 
      original_event=None, extension_elements=None, 
      extension_attributes=None, text=None):
    self.specialized = specialized
    self.entry_link = entry_link
    self.original_event = original_event
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    
 
class SendEventNotifications(atom.AtomBase):
  """The Google Calendar sendEventNotifications element"""
  
  _tag = 'sendEventNotifications'
  _namespace = GCAL_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['value'] = 'value'

  def __init__(self, extension_elements=None,
      value=None, extension_attributes=None, text=None):
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}
    
class QuickAdd(atom.AtomBase):
  """The Google Calendar quickadd element"""
  
  _tag = 'quickadd'
  _namespace = GCAL_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['value'] = 'value'

  def __init__(self, extension_elements=None,
      value=None, extension_attributes=None, text=None):
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  def _TransferToElementTree(self, element_tree):
    if self.value:
      element_tree.attrib['value'] = self.value
    element_tree.tag = GCAL_TEMPLATE % 'quickadd'
    atom.AtomBase._TransferToElementTree(self, element_tree)
    return element_tree

  def _TakeAttributeFromElementTree(self, attribute, element_tree):
    if attribute == 'value':
      self.value = element_tree.attrib[attribute]
      del element_tree.attrib[attribute]
    else:
      atom.AtomBase._TakeAttributeFromElementTree(self, attribute, 
          element_tree)

          
class WebContentGadgetPref(atom.AtomBase):

  _tag = 'webContentGadgetPref'
  _namespace = GCAL_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _attributes['name'] = 'name'
  _attributes['value'] = 'value'

  """The Google Calendar Web Content Gadget Preferences element"""

  def __init__(self, name=None, value=None, extension_elements=None,
      extension_attributes=None, text=None):
    self.name = name
    self.value = value
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}          
          
      
class WebContent(atom.AtomBase):

  _tag = 'webContent'
  _namespace = GCAL_NAMESPACE
  _children = atom.AtomBase._children.copy()
  _attributes = atom.AtomBase._attributes.copy()
  _children['{%s}webContentGadgetPref' % GCAL_NAMESPACE] = ('gadget_pref', 
      [WebContentGadgetPref])
  _attributes['url'] = 'url'
  _attributes['width'] = 'width'
  _attributes['height'] = 'height'

  def __init__(self, url=None, width=None, height=None, text=None,
      gadget_pref=None, extension_elements=None, extension_attributes=None):
    self.url = url
    self.width = width
    self.height = height
    self.text = text
    self.gadget_pref = gadget_pref or []
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}  

      
class WebContentLink(atom.Link):

  _tag = 'link'
  _namespace = atom.ATOM_NAMESPACE
  _children = atom.Link._children.copy()
  _attributes = atom.Link._attributes.copy()
  _children['{%s}webContent' % GCAL_NAMESPACE] = ('web_content', WebContent)
    
  def __init__(self, title=None, href=None, link_type=None, 
        web_content=None):
    atom.Link.__init__(self, rel=WEB_CONTENT_LINK_REL, title=title, href=href, 
        link_type=link_type)
    self.web_content = web_content


class CalendarEventEntry(gdata.GDataEntry):
  """A Google Calendar flavor of an Atom Entry """

  _tag = gdata.GDataEntry._tag
  _namespace = gdata.GDataEntry._namespace
  _children = gdata.GDataEntry._children.copy()
  _attributes = gdata.GDataEntry._attributes.copy()
  # This class also contains WebContentLinks but converting those members
  # is handled in a special version of _ConvertElementTreeToMember.
  _children['{%s}where' % gdata.GDATA_NAMESPACE] = ('where', [Where])
  _children['{%s}when' % gdata.GDATA_NAMESPACE] = ('when', [When])
  _children['{%s}who' % gdata.GDATA_NAMESPACE] = ('who', [Who])
  _children['{%s}extendedProperty' % gdata.GDATA_NAMESPACE] = (
      'extended_property', [ExtendedProperty]) 
  _children['{%s}visibility' % gdata.GDATA_NAMESPACE] = ('visibility', 
                                                         Visibility)
  _children['{%s}transparency' % gdata.GDATA_NAMESPACE] = ('transparency', 
                                                           Transparency)
  _children['{%s}eventStatus' % gdata.GDATA_NAMESPACE] = ('event_status', 
                                                          EventStatus)
  _children['{%s}recurrence' % gdata.GDATA_NAMESPACE] = ('recurrence', 
                                                         Recurrence)
  _children['{%s}recurrenceException' % gdata.GDATA_NAMESPACE] = (
      'recurrence_exception', [RecurrenceException])
  _children['{%s}sendEventNotifications' % GCAL_NAMESPACE] = (
      'send_event_notifications', SendEventNotifications)
  _children['{%s}quickadd' % GCAL_NAMESPACE] = ('quick_add', QuickAdd)
  _children['{%s}comments' % gdata.GDATA_NAMESPACE] = ('comments', Comments)
  _children['{%s}originalEvent' % gdata.GDATA_NAMESPACE] = ('original_event',
                                                            OriginalEvent)
  
  def __init__(self, author=None, category=None, content=None,
      atom_id=None, link=None, published=None, 
      title=None, updated=None, 
      transparency=None, comments=None, event_status=None,
      send_event_notifications=None, visibility=None,
      recurrence=None, recurrence_exception=None,
      where=None, when=None, who=None, quick_add=None,
      extended_property=None, original_event=None,
      extension_elements=None, extension_attributes=None, text=None):

    gdata.GDataEntry.__init__(self, author=author, category=category, 
                        content=content,
                        atom_id=atom_id, link=link, published=published,
                        title=title, updated=updated)
    
    self.transparency = transparency 
    self.comments = comments
    self.event_status = event_status 
    self.send_event_notifications = send_event_notifications
    self.visibility = visibility
    self.recurrence = recurrence 
    self.recurrence_exception = recurrence_exception or []
    self.where = where or []
    self.when = when or []
    self.who = who or []
    self.quick_add = quick_add
    self.extended_property = extended_property or []
    self.original_event = original_event
    self.text = text
    self.extension_elements = extension_elements or []
    self.extension_attributes = extension_attributes or {}

  # We needed to add special logic to _ConvertElementTreeToMember because we
  # want to make links with a rel of WEB_CONTENT_LINK_REL into a 
  # WebContentLink
  def _ConvertElementTreeToMember(self, child_tree):
    # Special logic to handle Web Content links
    if (child_tree.tag == '{%s}link' % atom.ATOM_NAMESPACE and 
        child_tree.attrib['rel'] == WEB_CONTENT_LINK_REL):
      if self.link is None:
        self.link = []
      self.link.append(atom._CreateClassFromElementTree(WebContentLink, 
                                                        child_tree))
      return
    # Find the element's tag in this class's list of child members
    if self.__class__._children.has_key(child_tree.tag):
      member_name = self.__class__._children[child_tree.tag][0]
      member_class = self.__class__._children[child_tree.tag][1]
      # If the class member is supposed to contain a list, make sure the
      # matching member is set to a list, then append the new member
      # instance to the list.
      if isinstance(member_class, list):
        if getattr(self, member_name) is None:
          setattr(self, member_name, [])
        getattr(self, member_name).append(atom._CreateClassFromElementTree(
            member_class[0], child_tree))
      else:
        setattr(self, member_name,
                atom._CreateClassFromElementTree(member_class, child_tree))
    else:
      atom.ExtensionContainer._ConvertElementTreeToMember(self, child_tree)
      

  def GetWebContentLink(self):
    """Finds the first link with rel set to WEB_CONTENT_REL

    Returns:
      A gdata.calendar.WebContentLink or none if none of the links had rel 
      equal to WEB_CONTENT_REL
    """

    for a_link in self.link:
      if a_link.rel == WEB_CONTENT_LINK_REL:
        return a_link
    return None
    

def CalendarEventEntryFromString(xml_string):
  return atom.CreateClassFromXMLString(CalendarEventEntry, xml_string)


def CalendarEventCommentEntryFromString(xml_string):
  return atom.CreateClassFromXMLString(CalendarEventCommentEntry, xml_string)
  

CalendarEventEntryLink._children = {'{%s}entry' % atom.ATOM_NAMESPACE: 
    ('entry', CalendarEventEntry)}
  

def CalendarEventEntryLinkFromString(xml_string):
  return atom.CreateClassFromXMLString(CalendarEventEntryLink, xml_string)


class CalendarEventFeed(gdata.GDataFeed, gdata.LinkFinder):
  """A Google Calendar event feed flavor of an Atom Feed"""

  _tag = gdata.GDataFeed._tag
  _namespace = gdata.GDataFeed._namespace
  _children = gdata.GDataFeed._children.copy()
  _attributes = gdata.GDataFeed._attributes.copy()
  _children['{%s}entry' % atom.ATOM_NAMESPACE] = ('entry', 
                                                  [CalendarEventEntry])

  def __init__(self, author=None, category=None, contributor=None,
      generator=None, icon=None, atom_id=None, link=None, logo=None, 
      rights=None, subtitle=None, title=None, updated=None, entry=None, 
      total_results=None, start_index=None, items_per_page=None,
      extension_elements=None, extension_attributes=None, text=None):
     gdata.GDataFeed.__init__(self, author=author, category=category,
                              contributor=contributor, generator=generator,
                              icon=icon,  atom_id=atom_id, link=link,
                              logo=logo, rights=rights, subtitle=subtitle,
                              title=title, updated=updated, entry=entry,
                              total_results=total_results,
                              start_index=start_index,
                              items_per_page=items_per_page,
                              extension_elements=extension_elements,
                              extension_attributes=extension_attributes,
                              text=text)


def CalendarListEntryFromString(xml_string):
  return atom.CreateClassFromXMLString(CalendarListEntry, xml_string)


def CalendarAclEntryFromString(xml_string):
  return atom.CreateClassFromXMLString(CalendarAclEntry, xml_string)


def CalendarListFeedFromString(xml_string):
  return atom.CreateClassFromXMLString(CalendarListFeed, xml_string)
  
  
def CalendarAclFeedFromString(xml_string):
  return atom.CreateClassFromXMLString(CalendarAclFeed, xml_string)


def CalendarEventFeedFromString(xml_string):
  return atom.CreateClassFromXMLString(CalendarEventFeed, xml_string)

  
def CalendarEventCommentFeedFromString(xml_string):
  return atom.CreateClassFromXMLString(CalendarEventCommentFeed, xml_string)


# Code to create atom feeds from element trees
#_CalendarListFeedFromElementTree = atom._AtomInstanceFromElementTree(
#    CalendarListFeed, 'feed', atom.ATOM_NAMESPACE)
#_CalendarListEntryFromElementTree = atom._AtomInstanceFromElementTree(
#    CalendarListEntry, 'entry', atom.ATOM_NAMESPACE)
#_CalendarAclFeedFromElementTree = atom._AtomInstanceFromElementTree(
#    CalendarAclFeed, 'feed', atom.ATOM_NAMESPACE)
#_CalendarAclEntryFromElementTree = atom._AtomInstanceFromElementTree(
#    CalendarAclEntry, 'entry', atom.ATOM_NAMESPACE)
#_CalendarEventFeedFromElementTree = atom._AtomInstanceFromElementTree(
#    CalendarEventFeed, 'feed', atom.ATOM_NAMESPACE)
#_CalendarEventEntryFromElementTree = atom._AtomInstanceFromElementTree(
#    CalendarEventEntry, 'entry', atom.ATOM_NAMESPACE)
#_CalendarEventCommentFeedFromElementTree = atom._AtomInstanceFromElementTree(
#    CalendarEventCommentFeed, 'feed', atom.ATOM_NAMESPACE)
#_CalendarEventCommentEntryFromElementTree = atom._AtomInstanceFromElementTree(
#    CalendarEventCommentEntry, 'entry', atom.ATOM_NAMESPACE)
#_WhereFromElementTree = atom._AtomInstanceFromElementTree(
#    Where, 'where', gdata.GDATA_NAMESPACE)
#_WhenFromElementTree = atom._AtomInstanceFromElementTree(
#    When, 'when', gdata.GDATA_NAMESPACE)
#_WhoFromElementTree = atom._AtomInstanceFromElementTree(
#    Who, 'who', gdata.GDATA_NAMESPACE)
#_VisibilityFromElementTree= atom._AtomInstanceFromElementTree(
#    Visibility, 'visibility', gdata.GDATA_NAMESPACE)
#_TransparencyFromElementTree = atom._AtomInstanceFromElementTree(
#    Transparency, 'transparency', gdata.GDATA_NAMESPACE)
#_CommentsFromElementTree = atom._AtomInstanceFromElementTree(
#    Comments, 'comments', gdata.GDATA_NAMESPACE)
#_EventStatusFromElementTree = atom._AtomInstanceFromElementTree(
#    EventStatus, 'eventStatus', gdata.GDATA_NAMESPACE)
#_SendEventNotificationsFromElementTree = atom._AtomInstanceFromElementTree(
#    SendEventNotifications, 'sendEventNotifications', GCAL_NAMESPACE)
#_QuickAddFromElementTree = atom._AtomInstanceFromElementTree(
#    QuickAdd, 'quickadd', GCAL_NAMESPACE)
#_AttendeeStatusFromElementTree = atom._AtomInstanceFromElementTree(
#    AttendeeStatus, 'attendeeStatus', gdata.GDATA_NAMESPACE)
#_AttendeeTypeFromElementTree = atom._AtomInstanceFromElementTree(
#    AttendeeType, 'attendeeType', gdata.GDATA_NAMESPACE)
#_ExtendedPropertyFromElementTree = atom._AtomInstanceFromElementTree(
#    ExtendedProperty, 'extendedProperty', gdata.GDATA_NAMESPACE)
#_RecurrenceFromElementTree = atom._AtomInstanceFromElementTree(
#    Recurrence, 'recurrence', gdata.GDATA_NAMESPACE)
#_RecurrenceExceptionFromElementTree = atom._AtomInstanceFromElementTree(
#    RecurrenceException, 'recurrenceException', gdata.GDATA_NAMESPACE)
#_OriginalEventFromElementTree = atom._AtomInstanceFromElementTree(
#    OriginalEvent, 'originalEvent', gdata.GDATA_NAMESPACE)
#_ColorFromElementTree = atom._AtomInstanceFromElementTree(
#    Color, 'color', GCAL_NAMESPACE)
#_HiddenFromElementTree = atom._AtomInstanceFromElementTree(
#    Hidden, 'hidden', GCAL_NAMESPACE)
#_SelectedFromElementTree = atom._AtomInstanceFromElementTree(
#    Selected, 'selected', GCAL_NAMESPACE)
#_TimezoneFromElementTree = atom._AtomInstanceFromElementTree(
#    Timezone, 'timezone', GCAL_NAMESPACE)
#_AccessLevelFromElementTree = atom._AtomInstanceFromElementTree(
#    AccessLevel, 'accesslevel', GCAL_NAMESPACE)
#_ReminderFromElementTree = atom._AtomInstanceFromElementTree(
#    Reminder, 'reminder', gdata.GDATA_NAMESPACE)
#_ScopeFromElementTree = atom._AtomInstanceFromElementTree(
#    Scope, 'scope', GACL_NAMESPACE)
#_RoleFromElementTree = atom._AtomInstanceFromElementTree(
#    Role, 'role', GACL_NAMESPACE)
#_WebContentLinkFromElementTree = atom._AtomInstanceFromElementTree(
#    WebContentLink, 'link', atom.ATOM_NAMESPACE)
#_WebContentFromElementTree = atom._AtomInstanceFromElementTree(
#    WebContent, 'webContent', GCAL_NAMESPACE)
#_WebContentGadgetPrefFromElementTree = atom._AtomInstanceFromElementTree(
#    WebContentGadgetPref, 'webContentGadgetPref', GCAL_NAMESPACE)
