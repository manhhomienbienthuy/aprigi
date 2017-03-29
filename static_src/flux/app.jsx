/*!
 * Script for Aprigi
 * Description: The app for my April girl
 * Copyright (C) 2016-present Anh Tranngoc
 * This file is distributed under the same license as the aprigi package.
 * Anh Tranngoc <naa@sfc.wide.ad.jp>, 2016.
 */

'use strict';

import React from 'react';
import ReactDOM from 'react-dom';

import ScrollToTop from './components/ScrollToTop';
import Navigation from './components/Navigation';
import LanguageSwitcher from './components/LanguageSwitcher';
import CountDown from './components/CountDown';

ReactDOM.render(
    <ScrollToTop />,
    document.getElementById('back-to-top-button')
);

ReactDOM.render(
    <Navigation />,
    document.getElementById('top')
);

ReactDOM.render(
    <LanguageSwitcher />,
    document.getElementById('js-language-switcher')
);

if (document.getElementsByClassName('countdown').length > 0) {
    ReactDOM.render(
        <CountDown />,
        document.getElementsByClassName('countdown')[0]
    );
}
