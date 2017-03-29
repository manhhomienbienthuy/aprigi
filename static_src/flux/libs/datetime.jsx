/**
 * --------------------------------------------------------------------------
 * Aprigi: Datetime library for React
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

export function timeDiff(startTime, stopTime) {
    const total = stopTime - startTime;
    return {
        seconds: Math.floor((total / 1000) % 60),
        minutes: Math.floor((total / 1000 / 60) % 60),
        hours: Math.floor((total / (1000 * 60 * 60)) % 24),
        days: Math.floor((total / (1000 * 60 * 60 * 24)) % 7),
        weeks: Math.floor(total / (1000 * 60 * 60 * 24 * 7))
    };
}
