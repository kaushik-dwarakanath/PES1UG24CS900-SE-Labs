"""Capture an actual desktop screenshot using the user-approved XDG portal."""
import shutil
import sys
from pathlib import Path
from urllib.parse import unquote, urlparse

import gi
gi.require_version("Gio", "2.0")
from gi.repository import Gio, GLib

destination = Path(sys.argv[1]).resolve()
bus = Gio.bus_get_sync(Gio.BusType.SESSION, None)
loop = GLib.MainLoop()


def response(connection, sender, path, interface, signal, parameters):
    status, results = parameters.unpack()
    if status == 0:
        source = Path(unquote(urlparse(results["uri"]).path))
        shutil.copyfile(source, destination)
        print(f"Actual screenshot saved: {destination}", flush=True)
    else:
        print(f"Screenshot cancelled or failed (portal status {status})", flush=True)
    loop.quit()


subscription = bus.signal_subscribe(
    "org.freedesktop.portal.Desktop", "org.freedesktop.portal.Request",
    "Response", None, None, Gio.DBusSignalFlags.NONE, response,
)
bus.call_sync(
    "org.freedesktop.portal.Desktop", "/org/freedesktop/portal/desktop",
    "org.freedesktop.portal.Screenshot", "Screenshot",
    GLib.Variant("(sa{sv})", ("", {"interactive": GLib.Variant("b", False)})),
    None, Gio.DBusCallFlags.NONE, -1, None,
)
print("Use the desktop screenshot dialog to share the screenshot.", flush=True)
loop.run()
if not destination.exists():
    sys.exit(1)
