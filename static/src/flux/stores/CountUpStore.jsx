/**
 * --------------------------------------------------------------------------
 * Aprigi: CountUpStore
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'user strict';

import {EventEmitter} from 'events';
import Dispatcher from '../dispatcher/Dispatcher';
import {CountUpConstants as Const} from '../constants/CountUpConstants';
import {timeDiff} from '../libs/datetime';

class CountUpStore extends EventEmitter {
    constructor() {
        super();

        this.UPDATABLE_ATTRS = ['seconds', 'minutes', 'hours', 'days', 'weeks'];

        this.store = {
            startTime: '2013/01/01'
        };

        this._updateStore();
        setInterval(this._countUp.bind(this), 1000);
    }

    get all() {
        return this.store;
    }

    addListener(callback) {
        this.on(Const.CHANGE_EVENT, callback);
    }

    _emitChange() {
        this.emit(Const.CHANGE_EVENT);
    }


    _updateStore() {
        const countDiff = timeDiff(new Date(this.store.startTime), new Date());
        this.UPDATABLE_ATTRS.forEach((propName) => {
            this.store[propName] = countDiff[propName];
        });
    }

    _countUp() {
        this._updateStore();
        this._emitChange();
    }
}

export default new CountUpStore(Dispatcher);
