/*
 * View model for OctoPrint-usbFileMan
 *
 * Author: Joshua Wills
 * License: AGPLv3
 */
$(function() {
	function UsbfilemanViewModel(parameters) {
		var self = this;
		self.commandResponse = ko.observable("");

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


		self.onDataUpdaterPluginMessage = function(plugin, data) {
			// self.mgLog("onDataUpdaterPluginMessage triggered.  Message:");
			// self.mgLog(data);
			if (plugin != "usbfileman") {
				// console.log('Ignoring '+plugin);
				return;
			}

			if (data.commandResponse !== undefined ){
				//console.log(data.commandResponse);
				// if (data.commandResponse.toString()[-1] != "\n") {
				// 	lineToLog = data.commandResponse.toString() + "\n";
				// }
				// else {
				// 	lineToLog = data.commandResponse.toString();
				// }

				self.commandResponse(self.commandResponse()+data.commandResponse.toString().trim()+"\n");
				//get div and scroll to bottom
				self.commandResponseText = $("#usbfileman_commandResponseText");
				self.commandResponseText.scrollTop(self.commandResponseText[0].scrollHeight);
			}

			if (data.commandError !== undefined){
				// if (data.commandError.toString()[-1] != "\n") {
				// 	lineToLog = data.commandError.toString() + "\n";
				// }
				// else {
				// 	lineToLog = data.commandError.toString();
				// }
				self.commandResponse(self.commandResponse()+data.commandError.toString().trim()+"\n");
				//get div and scroll to bottom
				self.commandResponseText = $("#usbfileman_commandResponseText");
				self.commandResponseText.scrollTop(self.commandResponseText[0].scrollHeight);
			}

			if (data.internetConnection !== undefined){
				if (data.internetConnection){
					self.googleGood(1);
				} else {
					self.googleGood(0);
				}
			}
		};

		self.showCommandResponse = function(input){
			command_response_popup = $("#usbfileman_command_response_popup");
			command_response_popup.modal({keyboard: false, backdrop: "static", show: true});
			if (input === "hide"){
				command_response_popup.modal("hide");
			}
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
