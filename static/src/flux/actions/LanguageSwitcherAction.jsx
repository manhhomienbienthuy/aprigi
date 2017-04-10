/**
 * --------------------------------------------------------------------------
 * Aprigi: LanguageSwitcherAction
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import Dispatcher from '../dispatcher/Dispatcher';
import {LanguageSwitcherConstants as Const} from '../constants/LanguageSwitcherConstants';

export const LanguageSwitcherAction = {
    changeLanguage(languageCode) {
        Dispatcher.dispatch({
            type: Const.CHANGE_LANGUAGE,
            language: languageCode
        });
    },
    submitForm() {
        const forms = document.getElementsByTagName('form');
        const languageForm = forms[forms.length - 1];
        languageForm.submit();
    }
};
