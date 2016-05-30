'use strict';

requirejs.config({
    paths: {
        'jquery': '//ajax.googleapis.com/ajax/libs/jquery/2.2.2/jquery.min',
        'mobile-menu': 'mod/mobile-menu',
        'scroll-top': 'mod/scroll-top',
        'language-switcher': 'mod/language-switcher'
    }
});

define(() => {
    var mods = ['mobile-menu', 'language-switcher'];

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
