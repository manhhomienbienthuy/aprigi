/**
 * --------------------------------------------------------------------------
 * Aprigi: ScrollToTopAction
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import Dispatcher from '../dispatcher/Dispatcher';
import {ScrollToTopConstants as Const} from '../constants/ScrollToTopConstants';

export const ScrollToTopAction = {
    toggleHidden() {
        Dispatcher.dispatch({
            type: Const.TOGGLE_HIDDEN
        });
    }
};
