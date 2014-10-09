# Copyright 2014 MongoDB, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import logging
import sys

logger = logging.getLogger('giza.content.steps.models')

from giza.core.inheritance import InheritableContentBase
from giza.config.base import ConfigurationBase
from giza.content.helper import get_all_languages, level_characters

if sys.version_info >= (3, 0):
    basestring = str

class HeadingMixin(object):
    @property
    def title(self):
        return self.heading

    @title.setter
    def title(self, value):
        self.heading = value

    @property
    def heading(self):
        if self.optional is True:
            return "Optional: " + self.state['heading']
        else:
            return self.state['heading']

    @heading.setter
    def heading(self, value):
        if isinstance(value, dict):
            self.state['heading'] = value['text']
            if 'character' in value and value['character'] in level_characters:
                self.state['level'] = level_characters[value['character']]
            else:
                self.state['level'] = 3
        else:
            self.state['heading'] = value
            self.state['level'] = 3

    @property
    def level(self):
        if 'level' in self.state:
            return self.state['level']
        else:
            return 3

    @level.setter
    def level(self, value):
        if isinstance(value, basetring):
            if value in level_characters:
                self.state['level'] = level_characters[value]
            else:
                logger.error('{0} is not a valid heading level'.format(value))
        elif isintance(value, (int, float, complex)):
            self.state['level'] = int(value)
        else:
            logger.error('{0} is not a valid heading level'.format(value))

    @property
    def optional(self):
        if 'optional' in self.state:
            return True
        else:
            return False

    @optional.setter
    def optional(self, value):
        if value is True:
            self.state['optional'] = True
        else:
            self.state['optional'] = False

class StepData(HeadingMixin, InheritableContentBase):
    _defalut_level = 3

    @property
    def number(self):
        if 'number' in self.state:
            return self.state['number']
        else:
            return None

    @number.setter
    def number(self, value):
        if isinstance(value, (int, float, complex)):
            self.state['number'] = int(value)
        else:
            raise TypeError

    @property
    def stepnum(self):
        return self.number

    @stepnum.setter
    def stepnum(self, value):
        self.number = value

    @property
    def action(self):
        return self.state['action']

    @action.setter
    def action(self, value):
        if isinstance(value, ActionContent):
            self.state['action'] = [ value ]
        elif isinstance(value, dict):
            self.state['action'] = [ ActionContent(value) ]
        elif isinstance(value, list):
            actions = []
            for item in value:
                if isinstance(item, ActionContent):
                    actions.append(item)
                else:
                    actions.append(ActionContent(item))

class ActionContent(HeadingMixin, ConfigurationBase):
    _option_registry = [ 'pre', 'post', 'content']

    @property
    def code(self):
        return self.state['code']

    @code.setter
    def code(self, value):
        if isinstance(value, list):
            self.state['code'] = value
        else:
            self.state['code'] = value.split('\n')

    @property
    def language(self):
        return self.state['language']

    @language.setter
    def language(self, value):
        if value in get_all_languages():
            self.state['language'] = value
        else:
            m = '{0} is not a supported language'.format(value)
            logger.error(m)
            TypeError(m)