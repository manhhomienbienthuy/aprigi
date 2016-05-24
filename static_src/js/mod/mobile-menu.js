define(['jquery'], ($) => {
    class MobileMenuExport {
        constructor(menu) {
            this.menu = $(menu);
            this.init();
        }

        init() {
            this.menu.addClass('mobile-navigation');
            this.button = $('<div class="navigation-button"><i class="fa fa-bars"></i></div>');
            this.button.insertBefore(this.menu);
            this.button.on('click', () => {
                this.menu.toggleClass('active');
                this.button.toggleClass('active');
            });
        }
    }

    return new MobileMenuExport('header .navigation');
});
