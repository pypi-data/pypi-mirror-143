import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin
} from '@jupyterlab/application';

import { ISettingRegistry } from '@jupyterlab/settingregistry';
import { IFileBrowserFactory } from '@jupyterlab/filebrowser';
import { fastForwardIcon } from '@jupyterlab/ui-components';

import { requestAPI } from '../handler';

/**
 * Initialization data for the jupyterlab_mutableai extension.
 */

const SETTINGS_PLUGIN_ID = 'jupyterlab_mutableai:settings-mutableai';

const contextMenu: JupyterFrontEndPlugin<void> = {
  id: 'jupyterlab_mutableai:contextMenu',
  autoStart: true,
  requires: [IFileBrowserFactory, ISettingRegistry],
  activate: (
    app: JupyterFrontEnd,
    factory: IFileBrowserFactory,
    settings: ISettingRegistry
  ) => {
    console.log('Mutable AI context menu is activated!');

    const { commands } = app;

    const command = 'context_menu:open';

    // Wait for the application to be restored and
    // for the settings for this plugin to be loaded
    Promise.all([app.restored, settings.load(SETTINGS_PLUGIN_ID)]).then(
      ([, setting]) => {
        commands.addCommand(command, {
          label: 'Fast Forward to Production with MutableAI',
          caption: 'Mutable AI context menu.',
          icon: fastForwardIcon,
          execute: () => {
            const file = factory.tracker.currentWidget?.selectedItems().next();

            const apiKey = setting.get('apiKey').composite as string;
            const transformDomain = setting.get('transformDomain')
              .composite as string;

            const dataToSend = { name: file?.path, apiKey, transformDomain };

            // POST request
            const reply = requestAPI<any>('TRANSFORM_NB', {
              body: JSON.stringify(dataToSend),
              method: 'POST'
            });

            // Log to console
            reply
              .then(response => console.log('Transformed Successfully!'))
              .catch(e => console.log('Transformation failed!', e));
          }
        });
      }
    );
  }
};

export default contextMenu;
