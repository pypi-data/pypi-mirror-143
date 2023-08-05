import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { MainAreaWidget } from '@jupyterlab/apputils';
import { settingsIcon } from '@jupyterlab/ui-components';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { SettingsWidget } from '../widgets/Settings';

const PLUGIN_ID = 'jupyterlab_mutableai:settings-mutableai';

const COMMAND_ID = 'jupyterlab_mutableai/settings:toggle-flag';
const COMMAND_SETTINGS_ID = 'jupyterlab_mutableai/settings:update-settings';

/**
 * Initialization data for the settings extension.
 */
const settings: JupyterFrontEndPlugin<void> = {
  id: PLUGIN_ID,
  autoStart: true,
  requires: [ISettingRegistry],
  activate: (app: JupyterFrontEnd, settings: ISettingRegistry) => {
    const { commands } = app;
    let flag = true;
    /**
     * Load the settings for this extension
     *
     * @param setting Extension settings
     */
    function loadSetting(setting: ISettingRegistry.ISettings): void {
      // Read the settings and convert to the correct type
      flag = setting.get('flag').composite as boolean;
    }

    // Wait for the application to be restored and
    // for the settings for this plugin to be loaded
    Promise.all([app.restored, settings.load(PLUGIN_ID)])
      .then(([, setting]) => {
        // Read the settings
        loadSetting(setting);

        // Listen for your plugin setting changes using Signal
        setting.changed.connect(loadSetting);

        commands.addCommand(COMMAND_ID, {
          label: 'AutoComplete',
          isToggled: () => flag,
          execute: () => {
            // Programmatically change a setting
            Promise.all([setting.set('flag', !flag)])
              .then(() => {
                const newFlag = setting.get('flag').composite as boolean;
                console.log(
                  `Mutable AI updated flag to '${
                    newFlag ? 'enabled' : 'disabled'
                  }'.`
                );
              })
              .catch(reason => {
                console.error(
                  `Something went wrong when changing the settings.\n${reason}`
                );
              });
          }
        });

        commands.addCommand(COMMAND_SETTINGS_ID, {
          label: 'Update Mutable AI Settings',
          execute: () => {
            const close = () => app.shell.currentWidget?.close();
            const content = new SettingsWidget(setting, close);
            const widget = new MainAreaWidget<SettingsWidget>({ content });
            widget.title.label = 'MutableAI Settings';
            widget.title.icon = settingsIcon;
            app.shell.add(widget, 'main');
          }
        });
      })
      .catch(reason => {
        console.error(
          `Something went wrong when reading the settings.\n${reason}`
        );
      });
  }
};

export default settings;
