# SPDX-License-Identifier: LGPL-3.0-or-later
# Copyright (C) 2020 Daniel Thompson

"""Unix Epoch Time clock
~~~~~~~~~~~~~~~~

Shows a time with only the unix epoch time.

.. figure:: res/UnixClock.png
    :width: 179
"""

import wasp

import fonts.aram as aram

CYBER_GREEN = 0x3640

class UnixClockApp():
    """Simple Unix Epoch Time Clock"""
    NAME = 'Unix Clock'

    def foreground(self):
        """Activate the application.

        Configure the status bar, redraw the display and request a periodic
        tick callback every second.
        """
        wasp.system.bar.clock = False
        self._draw(True)
        wasp.system.request_tick(1000)

    def sleep(self):
        """Prepare to enter the low power mode.

        :returns: True, which tells the system manager not to automatically
                  switch to the default application before sleeping.
        """
        return True

    def wake(self):
        """Return from low power mode.

        Time will have changes whilst we have been asleep so we must
        udpate the display (but there is no need for a full redraw because
        the display RAM is preserved during a sleep.
        """
        self._draw()

    def tick(self, ticks):
        """Periodic callback to update the display."""
        self._draw()

    def preview(self):
        """Provide a preview for the watch face selection."""
        wasp.system.bar.clock = False
        self._draw(True)

    def _draw(self, redraw=False):
        """Draw or lazily update the display.

        The updates are as lazy by default and avoid spending time redrawing
        if the time on display has not changed. However if redraw is set to
        True then a full redraw is be performed.
        """
        draw = wasp.watch.drawable
        hi =  wasp.system.theme('bright')
        lo =  wasp.system.theme('mid')
        mid = draw.lighten(lo, 1)

        now = int(wasp.watch.rtc.time())
        if redraw:
            # Clear the display and draw that static parts of the watch face
            draw.fill()
            draw.blit(aram.aram, 56, 28, fg=mid)
            draw.string("ARAM", 0, 168, width=240)

            # Redraw the status bar
            wasp.system.bar.draw()
        else:
            # Update only if the epoch time has changed
            if not wasp.system.bar.update() or self._epoch_time == now:
                # Skip the update
                return

        # Record the minute that is currently being displayed
        self._epoch_time = now

        # Draw the changeable parts of the watch face
        draw.set_color(CYBER_GREEN)
        draw.string(str(now), 0, 200, width=240)

        
