# CAPE - Config And Payload Extraction
# Copyright(C) 2018 redsand (redsand@redsand.net)
#
# This program is free software : you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.If not, see <http://www.gnu.org/licenses/>.

from lib.cuckoo.common.abstracts import Signature

THREAD_HIDE_FROM_DEBUGGER = 0x11


class antidebug_ntsetinformationthread(Signature):
    name = "antidebug_ntsetinformationthread"
    description = "NtSetInformationThread: attempt to hide thread from debugger"
    severity = 2
    categories = ["anti-debug"]
    authors = ["redsand"]
    minimum = "1.3"
    evented = True
    ttps = ["T1106"]  # MITRE v6,7,8
    ttps += ["U0119"]  # Unprotect
    mbcs = ["OB0001", "B0001", "B0001.014"]
    mbcs += ["OC0003", "C0038"]  # micro-behaviour

    filter_apinames = set(["NtSetInformationThread"])

    def on_call(self, call, _):
        ThreadInformationClass = self.get_raw_argument(call, "ThreadInformationClass")
        if not ThreadInformationClass:
            return False
        else:
            ThreadInformationClass = int(ThreadInformationClass)
        if ThreadInformationClass == THREAD_HIDE_FROM_DEBUGGER:
            if self.pid: self.mark_call()
            return True
