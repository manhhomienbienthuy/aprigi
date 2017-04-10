/**
 * --------------------------------------------------------------------------
 * Aprigi: Doms library for React
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

export function hasClass(className) {
     //return a boolean
    return !!document.getElementsByClassName(className).length;
}

export function getPageHeight() {
    const body = document.body;
    const html = document.documentElement;

    return Math.max(body.scrollHeight, body.offsetHeight,
                    html.clientHeight, html.scrollHeight,
                    html.offsetHeight);
}

export function scrollTop() {
    const html = document.documentElement;

    return Math.max(window.scrollY, html.scrollTop);
}
