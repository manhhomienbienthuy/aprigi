/**
 * --------------------------------------------------------------------------
 * Aprigi: Language switcher
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

define(['jquery'], ($) => {
    class LanguageSwitchExport {
        constructor(switcher, form) {
            this.switcher = $(switcher);
            this.form = $(form);
            this.init();
        }

        init() {
            $(() => {
                this.switcher.on('click', 'li a', (event) => {
                    event.preventDefault();
                    var $target = $(event.target);
                    if ($target.attr('class') !== 'current') {
                        var targetLanguage = $target.data('language');
                        var currentNext = this.form.find('#next').val();
                        this.form.find('#language').val(targetLanguage);
                        this.form.find('#next').val('/' + targetLanguage +
                                                    currentNext);
                        this.form.submit();
                    }
                });
            });
        }
    }

    return new LanguageSwitchExport('.language-switcher ul',
        '.language-switcher form');
});
