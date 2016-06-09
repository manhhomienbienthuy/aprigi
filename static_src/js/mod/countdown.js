/**
 * --------------------------------------------------------------------------
 * Aprigi: Countdown
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

define(['jquery', 'lodash', 'jquery.countdown'], ($, _) => {
    class CountdownExport {
        constructor(countdown, template) {
            this.countdown = $(countdown);
            this.template = _.template($(template).html());
            this.currDate = '00:00:00:00:00';
            this.nextDate = '00:00:00:00:00';
            this.parser = /([0-9]{2})/gi;
            this.target = this.countdown.attr('for');
            if (!this.target) {
                this.target = (new Date().getFullYear() + 1) + '/01/01';
            }
            this.labels = this.countdown.data('labels');
            if (!this.labels) {
                this.labels = ['weeks', 'days', 'hours', 'minutes', 'seconds'];
            }
            this.init();
        }

        init() {
            // Build the layout
            var initData = this.strfobj(this.currDate);
            this.labels.forEach((label) => {
                this.countdown.append(this.template({
                    curr: initData[label],
                    next: initData[label],
                    label: label
                }));
            });

            // Starts the countdown
            this.countdown.countdown(this.target, (event) => {
                var newDate = event.strftime('%w:%d:%H:%M:%S'),
                    data;
                if (newDate !== this.nextDate) {
                    this.currDate = this.nextDate;
                    this.nextDate = newDate;
                    // Setup the data
                    data = {
                        'curr': this.strfobj(this.currDate),
                        'next': this.strfobj(this.nextDate)
                    };

                    // Apply the new values to each node that changed
                    this.diff(data.curr, data.next).forEach((label) => {
                        var selector = '.%s'.replace(/%s/, label),
                            $node = this.countdown.find(selector);
                        // Update the node
                        $node.removeClass('flip');
                        $node.find('.curr').text(data.curr[label]);
                        $node.find('.next').text(data.next[label]);
                        // Wait for a repaint to then flip
                        _.delay(($node) => {
                            $node.addClass('flip');
                        }, 50, $node);
                    });
                }
            });
        }

        // Parse countdown string to an object
        strfobj(str) {
            var parsed = str.match(this.parser),
                obj = {};
            this.labels.forEach((label, i) => {
                obj[label] = parsed[i];
            });
            return obj;
        }

        // Return the time components that diffs
        diff(obj1, obj2) {
            var diff = [];
            this.labels.forEach((key) => {
                if (obj1[key] !== obj2[key]) {
                    diff.push(key);
                }
            });
            return diff;
        }
    }

    return new CountdownExport('#countdown', '#countdown-template');
});
