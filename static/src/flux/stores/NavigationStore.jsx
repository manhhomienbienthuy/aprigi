/**
 * --------------------------------------------------------------------------
 * Aprigi: NavigationStore
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import {EventEmitter} from 'events';
import Dispatcher from '../dispatcher/Dispatcher';
import {NavigationConstants as Const} from '../constants/NavigationConstants';
import {hasClass} from '../libs/doms';

class NavigationStore extends EventEmitter {
    constructor() {
        super();

        this.store = {
            showMenu: false,
            buttonActive: false,
            loggedIn: hasClass('logged-in')
        };

        this.dispatchToken = Dispatcher.register((action) => {
            switch(action.type) {
                case Const.TOGGLE_CLASS:
                    this._toggleClass();
                    this._emitChange();
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

    _toggleClass() {
        this.store.showMenu = !this.store.showMenu;
        this.buttonActive = !this.buttonActive;
    }
}

export default new NavigationStore(Dispatcher);
