/**
 * --------------------------------------------------------------------------
 * Aprigi: NavigationAction
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import Dispatcher from '../dispatcher/Dispatcher';
import {NavigationConstants as Const} from '../constants/NavigationConstants';

export const NavigationAction = {
    toggleClass() {
        Dispatcher.dispatch({
            type: Const.TOGGLE_CLASS
        });
    }
};
