coding=utf-8
from __future__ import absolute_import

import octoprint.plugin
import random
import requests
import json


class ThreedupPlugin(octoprint.plugin.StartupPlugin,
                     octoprint.plugin.TemplatePlugin,
                     octoprint.plugin.SettingsPlugin):

    def on_after_startup(self):
        self._logger.info("Hello World! (more: %s)" % self._settings.get(["url"]))

    def get_settings_defaults(self):
        return dict(url="http://localtouchscreen:8081")

    # def get_template_vars(self):
    # return dict(url=self._settings.get(["url"]))

    def get_template_configs(self):
        return [
            dict(type="navbar", custom_bindings=False),
            dict(type="settings", custom_bindings=False)
        ]

    def callback(self, comm, parsed_temps):
        url = self._settings.get(["url"])
        # self._logger.info("The URL is (more: %s)" % url )
        r = requests.get(url)
        # v = r.text.split(" ")
        v = json.loads(r.text)

        # Convert Fahrenheit to Celsius
        val1 = int(((int(v['temp1'])-32)*5) / 9)
        val2 = int(((int(v['temp2'])-32)*5) / 9)
        val3 = int(((int(v['voc'])-32)*5) / 9)
        parsed_temps.update(Temp1=(val1,150))
        parsed_temps.update(Temp2=(val2,150))
        parsed_temps.update(VOC=(val3,150))

        # parsed_temps.update(test=(random.uniform(99,101),100))
        # parsed_temps.update(test2=(random.uniform(199,201),200))

        return parsed_temps

# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Threedup Plugin"

# Set the Python version your plugin is compatible with below. Recommended is Python 3 only for all new plugins.
# OctoPrint 1.4.0 - 1.7.x run under both Python 3 and the end-of-life Python 2.
# OctoPrint 1.8.0 onwards only supports Python 3.
__plugin_pythoncompat__ = ">=3,<4"  # Only Python 3
__plugin_implementation__ = ThreedupPlugin()


__plugin_hooks__ = {

    "octoprint.comm.protocol.temperatures.received": __plugin_implementation__.callback
}
