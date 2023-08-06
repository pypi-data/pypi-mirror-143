"use strict";
(self["webpackChunk_jupyterlab_plugin_playground"] = self["webpackChunk_jupyterlab_plugin_playground"] || []).push([["lib_index_js"],{

/***/ "./lib/dialogs.js":
/*!************************!*\
  !*** ./lib/dialogs.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "formatCDNConsentDialog": () => (/* binding */ formatCDNConsentDialog)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

function formatCDNConsentDialog(moduleName, url) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null,
            moduleName,
            " is not a part of the distribution and needs to be downloaded before execution."),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null,
            "The current CDN URL is: ",
            url),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, "You should only allow to execute code from CDN if:"),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("ul", null,
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("li", null, "you fully trust the CDN provider AND your internet service provider AND your network administrator AND their ability to immediately remedy any attack against the network, or"),
            react__WEBPACK_IMPORTED_MODULE_0__.createElement("li", null, "you verified the integrity of the package by defining a cryptographic hash for verification via SRI feature [support to be implemented]")),
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("p", null, "You can abort execution and change the CDN URL in the settings first.")));
}


/***/ }),

/***/ "./lib/errors.js":
/*!***********************!*\
  !*** ./lib/errors.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "formatErrorWithResult": () => (/* binding */ formatErrorWithResult),
/* harmony export */   "formatImportError": () => (/* binding */ formatImportError)
/* harmony export */ });
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_0__);

function formatErrorWithResult(error, result) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
        "Error:",
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("pre", null, error.stack ? error.stack : error.message),
        "Final code:",
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("pre", null, result.code),
        result.transpiled
            ? 'The code was transpiled'
            : 'The code was not transpiled',
        "."));
}
function formatImportError(error, module) {
    return (react__WEBPACK_IMPORTED_MODULE_0__.createElement("div", null,
        "Error when importing ",
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("code", null, module),
        ":",
        react__WEBPACK_IMPORTED_MODULE_0__.createElement("pre", null, error.stack ? error.stack : error.message)));
}


/***/ }),

/***/ "./lib/index.js":
/*!**********************!*\
  !*** ./lib/index.js ***!
  \**********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "default": () => (__WEBPACK_DEFAULT_EXPORT__)
/* harmony export */ });
/* harmony import */ var typescript__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typescript */ "webpack/sharing/consume/default/typescript/typescript");
/* harmony import */ var typescript__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(typescript__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _loader__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! ./loader */ "./lib/loader.js");
/* harmony import */ var _transpiler__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! ./transpiler */ "./lib/transpiler.js");
/* harmony import */ var _modules__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! ./modules */ "./lib/modules.js");
/* harmony import */ var _errors__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! ./errors */ "./lib/errors.js");
/* harmony import */ var _resolver__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! ./resolver */ "./lib/resolver.js");
/* harmony import */ var _requirejs__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! ./requirejs */ "./lib/requirejs.js");













var CommandIDs;
(function (CommandIDs) {
    CommandIDs.createNewFile = 'plugin-playground:create-new-plugin';
    CommandIDs.loadCurrentAsExtension = 'plugin-playground:load-as-extension';
})(CommandIDs || (CommandIDs = {}));
const PLUGIN_TEMPLATE = `import {
  JupyterFrontEnd,
  JupyterFrontEndPlugin,
} from '@jupyterlab/application';

/**
 * This is an example hello world plugin.
 * Open Command Palette with Ctrl+Shift+C
 * (Command+Shift+C on Mac) and select
 * "Load Current File as Extension"
 */
const plugin: JupyterFrontEndPlugin<void> = {
  id: 'hello-world:plugin',
  autoStart: true,
  activate: (app: JupyterFrontEnd) => {
    alert('Hello World!');
  },
};

export default plugin;
`;
class PluginPlayground {
    constructor(app, settingRegistry, commandPalette, editorTracker, launcher, documentManager, settings, requirejs) {
        this.app = app;
        this.settingRegistry = settingRegistry;
        this.documentManager = documentManager;
        this.settings = settings;
        this.requirejs = requirejs;
        // Define the widgets base module for RequireJS (left for compatibility only)
        requirejs.define('@jupyter-widgets/base', [], () => _modules__WEBPACK_IMPORTED_MODULE_7__.modules["@jupyter-widgets/base"]);
        app.commands.addCommand(CommandIDs.loadCurrentAsExtension, {
            label: 'Load Current File As Extension',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.extensionIcon,
            isEnabled: () => editorTracker.currentWidget !== null &&
                editorTracker.currentWidget === app.shell.currentWidget,
            execute: async () => {
                const currentWidget = editorTracker.currentWidget;
                if (currentWidget) {
                    const currentText = currentWidget.context.model.toString();
                    this._loadPlugin(currentText, currentWidget.context.path);
                }
            }
        });
        commandPalette.addItem({
            command: CommandIDs.loadCurrentAsExtension,
            category: 'Plugin Playground',
            args: {}
        });
        app.commands.addCommand(CommandIDs.createNewFile, {
            label: 'TypeScript File (Playground)',
            caption: 'Create a new TypeScript file',
            icon: _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_5__.extensionIcon,
            execute: async (args) => {
                const model = await app.commands.execute('docmanager:new-untitled', {
                    path: args['cwd'],
                    type: 'file',
                    ext: 'ts'
                });
                const widget = await app.commands.execute('docmanager:open', {
                    path: model.path,
                    factory: 'Editor'
                });
                if (widget) {
                    widget.content.ready.then(() => {
                        widget.content.model.value.text = PLUGIN_TEMPLATE;
                    });
                }
                return widget;
            }
        });
        app.restored.then(async () => {
            const settings = this.settings;
            this._updateSettings(requirejs, settings);
            // add to the launcher
            if (launcher && settings.composite.showIconInLauncher) {
                launcher.add({
                    command: CommandIDs.createNewFile,
                    category: 'Other',
                    rank: 1
                });
            }
            const urls = settings.composite.urls;
            for (const u of urls) {
                await this._getModule(u);
            }
            const plugins = settings.composite.plugins;
            for (const t of plugins) {
                await this._loadPlugin(t, null);
            }
            settings.changed.connect(updatedSettings => {
                this._updateSettings(requirejs, updatedSettings);
            });
        });
    }
    _updateSettings(requirejs, settings) {
        const baseURL = settings.composite.requirejsCDN;
        requirejs.require.config({
            baseUrl: baseURL
        });
    }
    async _loadPlugin(code, path) {
        const tokenMap = new Map(Array.from(this.app._serviceMap.keys()).map((t) => [
            t.name,
            t
        ]));
        // Widget registry does not follow convention of importName:tokenName
        tokenMap.set('@jupyter-widgets/base:IJupyterWidgetRegistry', tokenMap.get('jupyter.extensions.jupyterWidgetRegistry'));
        const importResolver = new _resolver__WEBPACK_IMPORTED_MODULE_8__.ImportResolver({
            modules: _modules__WEBPACK_IMPORTED_MODULE_7__.modules,
            tokenMap: tokenMap,
            requirejs: this.requirejs,
            settings: this.settings,
            serviceManager: this.app.serviceManager,
            basePath: path
        });
        const pluginLoader = new _loader__WEBPACK_IMPORTED_MODULE_9__.PluginLoader({
            transpiler: new _transpiler__WEBPACK_IMPORTED_MODULE_10__.PluginTranspiler({
                compilerOptions: {
                    target: (typescript__WEBPACK_IMPORTED_MODULE_0___default().ScriptTarget.ES2017),
                    jsx: (typescript__WEBPACK_IMPORTED_MODULE_0___default().JsxEmit.React)
                }
            }),
            importFunction: importResolver.resolve.bind(importResolver),
            tokenMap: tokenMap,
            serviceManager: this.app.serviceManager,
            requirejs: this.requirejs
        });
        importResolver.dynamicLoader = pluginLoader.loadFile.bind(pluginLoader);
        let result;
        try {
            result = await pluginLoader.load(code, path);
        }
        catch (error) {
            if (error instanceof _loader__WEBPACK_IMPORTED_MODULE_9__.PluginLoadingError) {
                const internalError = error.error;
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: `Plugin loading failed: ${internalError.message}`,
                    body: (0,_errors__WEBPACK_IMPORTED_MODULE_11__.formatErrorWithResult)(error, error.partialResult)
                });
            }
            else {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showErrorMessage)('Plugin loading failed', error.message);
            }
            return;
        }
        const plugin = result.plugin;
        if (result.schema) {
            // TODO: this is mostly fine to get the menus and toolbars, but:
            // - transforms are not applied
            // - any refresh from the server might overwrite the data
            // - it is not a good long term solution in general
            this.settingRegistry.plugins[plugin.id] = {
                id: plugin.id,
                schema: JSON.parse(result.schema),
                raw: result.schema,
                data: {
                    composite: {},
                    user: {}
                },
                version: '0.0.0'
            };
            this.settingRegistry.pluginChanged.emit(plugin.id);
        }
        // Unregister plugin if already registered.
        if (this.app.hasPlugin(plugin.id)) {
            delete this.app._pluginMap[plugin.id];
        }
        this.app.registerPluginModule(plugin);
        if (plugin.autoStart) {
            try {
                await this.app.activatePlugin(plugin.id);
            }
            catch (e) {
                (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.showDialog)({
                    title: `Plugin autostart failed: ${e.message}`,
                    body: (0,_errors__WEBPACK_IMPORTED_MODULE_11__.formatErrorWithResult)(e, result)
                });
                return;
            }
        }
    }
    async _getModule(url) {
        const response = await fetch(url);
        const jsBody = await response.text();
        this._loadPlugin(jsBody, null);
    }
}
/**
 * Initialization data for the @jupyterlab/plugin-playground extension.
 */
const plugin = {
    id: '@jupyterlab/plugin-playground:plugin',
    autoStart: true,
    requires: [_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_1__.ISettingRegistry, _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__.ICommandPalette, _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_3__.IEditorTracker],
    optional: [_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_4__.ILauncher, _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_6__.IDocumentManager],
    activate: (app, settingRegistry, commandPalette, editorTracker, launcher, documentManager) => {
        // In order to accommodate loading ipywidgets and other AMD modules, we
        // load RequireJS before loading any custom extensions.
        const requirejsLoader = new _requirejs__WEBPACK_IMPORTED_MODULE_12__.RequireJSLoader();
        // We coud convert to `async` and use `await` but we don't, because a failure
        // would freeze JupyterLab on splash screen; this way if it fails to load,
        // only the plugin is affected, not the entire application.
        Promise.all([settingRegistry.load(plugin.id), requirejsLoader.load()]).then(([settings, requirejs]) => {
            new PluginPlayground(app, settingRegistry, commandPalette, editorTracker, launcher, documentManager, settings, requirejs);
        });
    }
};
/* harmony default export */ const __WEBPACK_DEFAULT_EXPORT__ = (plugin);


/***/ }),

/***/ "./lib/loader.js":
/*!***********************!*\
  !*** ./lib/loader.js ***!
  \***********************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "PluginLoader": () => (/* binding */ PluginLoader),
/* harmony export */   "PluginLoadingError": () => (/* binding */ PluginLoadingError)
/* harmony export */ });
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _transpiler__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! ./transpiler */ "./lib/transpiler.js");


class PluginLoader {
    constructor(options) {
        this._options = options;
    }
    async loadFile(code) {
        const functionBody = this._options.transpiler.transpile(code, false);
        return await this._createAsyncFunctionModule(functionBody);
    }
    async _createAsyncFunctionModule(transpiledCode) {
        const module = new AsyncFunction(this._options.transpiler.importFunctionName, transpiledCode);
        return await module(this._options.importFunction);
    }
    async _discoverSchema(pluginPath) {
        if (!pluginPath) {
            console.warn('Not looking for schema: no path');
            return null;
        }
        const serviceManager = this._options.serviceManager;
        if (!serviceManager) {
            console.warn('Not looking for schema: no document manager');
            return null;
        }
        const candidatePaths = [
            // canonical
            _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.join(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.dirname(pluginPath), '..', 'schema', 'plugin.json'),
            // simplification for dynamic plugins
            _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.join(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_0__.PathExt.dirname(pluginPath), 'plugin.json')
        ];
        for (const path of candidatePaths) {
            console.log(`Looking for schema in ${path}`);
            try {
                const file = await serviceManager.contents.get(path);
                console.log(`Found schema in ${path}`);
                return file.content;
            }
            catch (e) {
                console.log(`Did not find schema in ${path}`);
            }
        }
        return null;
    }
    /**
     * Create a plugin from TypeScript code.
     */
    async load(code, basePath) {
        var _a, _b;
        let functionBody;
        let plugin;
        let transpiled = true;
        try {
            functionBody = this._options.transpiler.transpile(code, true);
        }
        catch (error) {
            if (error instanceof _transpiler__WEBPACK_IMPORTED_MODULE_1__.NoDefaultExportError) {
                // no export statment
                // for compatibility with older version
                console.log('No default export was found in the plugin code, falling back to object-based evaluation');
                functionBody = `'use strict';\nreturn (${code})`;
                transpiled = false;
            }
            else {
                throw error;
            }
        }
        console.log(functionBody);
        let schema = null;
        try {
            if (transpiled) {
                const module = await this._createAsyncFunctionModule(functionBody);
                plugin = module.default;
                schema = await this._discoverSchema(basePath);
            }
            else {
                const requirejs = this._options.requirejs;
                plugin = new Function('require', 'requirejs', 'define', functionBody)(requirejs.require, requirejs.require, requirejs.define);
            }
        }
        catch (e) {
            throw new PluginLoadingError(e, { code: functionBody, transpiled });
        }
        // We allow one level of indirection (return a function instead of a plugin)
        if (typeof plugin === 'function') {
            plugin = plugin();
        }
        // Finally, we allow returning a promise (or an async function above).
        plugin = (await Promise.resolve(plugin));
        plugin.requires = (_a = plugin.requires) === null || _a === void 0 ? void 0 : _a.map((value) => {
            if (!isString(value)) {
                // already a token
                return value;
            }
            const token = this._options.tokenMap.get(value);
            if (!token) {
                throw Error('Required token' + value + 'not found in the token map');
            }
            return token;
        });
        plugin.optional = (_b = plugin.optional) === null || _b === void 0 ? void 0 : _b.map((value) => {
            if (!isString(value)) {
                // already a token
                return value;
            }
            const token = this._options.tokenMap.get(value);
            if (!token) {
                console.log('Optional token' + value + 'not found in the token map');
            }
            return token;
        }).filter((token) => token != null);
        return {
            schema,
            plugin,
            code: functionBody,
            transpiled
        };
    }
}
function isString(value) {
    return typeof value === 'string' || value instanceof String;
}
class PluginLoadingError extends Error {
    constructor(error, partialResult) {
        super();
        this.error = error;
        this.partialResult = partialResult;
    }
}
const AsyncFunction = Object.getPrototypeOf(async () => {
    // no-op
}).constructor;


/***/ }),

/***/ "./lib/modules.js":
/*!************************!*\
  !*** ./lib/modules.js ***!
  \************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "modules": () => (/* binding */ modules)
/* harmony export */ });
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyter-widgets/base */ "webpack/sharing/consume/default/@jupyter-widgets/base/@jupyter-widgets/base");
/* harmony import */ var _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/application */ "webpack/sharing/consume/default/@jupyterlab/application");
/* harmony import */ var _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__);
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! @jupyterlab/codeeditor */ "webpack/sharing/consume/default/@jupyterlab/codeeditor");
/* harmony import */ var _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__);
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__ = __webpack_require__(/*! @jupyterlab/codemirror */ "webpack/sharing/consume/default/@jupyterlab/codemirror");
/* harmony import */ var _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__);
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_5__ = __webpack_require__(/*! @jupyterlab/completer */ "webpack/sharing/consume/default/@jupyterlab/completer");
/* harmony import */ var _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_5___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_completer__WEBPACK_IMPORTED_MODULE_5__);
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_6__ = __webpack_require__(/*! @jupyterlab/console */ "webpack/sharing/consume/default/@jupyterlab/console");
/* harmony import */ var _jupyterlab_console__WEBPACK_IMPORTED_MODULE_6___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_console__WEBPACK_IMPORTED_MODULE_6__);
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7__);
/* harmony import */ var _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_8__ = __webpack_require__(/*! @jupyterlab/debugger */ "webpack/sharing/consume/default/@jupyterlab/debugger");
/* harmony import */ var _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_8___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_8__);
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_9__ = __webpack_require__(/*! @jupyterlab/docmanager */ "webpack/sharing/consume/default/@jupyterlab/docmanager");
/* harmony import */ var _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_9___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_9__);
/* harmony import */ var _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_10__ = __webpack_require__(/*! @jupyterlab/docprovider */ "webpack/sharing/consume/default/@jupyterlab/docprovider");
/* harmony import */ var _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_10___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_10__);
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_11__ = __webpack_require__(/*! @jupyterlab/docregistry */ "webpack/sharing/consume/default/@jupyterlab/docregistry");
/* harmony import */ var _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_11___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_11__);
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_12__ = __webpack_require__(/*! @jupyterlab/documentsearch */ "webpack/sharing/consume/default/@jupyterlab/documentsearch");
/* harmony import */ var _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_12___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_12__);
/* harmony import */ var _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_13__ = __webpack_require__(/*! @jupyterlab/extensionmanager */ "webpack/sharing/consume/default/@jupyterlab/extensionmanager");
/* harmony import */ var _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_13___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_13__);
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_14__ = __webpack_require__(/*! @jupyterlab/filebrowser */ "webpack/sharing/consume/default/@jupyterlab/filebrowser");
/* harmony import */ var _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_14___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_14__);
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_15__ = __webpack_require__(/*! @jupyterlab/fileeditor */ "webpack/sharing/consume/default/@jupyterlab/fileeditor");
/* harmony import */ var _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_15___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_15__);
/* harmony import */ var _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_16__ = __webpack_require__(/*! @jupyterlab/imageviewer */ "webpack/sharing/consume/default/@jupyterlab/imageviewer");
/* harmony import */ var _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_16___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_16__);
/* harmony import */ var _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_17__ = __webpack_require__(/*! @jupyterlab/inspector */ "webpack/sharing/consume/default/@jupyterlab/inspector");
/* harmony import */ var _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_17___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_17__);
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_18__ = __webpack_require__(/*! @jupyterlab/launcher */ "webpack/sharing/consume/default/@jupyterlab/launcher");
/* harmony import */ var _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_18___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_18__);
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_19__ = __webpack_require__(/*! @jupyterlab/logconsole */ "webpack/sharing/consume/default/@jupyterlab/logconsole");
/* harmony import */ var _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_19___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_19__);
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_20__ = __webpack_require__(/*! @jupyterlab/mainmenu */ "webpack/sharing/consume/default/@jupyterlab/mainmenu");
/* harmony import */ var _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_20___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_20__);
/* harmony import */ var _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_21__ = __webpack_require__(/*! @jupyterlab/markdownviewer */ "webpack/sharing/consume/default/@jupyterlab/markdownviewer");
/* harmony import */ var _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_21___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_21__);
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_22__ = __webpack_require__(/*! @jupyterlab/notebook */ "webpack/sharing/consume/default/@jupyterlab/notebook");
/* harmony import */ var _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_22___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_22__);
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_23__ = __webpack_require__(/*! @jupyterlab/outputarea */ "webpack/sharing/consume/default/@jupyterlab/outputarea");
/* harmony import */ var _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_23___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_23__);
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_24__ = __webpack_require__(/*! @jupyterlab/rendermime */ "webpack/sharing/consume/default/@jupyterlab/rendermime");
/* harmony import */ var _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_24___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_24__);
/* harmony import */ var _jupyterlab_rendermime_interfaces__WEBPACK_IMPORTED_MODULE_25__ = __webpack_require__(/*! @jupyterlab/rendermime-interfaces */ "webpack/sharing/consume/default/@jupyterlab/rendermime-interfaces");
/* harmony import */ var _jupyterlab_rendermime_interfaces__WEBPACK_IMPORTED_MODULE_25___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_rendermime_interfaces__WEBPACK_IMPORTED_MODULE_25__);
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_26__ = __webpack_require__(/*! @jupyterlab/services */ "webpack/sharing/consume/default/@jupyterlab/services");
/* harmony import */ var _jupyterlab_services__WEBPACK_IMPORTED_MODULE_26___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_services__WEBPACK_IMPORTED_MODULE_26__);
/* harmony import */ var _jupyterlab_settingeditor__WEBPACK_IMPORTED_MODULE_27__ = __webpack_require__(/*! @jupyterlab/settingeditor */ "webpack/sharing/consume/default/@jupyterlab/settingeditor");
/* harmony import */ var _jupyterlab_settingeditor__WEBPACK_IMPORTED_MODULE_27___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingeditor__WEBPACK_IMPORTED_MODULE_27__);
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_28__ = __webpack_require__(/*! @jupyterlab/settingregistry */ "webpack/sharing/consume/default/@jupyterlab/settingregistry");
/* harmony import */ var _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_28___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_28__);
/* harmony import */ var _jupyterlab_shared_models__WEBPACK_IMPORTED_MODULE_29__ = __webpack_require__(/*! @jupyterlab/shared-models */ "webpack/sharing/consume/default/@jupyterlab/shared-models");
/* harmony import */ var _jupyterlab_shared_models__WEBPACK_IMPORTED_MODULE_29___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_shared_models__WEBPACK_IMPORTED_MODULE_29__);
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_30__ = __webpack_require__(/*! @jupyterlab/statedb */ "webpack/sharing/consume/default/@jupyterlab/statedb");
/* harmony import */ var _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_30___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_30__);
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_31__ = __webpack_require__(/*! @jupyterlab/statusbar */ "webpack/sharing/consume/default/@jupyterlab/statusbar");
/* harmony import */ var _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_31___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_31__);
/* harmony import */ var _jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_32__ = __webpack_require__(/*! @jupyterlab/terminal */ "webpack/sharing/consume/default/@jupyterlab/terminal");
/* harmony import */ var _jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_32___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_32__);
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_33__ = __webpack_require__(/*! @jupyterlab/toc */ "webpack/sharing/consume/default/@jupyterlab/toc");
/* harmony import */ var _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_33___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_toc__WEBPACK_IMPORTED_MODULE_33__);
/* harmony import */ var _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_34__ = __webpack_require__(/*! @jupyterlab/tooltip */ "webpack/sharing/consume/default/@jupyterlab/tooltip");
/* harmony import */ var _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_34___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_34__);
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_35__ = __webpack_require__(/*! @jupyterlab/translation */ "webpack/sharing/consume/default/@jupyterlab/translation");
/* harmony import */ var _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_35___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_translation__WEBPACK_IMPORTED_MODULE_35__);
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_36__ = __webpack_require__(/*! @jupyterlab/ui-components */ "webpack/sharing/consume/default/@jupyterlab/ui-components");
/* harmony import */ var _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_36___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_36__);
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_37__ = __webpack_require__(/*! @lumino/algorithm */ "webpack/sharing/consume/default/@lumino/algorithm");
/* harmony import */ var _lumino_algorithm__WEBPACK_IMPORTED_MODULE_37___default = /*#__PURE__*/__webpack_require__.n(_lumino_algorithm__WEBPACK_IMPORTED_MODULE_37__);
/* harmony import */ var _lumino_application__WEBPACK_IMPORTED_MODULE_38__ = __webpack_require__(/*! @lumino/application */ "webpack/sharing/consume/default/@lumino/application");
/* harmony import */ var _lumino_application__WEBPACK_IMPORTED_MODULE_38___default = /*#__PURE__*/__webpack_require__.n(_lumino_application__WEBPACK_IMPORTED_MODULE_38__);
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_39__ = __webpack_require__(/*! @lumino/commands */ "webpack/sharing/consume/default/@lumino/commands");
/* harmony import */ var _lumino_commands__WEBPACK_IMPORTED_MODULE_39___default = /*#__PURE__*/__webpack_require__.n(_lumino_commands__WEBPACK_IMPORTED_MODULE_39__);
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_40__ = __webpack_require__(/*! @lumino/coreutils */ "webpack/sharing/consume/default/@lumino/coreutils");
/* harmony import */ var _lumino_coreutils__WEBPACK_IMPORTED_MODULE_40___default = /*#__PURE__*/__webpack_require__.n(_lumino_coreutils__WEBPACK_IMPORTED_MODULE_40__);
/* harmony import */ var _lumino_datagrid__WEBPACK_IMPORTED_MODULE_41__ = __webpack_require__(/*! @lumino/datagrid */ "./node_modules/@lumino/datagrid/dist/index.es6.js");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_42__ = __webpack_require__(/*! @lumino/disposable */ "webpack/sharing/consume/default/@lumino/disposable");
/* harmony import */ var _lumino_disposable__WEBPACK_IMPORTED_MODULE_42___default = /*#__PURE__*/__webpack_require__.n(_lumino_disposable__WEBPACK_IMPORTED_MODULE_42__);
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_43__ = __webpack_require__(/*! @lumino/domutils */ "webpack/sharing/consume/default/@lumino/domutils");
/* harmony import */ var _lumino_domutils__WEBPACK_IMPORTED_MODULE_43___default = /*#__PURE__*/__webpack_require__.n(_lumino_domutils__WEBPACK_IMPORTED_MODULE_43__);
/* harmony import */ var _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_44__ = __webpack_require__(/*! @lumino/dragdrop */ "webpack/sharing/consume/default/@lumino/dragdrop");
/* harmony import */ var _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_44___default = /*#__PURE__*/__webpack_require__.n(_lumino_dragdrop__WEBPACK_IMPORTED_MODULE_44__);
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_45__ = __webpack_require__(/*! @lumino/messaging */ "webpack/sharing/consume/default/@lumino/messaging");
/* harmony import */ var _lumino_messaging__WEBPACK_IMPORTED_MODULE_45___default = /*#__PURE__*/__webpack_require__.n(_lumino_messaging__WEBPACK_IMPORTED_MODULE_45__);
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_46__ = __webpack_require__(/*! @lumino/properties */ "webpack/sharing/consume/default/@lumino/properties");
/* harmony import */ var _lumino_properties__WEBPACK_IMPORTED_MODULE_46___default = /*#__PURE__*/__webpack_require__.n(_lumino_properties__WEBPACK_IMPORTED_MODULE_46__);
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_47__ = __webpack_require__(/*! @lumino/signaling */ "webpack/sharing/consume/default/@lumino/signaling");
/* harmony import */ var _lumino_signaling__WEBPACK_IMPORTED_MODULE_47___default = /*#__PURE__*/__webpack_require__.n(_lumino_signaling__WEBPACK_IMPORTED_MODULE_47__);
/* harmony import */ var _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_48__ = __webpack_require__(/*! @lumino/virtualdom */ "webpack/sharing/consume/default/@lumino/virtualdom");
/* harmony import */ var _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_48___default = /*#__PURE__*/__webpack_require__.n(_lumino_virtualdom__WEBPACK_IMPORTED_MODULE_48__);
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_49__ = __webpack_require__(/*! @lumino/widgets */ "webpack/sharing/consume/default/@lumino/widgets");
/* harmony import */ var _lumino_widgets__WEBPACK_IMPORTED_MODULE_49___default = /*#__PURE__*/__webpack_require__.n(_lumino_widgets__WEBPACK_IMPORTED_MODULE_49__);
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_50__ = __webpack_require__(/*! react */ "webpack/sharing/consume/default/react");
/* harmony import */ var react__WEBPACK_IMPORTED_MODULE_50___default = /*#__PURE__*/__webpack_require__.n(react__WEBPACK_IMPORTED_MODULE_50__);
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_51__ = __webpack_require__(/*! react-dom */ "webpack/sharing/consume/default/react-dom");
/* harmony import */ var react_dom__WEBPACK_IMPORTED_MODULE_51___default = /*#__PURE__*/__webpack_require__.n(react_dom__WEBPACK_IMPORTED_MODULE_51__);




















































const modules = {
    '@jupyter-widgets/base': _jupyter_widgets_base__WEBPACK_IMPORTED_MODULE_0__,
    '@jupyterlab/application': _jupyterlab_application__WEBPACK_IMPORTED_MODULE_1__,
    '@jupyterlab/apputils': _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_2__,
    '@jupyterlab/codeeditor': _jupyterlab_codeeditor__WEBPACK_IMPORTED_MODULE_3__,
    '@jupyterlab/codemirror': _jupyterlab_codemirror__WEBPACK_IMPORTED_MODULE_4__,
    '@jupyterlab/completer': _jupyterlab_completer__WEBPACK_IMPORTED_MODULE_5__,
    '@jupyterlab/console': _jupyterlab_console__WEBPACK_IMPORTED_MODULE_6__,
    '@jupyterlab/coreutils': _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_7__,
    '@jupyterlab/debugger': _jupyterlab_debugger__WEBPACK_IMPORTED_MODULE_8__,
    '@jupyterlab/docmanager': _jupyterlab_docmanager__WEBPACK_IMPORTED_MODULE_9__,
    '@jupyterlab/docprovider': _jupyterlab_docprovider__WEBPACK_IMPORTED_MODULE_10__,
    '@jupyterlab/docregistry': _jupyterlab_docregistry__WEBPACK_IMPORTED_MODULE_11__,
    '@jupyterlab/documentsearch': _jupyterlab_documentsearch__WEBPACK_IMPORTED_MODULE_12__,
    '@jupyterlab/extensionmanager': _jupyterlab_extensionmanager__WEBPACK_IMPORTED_MODULE_13__,
    '@jupyterlab/filebrowser': _jupyterlab_filebrowser__WEBPACK_IMPORTED_MODULE_14__,
    '@jupyterlab/fileeditor': _jupyterlab_fileeditor__WEBPACK_IMPORTED_MODULE_15__,
    '@jupyterlab/imageviewer': _jupyterlab_imageviewer__WEBPACK_IMPORTED_MODULE_16__,
    '@jupyterlab/inspector': _jupyterlab_inspector__WEBPACK_IMPORTED_MODULE_17__,
    '@jupyterlab/launcher': _jupyterlab_launcher__WEBPACK_IMPORTED_MODULE_18__,
    '@jupyterlab/logconsole': _jupyterlab_logconsole__WEBPACK_IMPORTED_MODULE_19__,
    '@jupyterlab/mainmenu': _jupyterlab_mainmenu__WEBPACK_IMPORTED_MODULE_20__,
    '@jupyterlab/markdownviewer': _jupyterlab_markdownviewer__WEBPACK_IMPORTED_MODULE_21__,
    '@jupyterlab/notebook': _jupyterlab_notebook__WEBPACK_IMPORTED_MODULE_22__,
    '@jupyterlab/outputarea': _jupyterlab_outputarea__WEBPACK_IMPORTED_MODULE_23__,
    '@jupyterlab/rendermime': _jupyterlab_rendermime__WEBPACK_IMPORTED_MODULE_24__,
    '@jupyterlab/rendermime-interfaces': _jupyterlab_rendermime_interfaces__WEBPACK_IMPORTED_MODULE_25__,
    '@jupyterlab/services': _jupyterlab_services__WEBPACK_IMPORTED_MODULE_26__,
    '@jupyterlab/settingeditor': _jupyterlab_settingeditor__WEBPACK_IMPORTED_MODULE_27__,
    '@jupyterlab/settingregistry': _jupyterlab_settingregistry__WEBPACK_IMPORTED_MODULE_28__,
    '@jupyterlab/shared-models': _jupyterlab_shared_models__WEBPACK_IMPORTED_MODULE_29__,
    '@jupyterlab/statedb': _jupyterlab_statedb__WEBPACK_IMPORTED_MODULE_30__,
    '@jupyterlab/statusbar': _jupyterlab_statusbar__WEBPACK_IMPORTED_MODULE_31__,
    '@jupyterlab/terminal': _jupyterlab_terminal__WEBPACK_IMPORTED_MODULE_32__,
    '@jupyterlab/toc': _jupyterlab_toc__WEBPACK_IMPORTED_MODULE_33__,
    '@jupyterlab/tooltip': _jupyterlab_tooltip__WEBPACK_IMPORTED_MODULE_34__,
    '@jupyterlab/translation': _jupyterlab_translation__WEBPACK_IMPORTED_MODULE_35__,
    '@jupyterlab/ui-components': _jupyterlab_ui_components__WEBPACK_IMPORTED_MODULE_36__,
    '@lumino/algorithm': _lumino_algorithm__WEBPACK_IMPORTED_MODULE_37__,
    '@lumino/application': _lumino_application__WEBPACK_IMPORTED_MODULE_38__,
    '@lumino/commands': _lumino_commands__WEBPACK_IMPORTED_MODULE_39__,
    '@lumino/coreutils': _lumino_coreutils__WEBPACK_IMPORTED_MODULE_40__,
    '@lumino/datagrid': _lumino_datagrid__WEBPACK_IMPORTED_MODULE_41__,
    '@lumino/disposable': _lumino_disposable__WEBPACK_IMPORTED_MODULE_42__,
    '@lumino/domutils': _lumino_domutils__WEBPACK_IMPORTED_MODULE_43__,
    '@lumino/dragdrop': _lumino_dragdrop__WEBPACK_IMPORTED_MODULE_44__,
    '@lumino/messaging': _lumino_messaging__WEBPACK_IMPORTED_MODULE_45__,
    '@lumino/properties': _lumino_properties__WEBPACK_IMPORTED_MODULE_46__,
    '@lumino/signaling': _lumino_signaling__WEBPACK_IMPORTED_MODULE_47__,
    '@lumino/virtualdom': _lumino_virtualdom__WEBPACK_IMPORTED_MODULE_48__,
    '@lumino/widgets': _lumino_widgets__WEBPACK_IMPORTED_MODULE_49__,
    react: react__WEBPACK_IMPORTED_MODULE_50__,
    'react-dom': react_dom__WEBPACK_IMPORTED_MODULE_51__
};


/***/ }),

/***/ "./lib/requirejs.js":
/*!**************************!*\
  !*** ./lib/requirejs.js ***!
  \**************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "loadInIsolated": () => (/* binding */ loadInIsolated),
/* harmony export */   "RequireJSLoader": () => (/* binding */ RequireJSLoader)
/* harmony export */ });
/* harmony import */ var _raw_loader_node_modules_requirejs_require_js__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! !!raw-loader!../node_modules/requirejs/require.js */ "./node_modules/raw-loader/dist/cjs.js!./node_modules/requirejs/require.js");
/// <reference types="requirejs" />

/**
 * Load requirejs in an iframe to avoid polution of `window` object.
 */
async function loadInIsolated(source) {
    return new Promise((resolve, reject) => {
        const iframe = document.createElement('iframe');
        iframe.style.display = 'none';
        iframe.onload = () => {
            const contentWindow = iframe.contentWindow;
            if (!contentWindow) {
                reject('Cannot load in isolated: no contentWindow, origin error?');
                return;
            }
            const iframeWindow = contentWindow.window;
            // execure require JS
            iframeWindow.eval(source);
            const requirejs = {
                require: iframeWindow.require,
                define: iframeWindow.define
            };
            if (requirejs.require && requirejs.define) {
                resolve(requirejs);
            }
            else {
                reject('Require.js loading did not result in `require` and `define` objects attachment to window');
            }
            // Note: cannot remove child from parent node, or require.js will not work
            // because it's timer will not be able to tick (no window reference)!
            iframe.onload = null;
        };
        document.body.appendChild(iframe);
    });
}
class RequireJSLoader {
    async load() {
        return await loadInIsolated(_raw_loader_node_modules_requirejs_require_js__WEBPACK_IMPORTED_MODULE_0__["default"]);
    }
}


/***/ }),

/***/ "./lib/resolver.js":
/*!*************************!*\
  !*** ./lib/resolver.js ***!
  \*************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "ImportResolver": () => (/* binding */ ImportResolver)
/* harmony export */ });
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! @jupyterlab/apputils */ "webpack/sharing/consume/default/@jupyterlab/apputils");
/* harmony import */ var _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__);
/* harmony import */ var _errors__WEBPACK_IMPORTED_MODULE_2__ = __webpack_require__(/*! ./errors */ "./lib/errors.js");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__ = __webpack_require__(/*! @jupyterlab/coreutils */ "webpack/sharing/consume/default/@jupyterlab/coreutils");
/* harmony import */ var _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1___default = /*#__PURE__*/__webpack_require__.n(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__);
/* harmony import */ var _dialogs__WEBPACK_IMPORTED_MODULE_3__ = __webpack_require__(/*! ./dialogs */ "./lib/dialogs.js");




function handleImportError(error, module) {
    return (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
        title: `Import in plugin code failed: ${error.message}`,
        body: (0,_errors__WEBPACK_IMPORTED_MODULE_2__.formatImportError)(error, module)
    });
}
async function askUserForCDNPolicy(exampleModule, cdnUrl) {
    const decision = await (0,_jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.showDialog)({
        title: 'Allow execution of code from CDN?',
        body: (0,_dialogs__WEBPACK_IMPORTED_MODULE_3__.formatCDNConsentDialog)(exampleModule, cdnUrl),
        buttons: [
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.okButton({
                label: 'Forbid'
            }),
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.cancelButton({
                label: 'Abort'
            }),
            _jupyterlab_apputils__WEBPACK_IMPORTED_MODULE_0__.Dialog.warnButton({
                label: 'Allow'
            })
        ],
        defaultButton: 0
    });
    switch (decision.button.label) {
        case 'Forbid':
            return 'never';
        case 'Allow':
            return 'always-insecure';
        case 'Abort':
            return 'abort-to-investigate';
        default:
            return 'awaiting-decision';
    }
}
class ImportResolver {
    constructor(_options) {
        this._options = _options;
        // no-op
    }
    set dynamicLoader(loader) {
        this._options.dynamicLoader = loader;
    }
    /**
     * Convert import to:
     *   - token string,
     *   - module assignment if appropriate module is available,
     *   - requirejs import if everything else fails
     */
    async resolve(module) {
        try {
            const tokenAndDefaultHandler = {
                get: (target, prop, receiver) => {
                    if (typeof prop !== 'string') {
                        return Reflect.get(target, prop, receiver);
                    }
                    const tokenName = `${module}:${prop}`;
                    if (this._options.tokenMap.has(tokenName)) {
                        // eslint-disable-next-line  @typescript-eslint/no-non-null-assertion
                        return this._options.tokenMap.get(tokenName);
                    }
                    // synthetic default import (without proxy)
                    if (prop === 'default' && !(prop in target)) {
                        return target;
                    }
                    return Reflect.get(target, prop, receiver);
                }
            };
            const knownModule = this._resolveKnownModule(module);
            if (knownModule !== null) {
                return new Proxy(knownModule, tokenAndDefaultHandler);
            }
            const localFile = await this._resolveLocalFile(module);
            if (localFile !== null) {
                return localFile;
            }
            const baseURL = this._options.settings.composite.requirejsCDN;
            const consent = await this._getCDNConsent(module, baseURL);
            if (!consent.agreed) {
                throw new Error(`Module ${module} requires execution from CDN but it is not allowed.`);
            }
            const externalAMDModule = await this._resolveAMDModule(module);
            if (externalAMDModule !== null) {
                return externalAMDModule;
            }
            throw new Error(`Could not resolve the module ${module}`);
        }
        catch (error) {
            handleImportError(error, module);
            throw error;
        }
    }
    async _getCDNConsent(module, cdnUrl) {
        const allowCDN = this._options.settings.composite.allowCDN;
        switch (allowCDN) {
            case 'awaiting-decision': {
                const newPolicy = await askUserForCDNPolicy(module, cdnUrl);
                if (newPolicy === 'abort-to-investigate') {
                    throw new Error('User aborted execution when asked about CDN policy');
                }
                else {
                    await this._options.settings.set('allowCDN', newPolicy);
                }
                return await this._getCDNConsent(module, cdnUrl);
            }
            case 'never':
                console.warn('Not loading the module ', module, 'as it is not a known token/module and the CDN policy is set to `never`');
                return { agreed: false };
            case 'always-insecure':
                return { agreed: true };
        }
    }
    _resolveKnownModule(module) {
        if (Object.prototype.hasOwnProperty.call(this._options.modules, module)) {
            return this._options.modules[module];
        }
        return null;
    }
    async _resolveAMDModule(module) {
        const require = this._options.requirejs.require;
        return new Promise((resolve, reject) => {
            console.log('Fetching', module, 'via require.js');
            require([module], (mod) => {
                if (!mod) {
                    reject(`Module ${module} could not be loaded via require.js`);
                }
                return resolve(mod);
            }, (error) => {
                return reject(error);
            });
        });
    }
    async _resolveLocalFile(module) {
        if (!module.startsWith('.')) {
            // not a local file, can't help here
            return null;
        }
        const serviceManager = this._options.serviceManager;
        if (serviceManager === null) {
            throw Error(`Cannot resolve import of local module ${module}: service manager is not available`);
        }
        if (!this._options.dynamicLoader) {
            throw Error(`Cannot resolve import of local module ${module}: dynamic loader is not available`);
        }
        const path = this._options.basePath;
        if (path === null) {
            throw Error(`Cannot resolve import of local module ${module}: the base path was not provided`);
        }
        const base = _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.dirname(path);
        const candidatePaths = [
            _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(base, module + '.ts'),
            _jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(base, module + '.tsx')
        ];
        if (module.endsWith('.svg')) {
            candidatePaths.push(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.join(base, module));
        }
        for (const candidatePath of candidatePaths) {
            const directory = await serviceManager.contents.get(_jupyterlab_coreutils__WEBPACK_IMPORTED_MODULE_1__.PathExt.dirname(candidatePath));
            const files = directory.content;
            const filePaths = new Set(files.map(file => file.path));
            if (filePaths.has(candidatePath)) {
                console.log(`Resolved ${module} to ${candidatePath}`);
                const file = await serviceManager.contents.get(candidatePath);
                if (candidatePath.endsWith('.svg')) {
                    return {
                        default: file.content
                    };
                }
                return await this._options.dynamicLoader(file.content);
            }
        }
        console.warn(`Could not resolve ${module}, candidate paths:`, candidatePaths);
        return null;
    }
}


/***/ }),

/***/ "./lib/transpiler.js":
/*!***************************!*\
  !*** ./lib/transpiler.js ***!
  \***************************/
/***/ ((__unused_webpack_module, __webpack_exports__, __webpack_require__) => {

__webpack_require__.r(__webpack_exports__);
/* harmony export */ __webpack_require__.d(__webpack_exports__, {
/* harmony export */   "NoDefaultExportError": () => (/* binding */ NoDefaultExportError),
/* harmony export */   "PluginTranspiler": () => (/* binding */ PluginTranspiler)
/* harmony export */ });
/* harmony import */ var typescript__WEBPACK_IMPORTED_MODULE_0__ = __webpack_require__(/*! typescript */ "webpack/sharing/consume/default/typescript/typescript");
/* harmony import */ var typescript__WEBPACK_IMPORTED_MODULE_0___default = /*#__PURE__*/__webpack_require__.n(typescript__WEBPACK_IMPORTED_MODULE_0__);

class NoDefaultExportError extends Error {
}
function isUseStrict(node) {
    return (typescript__WEBPACK_IMPORTED_MODULE_0___default().isExpressionStatement(node) &&
        typescript__WEBPACK_IMPORTED_MODULE_0___default().isStringLiteral(node.expression) &&
        node.expression.text === 'use strict');
}
class PluginTranspiler {
    constructor(options) {
        this.importFunctionName = 'require';
        this._options = options;
        if (options.compilerOptions.module) {
            throw new Error('The module setting is an implementation detail of transpiler.');
        }
    }
    /**
     * Transpile an ES6 plugin into a function body of an async function,
     * returning the plugin that would be exported as default.
     */
    transpile(code, requireDefaultExport) {
        const result = typescript__WEBPACK_IMPORTED_MODULE_0___default().transpileModule(code, {
            compilerOptions: Object.assign(Object.assign({}, this._options.compilerOptions), { module: (typescript__WEBPACK_IMPORTED_MODULE_0___default().ModuleKind.CommonJS) }),
            transformers: {
                before: requireDefaultExport
                    ? [this._requireDefaultExportTransformer()]
                    : [],
                after: [
                    this._awaitRequireTransformer(),
                    this._exportWrapperTransformer()
                ]
            }
        });
        return result.outputText;
    }
    _exportWrapperTransformer() {
        // working on output of `createImportCallExpressionCommonJS` from TypeScript
        return context => {
            return source => {
                const transpiledStatements = [...source.statements];
                const pinnedStatements = [];
                if (isUseStrict(transpiledStatements[0])) {
                    // eslint-disable-next-line  @typescript-eslint/no-non-null-assertion
                    const first = transpiledStatements.shift();
                    pinnedStatements.push(first);
                }
                return typescript__WEBPACK_IMPORTED_MODULE_0___default().factory.updateSourceFile(source, [
                    ...pinnedStatements,
                    typescript__WEBPACK_IMPORTED_MODULE_0___default().factory.createVariableStatement(undefined /* modifiers */, typescript__WEBPACK_IMPORTED_MODULE_0___default().factory.createVariableDeclarationList([
                        typescript__WEBPACK_IMPORTED_MODULE_0___default().factory.createVariableDeclaration(typescript__WEBPACK_IMPORTED_MODULE_0___default().factory.createIdentifier('exports'), undefined /* exclamationToken */, undefined /* type */, typescript__WEBPACK_IMPORTED_MODULE_0___default().factory.createObjectLiteralExpression())
                    ], (typescript__WEBPACK_IMPORTED_MODULE_0___default().NodeFlags.Const))),
                    // original statements
                    ...transpiledStatements,
                    // return `exports`
                    typescript__WEBPACK_IMPORTED_MODULE_0___default().factory.createReturnStatement(typescript__WEBPACK_IMPORTED_MODULE_0___default().factory.createIdentifier('exports'))
                ]);
            };
        };
    }
    _awaitRequireTransformer() {
        // working on output of `createImportCallExpressionCommonJS` from TypeScript
        return context => {
            const visit = node => {
                if (typescript__WEBPACK_IMPORTED_MODULE_0___default().isCallExpression(node)) {
                    const expression = node.expression;
                    if (typescript__WEBPACK_IMPORTED_MODULE_0___default().isIdentifier(expression) && expression.text === 'require') {
                        return typescript__WEBPACK_IMPORTED_MODULE_0___default().factory.createAwaitExpression(node);
                    }
                }
                return typescript__WEBPACK_IMPORTED_MODULE_0___default().visitEachChild(node, child => visit(child), context);
            };
            return source => typescript__WEBPACK_IMPORTED_MODULE_0___default().visitNode(source, visit);
        };
    }
    _requireDefaultExportTransformer() {
        return context => {
            let defaultExport = null;
            const visit = node => {
                // default export
                if (typescript__WEBPACK_IMPORTED_MODULE_0___default().isExportAssignment(node)) {
                    const hasDefaultClause = node
                        .getChildren()
                        .some(node => node.kind === (typescript__WEBPACK_IMPORTED_MODULE_0___default().SyntaxKind.DefaultKeyword));
                    if (hasDefaultClause) {
                        defaultExport = node.expression;
                    }
                    else {
                        console.warn('Export assignment without default keyword not supported: ' +
                            node.getText(), node);
                    }
                }
                return typescript__WEBPACK_IMPORTED_MODULE_0___default().visitEachChild(node, child => visit(child), context);
            };
            return source => {
                const traveresed = typescript__WEBPACK_IMPORTED_MODULE_0___default().visitNode(source, visit);
                if (!defaultExport) {
                    throw new NoDefaultExportError('Default export not found');
                }
                return traveresed;
            };
        };
    }
}


/***/ })

}]);
//# sourceMappingURL=lib_index_js.c86e055e8ccff1c4543c.js.map