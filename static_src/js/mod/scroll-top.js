/**
 * --------------------------------------------------------------------------
 * Aprigi: Back-to-top button handler
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

define(['jquery'], ($) => {
    class ScrollTopExport{
        constructor(window, body) {
            this.body = $(body);
            this.window = $(window);
            this.offset = this.window.height() * 0.75;
            this.init();
        }

        init() {
            this.button = $('<a href="#top" class="back-to-top"><i class="fa fa-chevron-up"></i></a>');
            this.body.append(this.button);

            this.window.scroll(() => {
                if (this.window.scrollTop() > this.offset) {
                    this.button.fadeIn('medium');
                } else {
                    this.button.fadeOut('medium');
                }
            });
        }
    }

    return new ScrollTopExport(window, 'body');
});
