"use strict";
(self["webpackChunkjupyterlab_run_and_reload"] = self["webpackChunkjupyterlab_run_and_reload"] || []).push([["lib_index_js"],{

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _style_play_in_file_svg__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! ../style/play-in-file.svg */ "./style/play-in-file.svg");
/* harmony import */ var _style_fastforward_in_file_svg__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ../style/fastforward-in-file.svg */ "./style/fastforward-in-file.svg");








var CommandIDs;
(function (CommandIDs) {
    CommandIDs.runAndReloadAll = 'run-and-reload:run-all-cells-and-reload';
    CommandIDs.restartRunAndReloadAll = 'run-and-reload:restart-run-all-cells-and-reload';
    // TODO: Import this from notebook extension
    CommandIDs.restart = 'notebook:restart-kernel';
})(CommandIDs || (CommandIDs = {}));
// TODO: Change category to run items
const PALETTE_CATEGORY = 'Run and reload extension';
/**
 * Initialization data for the jupyterlab_run_and_reload extension.
 *
 * TODOs:
 * - Add setting: file extensions to reload
 * - Add setting: only reload visible widgets or not
 * - Add toolbar button in notebook panel with run and reload
 * - Also add "Restart kernel, run all cells and reload PDFs"
 */
const plugin = {
    id: 'jupyterlab_run_and_reload:plugin',
    autoStart: true,
    requires: [_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_2__.IDocumentManager],
    optional: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_0__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_1__.ICommandPalette],
    activate: (app, manager, settingRegistry, palette) => {
        console.log('JupyterLab extension jupyterlab_run_and_reload is activated!');
        if (settingRegistry) {
            settingRegistry
                .load(plugin.id)
                .then(settings => {
                console.log('jupyterlab_run_and_reload settings loaded:', settings.composite);
            })
                .catch(reason => {
                console.error('Failed to load settings for jupyterlab_run_and_reload.', reason);
            });
        }
        const { shell, commands } = app;
        const icon = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.LabIcon({
            name: 'run-and-reload:play-in-file-icon',
            svgstr: _style_play_in_file_svg__WEBPACK_IMPORTED_MODULE_6__["default"]
        });
        const icon2 = new _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.LabIcon({
            name: 'run-and-reload:fastforward-in-file-icon',
            svgstr: _style_fastforward_in_file_svg__WEBPACK_IMPORTED_MODULE_7__["default"]
        });
        function commandExecutionFunction(withRestart) {
            async function executeCommand() {
                // Get currently selected widget
                const currentWidget = shell.currentWidget;
                // If current widget is a notebook then we can run all cells
                // If not, then this command does not make sense and should not be callable actually
                if (!(currentWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.NotebookPanel)) {
                    return;
                }
                function widgetShouldReload(widget) {
                    const context = manager.contextForWidget(widget);
                    return context === null || context === void 0 ? void 0 : context.path.endsWith('.pdf');
                }
                // Get all attached widgets in the shell
                const currentWidgets = (0,_lumino_algorithm__WEBPACK_IMPORTED_MODULE_3__.toArray)(shell.widgets());
                // Obtain the list of widgets that might need to be reloaded after the notebook is finished
                const widgetsToReload = currentWidgets.filter(widgetShouldReload);
                const contextsToReload = widgetsToReload.map(widget => manager.contextForWidget(widget));
                // Connect the openOrReveal function to the fileChanged signal of the relevant widgets
                contextsToReload.forEach(context => {
                    context === null || context === void 0 ? void 0 : context.fileChanged.connect((context, model) => {
                        manager.openOrReveal(context.path);
                    });
                });
                // If current widget is a notebook then we can run all cells
                if (currentWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.NotebookPanel) {
                    let restarted;
                    if (withRestart) {
                        restarted = await commands.execute(CommandIDs.restart, {
                            activate: false
                        });
                    }
                    else {
                        restarted = true;
                    }
                    // TODO: Add check on result + notification if notebook run was not successfull
                    if (restarted) {
                        await _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.NotebookActions.runAll(currentWidget.content, currentWidget.sessionContext);
                    }
                    // Loop over all widgets in the shell and revert the relevant ones
                    for (const context of contextsToReload) {
                        context === null || context === void 0 ? void 0 : context.revert();
                    }
                }
            }
            return executeCommand;
        }
        commands.addCommand(CommandIDs.runAndReloadAll, {
            label: 'Run All Cells and Reload PDFs',
            caption: 'Run all the cells of the notebook and then reload static content that has changed (e.g. PDF).',
            icon: args => (args['ignoreIcon'] ? undefined : icon),
            isEnabled: () => shell.currentWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.NotebookPanel,
            execute: commandExecutionFunction(false)
        });
        commands.addCommand(CommandIDs.restartRunAndReloadAll, {
            label: 'Restart Kernel, Run All Cells and Reload PDFs',
            caption: 'Restart the kernel, run all the cells of the notebook and then reload static content that has changed (e.g. PDF).',
            icon: args => (args['ignoreIcon'] ? undefined : icon2),
            isEnabled: () => shell.currentWidget instanceof _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_4__.NotebookPanel,
            execute: commandExecutionFunction(true)
        });
        // Add the command to the palette
        if (palette) {
            palette.addItem({
                command: CommandIDs.runAndReloadAll,
                args: { ignoreIcon: true },
                category: PALETTE_CATEGORY
            });
            palette.addItem({
                command: CommandIDs.restartRunAndReloadAll,
                args: { ignoreIcon: true },
                category: PALETTE_CATEGORY
            });
        }
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./style/fastforward-in-file.svg":
/*!***************************************!*\
  !*** ./style/fastforward-in-file.svg ***!
  \***************************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg fill=\"var(--jp-icon-contrast-color0)\" xmlns=\"http://www.w3.org/2000/svg\"  viewBox=\"0 0 30 30\" width=\"210px\" height=\"210px\">\n<path d=\"M24.707,8.793l-6.5-6.5C18.019,2.105,17.765,2,17.5,2H7C5.895,2,5,2.895,5,4v22c0,1.105,0.895,2,2,2h16c1.105,0,2-0.895,2-2V9.5C25,9.235,24.895,8.981,24.707,8.793z M18,10c-0.552,0-1-0.448-1-1V3.904L23.096,10H18z\"/>\n<polygon points=\"8,15 8,23 15,19\" style=\"fill:var(--jp-toolbar-background);stroke:var(--jp-toolbar-background);stroke-width:1;stroke-linejoin:round\" />\n<polygon points=\"15,15 15,23 22,19\" style=\"fill:var(--jp-toolbar-background);stroke:var(--jp-toolbar-background);stroke-width:1;stroke-linejoin:round\" />\n</svg>");

/***/ }),

/***/ "./style/play-in-file.svg":
/*!********************************!*\
  !*** ./style/play-in-file.svg ***!
  \********************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = ("<svg fill=\"var(--jp-icon-contrast-color0)\" xmlns=\"http://www.w3.org/2000/svg\"  viewBox=\"0 0 30 30\" width=\"210px\" height=\"210px\">\n<path d=\"M24.707,8.793l-6.5-6.5C18.019,2.105,17.765,2,17.5,2H7C5.895,2,5,2.895,5,4v22c0,1.105,0.895,2,2,2h16c1.105,0,2-0.895,2-2V9.5C25,9.235,24.895,8.981,24.707,8.793z M18,10c-0.552,0-1-0.448-1-1V3.904L23.096,10H18z\"/>\n<polygon points=\"10,12 10,24 21,18\" style=\"fill:var(--jp-toolbar-background);stroke:var(--jp-toolbar-background);stroke-width:1;stroke-linejoin:round\" />\n</svg>");

/***/ })

}]);
//# sourceMappingURL=lib_index_js.4f63533ee086422e819e.js.map