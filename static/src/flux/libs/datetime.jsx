/**
 * --------------------------------------------------------------------------
 * Aprigi: Datetime library for React
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

export function timeDiff(startTime, stopTime) {
    const total = (stopTime - startTime) / 1000;
    return {
        seconds: total % 60 | 0,
        minutes: total / 60 % 60 | 0,
        hours: total / 60 / 60 % 24 | 0,
        days: total / 60 / 60 / 24 % 7 | 0,
        weeks: total / 60 / 60 / 24 / 7 | 0
    };
}
