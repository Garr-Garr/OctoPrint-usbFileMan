# coding=utf-8
from __future__ import absolute_import

### (Don't forget to remove me)
# This is a basic skeleton for your plugin's __init__.py. You probably want to adjust the class name of your plugin
# as well as the plugin mixins it's subclassing from. This is really just a basic skeleton to get you started,
# defining your plugin as a template plugin, settings and asset plugin. Feel free to add or remove mixins
# as necessary.
#
# Take a look at the documentation on what other plugin mixins are available.

import octoprint.plugin
import os
import sys
import shutil
import hashlib
import flask
import datetime
import time
from octoprint.events import Events
from octoprint.util.commandline import CommandlineCaller, CommandlineError


class UsbfilemanPlugin(octoprint.plugin.SettingsPlugin,
					   octoprint.plugin.AssetPlugin,
					   octoprint.plugin.TemplatePlugin,
					   octoprint.plugin.SimpleApiPlugin,
					   octoprint.plugin.EventHandlerPlugin,
					   octoprint.plugin.StartupPlugin):

	##~~ SettingsPlugin mixin

	def on_after_startup(self):
		try:
			os.makedirs(self._settings.get(["copyFolder"]))
		except Exception as e:
			if not os.path.isdir(self._settings.get(["copyFolder"])):
				self._logger.info("Exception while trying to create/check for the copyFolder target: "+str(e))

		# for file in os.listdir(self._basefolder):
		# 	self._logger.info(file)
		# for file in os.listdir(os.path.join(self._basefolder,"installation")):
		# 	self._logger.info(file)
		self._logger.info(os.path.join(self._basefolder,"installation"))

	def on_api_get(self, request):
		self._logger.info("usbfileman on_api_get triggered.  Request: "+str(request))
		resultMessage = ""
		newFiles = False
		dest = self._settings.get(["copyFolder"])

		for folderToCheck in self._settings.get(["watchFolders"]):
			src = folderToCheck
			if not os.path.exists(folderToCheck):
				resultMessage += (" --- USB mount path does not exist: "+folderToCheck)
				continue
			try:
				usbFiles = os.listdir(src)
				# self._logger.info(str(usbFiles))
			except Exception as e:
				self._logger.info("Could not list files in watchFolder; exception: "+str(e))
				resultMessage += (" --- Could not list files in watchFolder; exception: "+str(e))
				continue
				# return flask.jsonify(result="Could not list files in watchFolder; exception: "+str(e))

			try:
				for file_name in usbFiles:
					# self._logger.info(str(file_name))
					file_root, file_extension = os.path.splitext(file_name)
					if (str(file_root).startswith("COPIED")):
						self._logger.info("File already copied according to name: "+str(file_name))
						continue
					if (str(file_root).startswith("._")):
						self._logger.info("File seems to be a Mac system file; skipping.  Filename : "+str(file_name))
						continue
					if (file_extension in self._settings.get(["copyFileTypes"])):
						full_src_name = os.path.join(src, file_name)
						full_dest_name = os.path.join(dest, file_name)
						if not (os.path.isfile(full_dest_name)):
							shutil.copy(full_src_name, dest)
							self._logger.info("Copied "+file_name+" to uploads/USB folder.")
							resultMessage += (" --- Copied "+file_name+" to uploads/USB folder.")
							newFiles = True
							if (self._settings.get(["fileAction"]) == "rename"):
								copiedName = os.path.join(src, ("COPIED" + file_name))
								os.rename(full_src_name, copiedName)
								resultMessage += (" --- Renamed original file in watchFolder to: "+copiedName)
						else:
							if ((hashlib.md5(open(full_src_name).read()).hexdigest()) != (hashlib.md5(open(full_dest_name).read()).hexdigest())):
								# newDestName = dest + '/' + os.path.splitextfile_name + '-' + str(datetime.datetime.now().strftime('%y-%m-%d_%H-%M'))
								newDestName = os.path.join(dest, (file_root + "-" + str(datetime.datetime.now().strftime('%y-%m-%d_%H-%M')) + file_extension) )
								shutil.copyfile(full_src_name, newDestName)
								self._logger.info("Copied a new version of "+file_name+" to uploads/USB folder as " + newDestName)
								resultMessage += (" --- Copied a new version of "+file_name+" to uploads/USB folder as " + newDestName)
								newFiles = True
								if (self._settings.get(["fileAction"]) == "rename"):
									copiedName = os.path.join(src, ("COPIED" + file_name))
									os.rename(full_src_name, copiedName)
									resultMessage += (" --- Renamed original file in watchFolder to: "+copiedName)
			except Exception as e:
				self._logger.info("Could not copy files to uploads/USB folder; exception: "+str(e))
				resultMessage += (" --- Could not copy files to uploads/USB folder; exception: "+str(e))
				continue
				# return flask.jsonify(result="Could not copy files to uploads/USB folder; exception: "+str(e)+" .  Results before exception: "+resultMessage)

		if (resultMessage == ""):
			resultMessage = "Nothing to do."
		if (newFiles):
			self._event_bus.fire(Events.UPDATED_FILES, dict(type="printables"))
		return flask.jsonify(result="Finished without error.  Results: "+resultMessage)


	def get_settings_defaults(self):
		return dict(watchFolders = ["/media/usb1/toprint", "/media/usb2/toprint", "/media/usb3/toprint", "/media/usb4/toprint"],
			copyFolder = "/home/pi/.octoprint/uploads/USB",
			fileAction = "rename",
			copyFileTypes = [".gcode", ".gco", ".g", ".stl"],
			userFeedback = "log"
		)

	##~~ AssetPlugin mixin

	def get_assets(self):
		# Define your plugin's asset files to automatically include in the
		# core UI here.
		return dict(
			js=["js/usbfileman.js"],
			css=["css/usbfileman.css"],
			less=["less/usbfileman.less"]
		)

	##~~ Softwareupdate hook

	def get_update_information(self):
		# Define the configuration for your plugin to use with the Software Update
		# Plugin here. See https://github.com/foosel/OctoPrint/wiki/Plugin:-Software-Update
		# for details.
		return dict(
			usbfileman=dict(
				displayName="Usbfileman Plugin",
				displayVersion=self._plugin_version,

				# version check: github repository
				type="github_release",
				user="MakerGear",
				repo="OctoPrint-usbFileMan",
				current=self._plugin_version,

				# update method: pip
				pip="https://github.com/MakerGear/OctoPrint-usbFileMan/archive/{target_version}.zip"
			)
		)

	def get_api_commands(self):
		# self._logger.info("USBFileMan get_api_commands triggered.")
		#self._logger.info("M114 sent to printer.")
		#self._printer.commands("M114");
		#self.position_state = "stale"
		return dict(adminAction=["action"])

	def on_api_command(self, command, data):
		self._logger.info("USBFileMan on_api_command triggered.  Command: "+str(command)+" .  Data: "+str(data))
		if command == 'adminAction':
			self._logger.info(data)
			self.adminAction(data)
		# elif command == 'writeNetconnectdPassword':
		# 	#self.writeNetconnectdPassword(data)
		# 	self._execute("/home/pi/.octoprint/scripts/changeNetconnectdPassword.sh "+data['password'])
		# 	self._logger.info("Netconnectd password changed to "+data['password']+" !")

	def adminAction(self, action, payload={}):
		self._logger.info("adminAction called: "+ str(action))
		caller = CommandlineCaller()
		caller.on_log_call = self.log_call
		caller.on_log_stdout = self.log_stdout
		caller.on_log_stderr = self.log_stderr
		if action["action"] == 'onlineInstall':
			try:
				# caller.checked_call(["some", "command", "with", "parameters"])
				# caller.checked_call(["sudo apt-get install pmount"])
				caller.checked_call(["sudo", "cp", (os.path.join(self._basefolder,"installation","usbstick.rules")), "/etc/udev/rules.d/"])
				caller.checked_call(["sudo", "cp", (os.path.join(self._basefolder,"installation","usbstick-handler@.service")), "/lib/systemd/system/"])
				caller.checked_call(["sudo", "cp", (os.path.join(self._basefolder,"installation","cpmount")), "/usr/local/bin/cpmount"])
				caller.checked_call(["sudo", "chmod", "u+x", "/usr/local/bin/cpmount"])
			except CommandlineError as err:
				self._logger.info(u"Command returned {}".format(err.returncode))
			except Exception as e:
				self._logger.info(u"Command failed with some other error {}.".format(str(e)))
			else:
				self._logger.info(u"Command finished successfully")



		elif action["action"] == 'offlineInstall':
			try:
				# caller.checked_call(["some", "command", "with", "parameters"])
				caller.checked_call(["sudo", "dpkg", "-i", (os.path.join(self._basefolder,"installation/pmount_0.9.23-3_armhf.deb"))])
				caller.checked_call(["sudo", "cp", (os.path.join(self._basefolder,"installation","usbstick.rules")), "/etc/udev/rules.d/"])
				caller.checked_call(["sudo", "cp", (os.path.join(self._basefolder,"installation","usbstick-handler@.service")), "/lib/systemd/system/"])
				caller.checked_call(["sudo", "cp", (os.path.join(self._basefolder,"installation","cpmount")), "/usr/local/bin/cpmount"])
				caller.checked_call(["sudo", "chmod", "u+x", "/usr/local/bin/cpmount"])
			except CommandlineError as err:
				self._logger.info(u"Command returned {}".format(err.returncode))
			else:
				self._logger.info(u"Command finished successfully")



	def log(self, prefix, msgType="stdout", *lines):
		for line in lines:
			self._logger.info(u"{} {}".format(prefix, line))
			if msgType == "stderr":
				self._plugin_manager.send_plugin_message("usbfileman", dict(commandError = line))
			elif msgType == "stdout":
				self._plugin_manager.send_plugin_message("usbfileman", dict(commandResponse = line))


	def log_stdout(self, *lines):
		self.log(u">>>", "stdout", *lines)

	def log_stderr(self, *lines):
		self.log(u"!!!", "stderr", *lines)

	def log_call(self, *lines):
		self.log(u"---", "stdout", *lines)



	# try:
	# 	caller.checked_call(["some", "command", "with", "parameters"])
	# except CommandLineError as err:
	# 	self._logger.info(u"Command returned {}".format(err.returncode))
	# else:
	# 	self._logger.info(u"Command finished successfully")






# If you want your plugin to be registered within OctoPrint under a different name than what you defined in setup.py
# ("OctoPrint-PluginSkeleton"), you may define that here. Same goes for the other metadata derived from setup.py that
# can be overwritten via __plugin_xyz__ control properties. See the documentation for that.
__plugin_name__ = "Usbfileman Plugin"

def __plugin_load__():
	global __plugin_implementation__
	__plugin_implementation__ = UsbfilemanPlugin()

	global __plugin_hooks__
	__plugin_hooks__ = {
		"octoprint.plugin.softwareupdate.check_config": __plugin_implementation__.get_update_information
	}

