'use strict';

define(['jquery'], ($) => {
    class LanguageSwitcherExport {
        constructor(switcher, form) {
            this.switcher = $(switcher);
            this.form = $(form);
            this.init();
        }

        init() {
            this.switcher.on('click', 'li a', (event) => {
                event.preventDefault();
                var $target = $(event.target);
                if ($target.attr('class') !== 'current') {
                    this.form.find('#language').val($target.data('language'));
                    this.form.submit();
                }
            });
        }
    }

    return new LanguageSwitcherExport('.language-switcher ul',
        '.language-switcher form');
});
