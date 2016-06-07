# Copyright (C) 2014 The Genome Institute, Washington University Medical School
#
# This file is part of lsf-python.
#
# lsf-python is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# lsf-python is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with lsf-python.  If not, see <http://www.gnu.org/licenses/>.

from .exceptions import InvalidOption
from pythonlsf import lsf as api
import logging


__all__ = ['get_options', 'set_options']


LOG = logging.getLogger(__name__)


class Option(object):
    def __init__(self, name, cast_with=str, flag=None, flag_group='options'):
        self.name = str(name)
        self.cast_with = cast_with

        if flag is not None:
            self.flag = int(flag)
        else:
            self.flag = None
        self.flag_group = flag_group

    def set_value(self, request, value):
        cast_value = self.cast_with(value)
        setattr(request, self.name, cast_value)

        if self.flag is not None:
            options = getattr(request, self.flag_group)
            setattr(request, self.flag_group, options | self.flag)

    def get_value(self, request):
        if (not self.flag) or (getattr(request, self.flag_group) & self.flag):
            return getattr(request, self.name)


_OPTIONS = {o.name: o for o in
    [
        Option('beginTime', cast_with=int),
        Option('errFile', flag=api.SUB_ERR_FILE),
        Option('jobGroup', flag=api.SUB2_JOB_GROUP, flag_group='options2'),
        Option('inFile', flag=api.SUB_IN_FILE),
        Option('jobName', flag=api.SUB_JOB_NAME),
        Option('mailUser', flag=api.SUB_MAIL_USER),
        Option('maxNumProcessors', cast_with=int),
        Option('numProcessors', cast_with=int),
        Option('outFile', flag=api.SUB_OUT_FILE),
        Option('preExecCmd', flag=api.SUB_PRE_EXEC),
        Option('postExecCmd', flag=api.SUB3_POST_EXEC, flag_group='options3'),
        Option('projectName', flag=api.SUB_PROJECT_NAME),
        Option('queue', flag=api.SUB_QUEUE),
        Option('resReq', flag=api.SUB_RES_REQ),
        Option('termTime', cast_with=int),
    ]
}


def get_options(submit_struct):
    result = {}
    for name, option in _OPTIONS.iteritems():
        value = option.get_value(submit_struct)
        if value is not None:
            result[name] = value
    return result


def set_options(request, options):
    if not options:
        return

    for name, value in options.iteritems():
        option = _OPTIONS.get(name)
        if not option:
            raise InvalidOption(name)

        option.set_value(request, value)
