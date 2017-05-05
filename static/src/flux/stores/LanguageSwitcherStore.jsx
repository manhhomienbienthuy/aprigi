/**
 * --------------------------------------------------------------------------
 * Aprigi: LanguageSwitcherStore
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import {EventEmitter} from 'events';
import Dispatcher from '../dispatcher/Dispatcher';
import {LanguageSwitcherConstants as Const} from '../constants/LanguageSwitcherConstants';

class LanguageSwitcherStore extends EventEmitter {
    constructor() {
        super();

        this.store = {
            availableLanguages: [
                {code: 'en', name: 'English'},
                {code: 'vi', name: 'Tiếng Việt'}
            ],
            currentLanguage: window.location.pathname.split('/')[1] || 'en'
        };

        this.dispatchToken = Dispatcher.register((action) => {
            switch(action.type) {
                case Const.CHANGE_LANGUAGE:
                    if (this.store.currentLanguage !== action.language) {
                        this._changeLanguage(action.language);
                        this._emitChange();
                    }
                    break;
            }
        });
    }

    get all() {
        return this.store;
    }

    _emitChange() {
        this.emit(Const.CHANGE_EVENT);
    }

    addListener(callback) {
        this.on(Const.CHANGE_EVENT, callback);
    }

    _changeLanguage(newLanguage) {
        this.store.currentLanguage = newLanguage;
    }
}

export default new LanguageSwitcherStore(Dispatcher);
