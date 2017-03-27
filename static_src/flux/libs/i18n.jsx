/**
 * --------------------------------------------------------------------------
 * Aprigi: i18n library for React
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import i18n from 'i18next';

i18n.init({
    lng: window.location.pathname.split('/')[1] || 'en',
    debug: false,
    ns: [
        'common'
    ],
    defaultNS: 'common',
    nsSeparator: '.',
    resources: {
        vi: {
            common: {
                appMeta: 'Dành tặng cô gái tháng Tư của tôi, from naa with love',
                savings: 'Tiết kiệm',
                expenses: 'Chi tiêu',
                logout: 'Đăng xuất',
                login: 'Đăng nhập'
            }
        },
        en: {
            common: {
                appMeta: 'The app for my April girl, from naa with love',
                savings: 'Savings',
                expenses: 'Expenses',
                logout: 'Logout',
                login: 'Login'
            }
        }
    }
});

export default i18n;
