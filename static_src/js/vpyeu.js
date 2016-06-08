/*!
 * Script for Aprigi
 * Description: The app for my April girl
 * Copyright (C) 2016 Aprigi
 * This file is distributed under the same license as the aprigi package.
 * Anh Tranngoc <naa@sfc.wide.ad.jp>, 2016.
 */

'use strict';

requirejs.config({
    paths: {
        'jquery': '//ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min',
        'mobile-menu': 'mod/mobile-menu',
        'scroll-top': 'mod/scroll-top',
        'language-switch': 'mod/language-switch'
    }
});

define(() => {
    var mods = ['mobile-menu', 'language-switch'];

    function getPageHeight() {
        var body = document.body;
        var html = document.documentElement;

        return Math.max(body.scrollHeight, body.offsetHeight,
                        html.clientHeight, html.scrollHeight,
                        html.offsetHeight);
    }

    if (getPageHeight() > window.innerHeight * 2) {
        mods.push('scroll-top');
    }

    requirejs(mods);
});
