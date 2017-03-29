/**
 * --------------------------------------------------------------------------
 * Aprigi: CountDownStore
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'user strict';

import {EventEmitter} from 'events';
import Dispatcher from '../dispatcher/Dispatcher';
import {CountDownConstants as Const} from '../constants/CountDownConstants';

class CountDownStore extends EventEmitter {
    constructor() {
        super();

        this.store = {
            endTime: (new Date().getFullYear() + 1) + '/01/01'
        };

        this._calculateCountDown();
        setInterval(this._countDown.bind(this), 1000);
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

    _countDown() {
        this._calculateCountDown();
        this._emitChange();
    }

    _calculateCountDown() {
        this.store.total = Date.parse(this.store.endTime) - (new Date());
        this.store.seconds = Math.floor((this.store.total / 1000) % 60);
        this.store.minutes = Math.floor((this.store.total / 1000 / 60) % 60);
        this.store.hours = Math.floor((this.store.total / (1000 * 60 * 60)) % 24);
        this.store.days = Math.floor(this.store.total / (1000 * 60 * 60 * 24) % 7);
        this.store.weeks = Math.floor(this.store.total / (1000 * 60 * 60 * 24 * 7));
        this._paddingZeros();
    }

    _paddingZeros() {
        ['seconds', 'minutes', 'hours', 'days', 'weeks'].forEach((propName) => {
            this.store[propName] = ('0' + this.store[propName]).slice(-2);
        });
    }
}

export default new CountDownStore(Dispatcher);
