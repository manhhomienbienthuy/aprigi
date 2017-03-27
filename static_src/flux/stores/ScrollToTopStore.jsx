/**
 * --------------------------------------------------------------------------
 * Aprigi: ScrollToTopStore
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'user strict';

import {EventEmitter} from 'events';
import Dispatcher from '../dispatcher/Dispatcher';
import {ScrollToTopConstants as Const} from '../constants/ScrollToTopConstants';

class ScrollToTopStore extends EventEmitter {
    constructor() {
        super();

        this.store = {
            hidden: true
        };

        this.dispatchToken = Dispatcher.register((action) => {
            switch(action.type) {
                case Const.TOGGLE_HIDDEN:
                    this._toggleHidden();
                    break;
            }

            this._emitChange();
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

    _toggleHidden() {
        this.store.hidden = !this.store.hidden;
    }
}

export default new ScrollToTopStore(Dispatcher);
