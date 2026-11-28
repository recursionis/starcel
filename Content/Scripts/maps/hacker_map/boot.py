"""
boot.py — the intro, timed like the reference video.

    log       0-6 s   kernel log scrolls on a Screen Cube in front of the
                      camera (panels are built meanwhile, one step per tick;
                      the log keeps scrolling until building is done)
    complete  6-7 s   "Boot Complete"
    line      7-9 s   a glowing line grows out from the centre
    welcome   9-11 s  terminal frame + "Welcome back, <user>", keyboard fades up
    panels    11-15 s SYSTEM, NETWORK, FILESYSTEM flicker in; globe grows
    neofetch  15-20 s `neofetch` is typed into the shell and runs
    idle              shell focused for the user

Esc skips to idle; F5 (BootSequence.replay) runs it again without
rebuilding anything.
"""

import os
import random

from unreal_engine import FVector

from maps.hacker_map import theme, ui, layout
from maps.hacker_map.theme import rot

BOOT_LINES = """Welcome to Starcel!
Starcel Kernel Version 9.0.0: {date}; root:starcel-4.27.2~1/RELEASE_X86_64
vm_page_bootstrap: {free} free pages and {wired} wired pages
kext submap [0xffffff7f8072e000 - 0xffffff8000000000], kernel text [0xffffff8000200000 - 0xffffff800072e000]
zone leak detection enabled
standard timeslicing quantum is 10000 us
mig_table_max_displ = 72
TSC Deadline Timer supported and enabled
StarcelACPICPU: ProcessorId=1 LocalApicId=0 Enabled
StarcelACPICPU: ProcessorId=2 LocalApicId=2 Enabled
StarcelACPICPU: ProcessorId=3 LocalApicId=1 Enabled
StarcelACPICPU: ProcessorId=4 LocalApicId=3 Enabled
StarcelACPICPU: ProcessorId=5 LocalApicId=255 Disabled
StarcelACPICPU: ProcessorId=6 LocalApicId=255 Disabled
calling mpo_policy_init for TMSafetyNet
Security policy loaded: Safety net for Rollback (TMSafetyNet)
calling mpo_policy_init for Sandbox
Security policy loaded: Seatbelt sandbox policy (Sandbox)
calling mpo_policy_init for Quarantine
Security policy loaded: Quarantine policy (Quarantine)
Copyright (c) 1982, 1986, 1989, 1991, 1993, 2015
The Regents of the Starcel Collective. All rights reserved.
IOAPIC: Version 0x20 Vectors 64:87
ACPI: System State [S0 S3 S4 S5] (S3)
PFM64 0xf10000000, 0xf0000000
[ PCI configuration begin ]
StarcelIntelCPUPowerManagement: Turbo Ratios 0046
StarcelIntelCPUPowerManagement: (built 13:08:12 Jun 18 2011) initialization complete
console relocated to 0xf10000000
PCI configuration changed (bridge=16 device=4 cardbus=0)
[ PCI configuration end, bridges 12 devices 16 ]
mbinit: done [64 MB total pool size, (42/21) split]
Pthread support ABORTS when sync kernel primitives misused
com.starcel.StarcelFSCompressionTypeZlib kmod start
com.starcel.StarcelTrololoBootScreen kmod start
com.starcel.StarcelFSCompressionTypeZlib load succeeded
com.starcel.StarcelFSCompressionTypeDataless load succeeded

StarcelIntelCPUPowerManagementClient: ready
BTCOEXIST off
wl0: Broadcom BCM4331 802.11 Wireless Controller
5.100.98.75

FireWire (OHCI) Lucent ID 5901 built-in now active, GUID c82a14fffee4a086; max speed s800.
rooting via boot-uuid from /chosen: F5670083-AC74-33D3-8361-AC1977EE4AA2
Waiting on <dict ID="0"><key>IOProviderClass</key><string ID="1">
IOResources</string><key>IOResourceMatch</key><string ID="2">boot-uuid-media</string></dict>
Got boot device = IOService:/StarcelACPIPlatformExpert/PCI0@0/StarcelACPIPCI/SATA@1F,2/
StarcelUnrealEngine: mounting /Game/Maps/HackerMap
StarcelPython: UnrealEnginePython {py} ready
BSD root: disk0s2, major 14, minor 2
Kernel is LP64
IOThunderboltSwitch::i2cWriteDWord - status = 0xe00002ed
IOThunderboltSwitch::i2cWriteDWord - status = 0x00000000
IOThunderboltSwitch::i2cWriteDWord - status = 0xe00002ed
StarcelUSBMultitouchDriver::checkStatus - received Status Packet, Payload 2: device was reinitialized
[IOBluetoothHCIController::setConfigState] calling registerService
AirPort_Brcm4331: Ethernet address e4:ce:8f:46:18:d2
IO80211Controller::dataLinkLayerAttachComplete(): adding StarcelFINVRAM notification
Created virtif 0xffffff800c32ee00 p2p0
Previous Shutdown Cause: 3
NTFS driver 3.8 [Flags: R/W].
NTFS volume name {host}, version 3.1.
DSMOS has arrived
en1: 802.11d country code set to 'US'.
en1: Supported channels 1 2 3 4 5 6 7 8 9 10 11 36 40 44 48 52 56 60 64 100 104 108 112 116 120 124
MacAuthEvent en1 Auth result for: 00:60:64:1e:e9:e4 MAC AUTH succeeded
wlEvent: en1 en1 Link UP
AirPort: Link Up on en1
virtual bool IOHIDEventSystemUserClient::initWithTask(task*, void*, UInt32):
Client task not privileged to open IOHIDSystem for mapping memory (e00002c1)
StarcelSysmon: worker online
StarcelHackerMap: building panels
"""

# phase name -> duration (s); 'log' may run longer while panels build
PHASES = [('log', 6.0), ('complete', 1.0), ('line', 2.0), ('welcome', 2.0),
          ('panels', 4.0), ('neofetch', 5.0), ('hello', 3.0), ('idle', 0.0)]

HELLO = 'Hi Reddit'      # typed into the shell prompt at the end, like the video


class BootSequence:
    def __init__(self, main):
        self.main = main
        self.phase_i = 0
        self.t = 0.0
        self.total = 0.0
        self.log_lines = self._lines()
        self.shown = 0
        self.screen = None
        self.line_bar = None
        self.done = False
        self._img_acc = 1.0
        self._neofetch_started = False

    # helpers

    @property
    def phase(self):
        return PHASES[self.phase_i][0]

    def _lines(self):
        import datetime
        import platform
        import socket
        import sys
        fmt = dict(date=datetime.datetime.now().strftime('%a %b %d %H:%M:%S %Z %Y'),
                   free=random.randint(800000, 999999), wired=random.randint(40000, 60000),
                   host=socket.gethostname().upper(), py=platform.python_version())
        return [ln.format(**fmt) if '{' in ln else ln
                for ln in BOOT_LINES.strip('\n').split('\n')]

    SCREEN_DIST = 0.45     # boot screen distance, fraction of the wall distance

    def _front(self):
        """Boot screen centre and the width that fills the 90 deg view there."""
        loc, _ = layout.camera_spot()
        dist = layout.WALL_X * self.SCREEN_DIST
        return FVector(loc.x + dist, loc.y, loc.z), 2.0 * dist * 0.98

    # screen

    def _log_image(self, lines, complete=False):
        from PIL import Image, ImageDraw
        W, H = 1280, 720
        img = Image.new('RGBA', (W, H), (0, 0, 0, 255))
        d = ImageDraw.Draw(img)
        font = theme.pil_font(15)
        line_h = 18
        rows = H // line_h - 1
        view = lines[-rows:]
        y = H - line_h * (len(view) + 1)
        for ln in view:
            d.text((6, y), ln, font=font, fill=theme.PIL_GREEN)
            y += line_h
        if complete:
            d.text((6, H - line_h - 2), 'Boot Complete', font=theme.pil_font(16, True),
                   fill=theme.PIL_HOT)
        return img

    def _ensure_screen(self):
        if self.screen is None:
            c, w = self._front()
            self.screen = ui.ScreenCube(self._log_image([]), c, w, w * 9 / 16,
                                        strength=theme.GLOW_LINE * 0.45)
        ui.set_hidden(self.screen.actor, False)

    def _hide_screen(self):
        if self.screen is not None:
            ui.set_hidden(self.screen.actor, True)

    # control

    def start(self):
        self.phase_i, self.t, self.total, self.shown = 0, 0.0, 0.0, 0
        self.done = False
        self._neofetch_started = False
        self.main.hide_all_panels()
        self._ensure_screen()

    def replay(self):
        if self.main.terminal is not None:
            self.main.terminal.clear()
            self.main.terminal.hide_welcome()
        self.start()

    def skip(self):
        """Esc: jump to the end (finishes any remaining panel building)."""
        if self.done:
            return
        self.main.build_all_now()
        self._hide_screen()
        self._destroy_line()
        t = self.main.terminal
        if t is not None:
            t.hide_welcome()
            if t._typing is not None:
                t.finish_typing()
            if not self._neofetch_started:
                t.run('neofetch')
            self._set_prompt(HELLO)
        self.main.show_all_panels()
        self._finish()

    def _set_prompt(self, text):
        t = self.main.terminal
        child = getattr(t.prompt, 'text3d_actor', None) if t and t.prompt else None
        if child is not None:
            ui.set_text(child, text)

    def _finish(self):
        self.done = True
        self.phase_i = len(PHASES) - 1
        if self.main.terminal is not None:
            self.main.terminal.focus_prompt()

    def _advance(self):
        self.phase_i = min(len(PHASES) - 1, self.phase_i + 1)
        self.t = 0.0
        self._enter(self.phase)

    def _enter(self, phase):
        m = self.main
        if phase == 'line':
            self._hide_screen()
            c, self._line_w = self._front()
            self.line_bar = ui.spawn_mesh(ui.CUBE, c, rot(yaw=90),
                                          FVector(0.01, 0.01, self._line_w * 0.0012 / 100.0))
            theme.glow(self.line_bar, theme.GLOW_LINE)
        elif phase == 'welcome':
            self._destroy_line()
            if m.terminal is not None:
                m.terminal.show_welcome(m.data.user if m.data else 'user')
        elif phase == 'panels':
            pass
        elif phase == 'neofetch':
            t = m.terminal
            if t is not None:
                t.hide_welcome()
                self._neofetch_started = True
                t.type_command('neofetch', cps=8.0)
        elif phase == 'hello':
            if m.terminal is not None:
                m.terminal.type_text(HELLO, cps=7.0)
        elif phase == 'idle':
            m.show_all_panels()
            self._finish()

    def _destroy_line(self):
        if self.line_bar is not None:
            ui.destroy(self.line_bar)
            self.line_bar = None

    # per-frame

    def tick(self, dt):
        if self.done:
            return
        self.t += dt
        self.total += dt
        phase, dur = PHASES[self.phase_i]
        m = self.main

        if phase == 'log':
            # the log scrolls while main builds panels
            rate = 14.0 if m.building else 40.0
            self.shown = min(len(self.log_lines), self.shown + max(1, int(rate * dt + 0.5)))
            self._img_acc += dt
            if self._img_acc > 1.0 / 15.0:
                self._img_acc = 0.0
                lines = self.log_lines[:self.shown]
                if m.building and self.shown >= len(self.log_lines):
                    # still building: keep the log alive with progress lines
                    lines = lines + [f'StarcelHackerMap: {m.build_status()}']
                self.screen.update(self._log_image(lines))
            if self.t >= dur and not m.building:
                self.shown = len(self.log_lines)
                self.screen.update(self._log_image(self.log_lines, complete=True))
                self._advance()
            return

        if phase == 'line' and self.line_bar is not None:
            k = min(1.0, self.t / (dur * 0.8))
            w = self._line_w * 0.9 * (k * k * (3 - 2 * k))
            self.line_bar.set_actor_scale(FVector(max(0.01, w / 100.0), 0.01,
                                                  self._line_w * 0.0012 / 100.0))

        if phase == 'welcome':
            k = min(1.0, self.t / dur)
            m.reveal_panel('terminal', min(1.0, k * 2.0))
            m.reveal_panel('keyboard', max(0.0, (k - 0.3) / 0.7))

        if phase == 'panels':
            k = self.t / dur
            for i, key in enumerate(('system', 'network', 'filesystem')):
                m.reveal_panel(key, max(0.0, min(1.0, (k - i * 0.25) / 0.35)))
            m.set_globe_grow(min(1.0, max(0.0, (k - 0.25) / 0.4)))

        if dur and self.t >= dur:
            self._advance()
