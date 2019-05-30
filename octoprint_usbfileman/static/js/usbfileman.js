/*
 * View model for OctoPrint-usbFileMan
 *
 * Author: Joshua Wills
 * License: AGPLv3
 */
$(function() {
	function UsbfilemanViewModel(parameters) {
		var self = this;

		// assign the injected parameters, e.g.:
		// self.loginStateViewModel = parameters[0];
		// self.settingsViewModel = parameters[1];
		self.adminAction = function(targetAction, payloadName, payload) {
			if (payloadName === undefined || payload === undefined){
				payloadName = "";
				payload = {};
			}



			var url = OctoPrint.getSimpleApiUrl("usbfileman");
			// console.log("Pre-adminAction blocking test.");
			OctoPrint.issueCommand(url, "adminAction", {"action":targetAction, "payload":{[payloadName]:payload}});
			// console.log("Post-adminAction blocking test.");

		};
	}

	/* view model class, parameters for constructor, container to bind to
	 * Please see http://docs.octoprint.org/en/master/plugins/viewmodels.html#registering-custom-viewmodels for more details
	 * and a full list of the available options.
	 */
	OCTOPRINT_VIEWMODELS.push({
		construct: UsbfilemanViewModel,
		// ViewModels your plugin depends on, e.g. loginStateViewModel, settingsViewModel, ...
		dependencies: [ /* "loginStateViewModel", "settingsViewModel" */ ],
		// Elements to bind to, e.g. #settings_plugin_usbfileman, #tab_plugin_usbfileman, ...
		elements: ["#usbfileman_settings"]
	});
});
