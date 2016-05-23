define(['jquery'], function($) {
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
                if ($(window).scrollTop() > this.offset) {
                    this.button.fadeIn('medium');
                } else {
                    this.button.fadeOut('medium');
                }
            });
        }
    }

    return new ScrollTopExport(window, 'body');
});
