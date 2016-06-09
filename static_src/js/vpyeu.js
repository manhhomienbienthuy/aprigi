/*!
 * Script for Aprigi
 * Description: The app for my April girl
 * Copyright (C) 2016 Aprigi
 * This file is distributed under the same license as the aprigi package.
 * Anh Tranngoc <naa@sfc.wide.ad.jp>, 2016.
 */

'use strict';

requirejs.config({
    shim: {
        'jquery': [],
        'lodash': [],
        'jquery.countdown': ['jquery']
    },
    paths: {
        'jquery': '//ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min',
        'jquery.countdown': '//cdnjs.cloudflare.com/ajax/libs/jquery.countdown/2.1.0/jquery.countdown.min',
        'lodash': '//cdnjs.cloudflare.com/ajax/libs/lodash.js/4.13.1/lodash.min',
        'mobile-menu': 'mod/mobile-menu',
        'scroll-top': 'mod/scroll-top',
        'language-switch': 'mod/language-switch',
        'countdown': 'mod/countdown'
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

    function hasClass(className) {
         //return a boolean
        return !!document.getElementsByClassName(className).length;
    }

    if (getPageHeight() > window.innerHeight * 2) {
        mods.push('scroll-top');
    }

    if (hasClass('countdown')) {
        mods.push('countdown');
    }

    requirejs(mods);
});
