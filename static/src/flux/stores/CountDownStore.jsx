/**
 * --------------------------------------------------------------------------
 * Aprigi: CountDownStore
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import {EventEmitter} from 'events';
import Dispatcher from '../dispatcher/Dispatcher';
import {CountDownConstants as Const} from '../constants/CountDownConstants';
import {timeDiff} from '../libs/datetime';

class CountDownStore extends EventEmitter {
    constructor() {
        super();

        this.UPDATABLE_ATTRS = ['seconds', 'minutes', 'hours', 'days', 'weeks'];

        this.store = {
            endTime: (new Date().getFullYear() + 1) + '/01/01'
        };

        this._updateStore();
        setInterval(this._countDown.bind(this), 1000);
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
        const countDiff = timeDiff(new Date(), new Date(this.store.endTime));
        this.UPDATABLE_ATTRS.forEach((propName) => {
            this.store[propName] = countDiff[propName];
        });
        this._paddingZeros();
    }

    _paddingZeros() {
        this.UPDATABLE_ATTRS.forEach((propName) => {
            this.store[propName] = ('0' + this.store[propName]).slice(-2);
        });
    }

    _countDown() {
        this._updateStore();
        this._emitChange();
    }

}

export default new CountDownStore(Dispatcher);
