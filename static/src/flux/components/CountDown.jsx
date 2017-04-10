/**
 * --------------------------------------------------------------------------
 * Aprigi: Countdown component
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import React from 'react';
import Store from '../stores/CountDownStore';
import i18n from '../libs/i18n';

export default class CountDown extends React.Component {
    constructor(props) {
        super(props);

        this.state = Store.all;
    }

    componentDidMount() {
        Store.addListener(() => {
            this.setState(Store.all);
        });
    }

    render () {
        return (
            <div className="countdown-container">
                <p className="small-text">{i18n.t('countdown.title')}</p>

                <div>
                    <span className="days">{this.state.weeks}</span>
                    <div className="small-text">{i18n.t('Weeks')}</div>
                </div>

                {' '}
                <div>
                    <span className="days">{this.state.days}</span>
                    <div className="small-text">{i18n.t('Days')}</div>
                </div>

                {' '}
                <div>
                    <span className="hours">{this.state.hours}</span>
                    <div className="small-text">{i18n.t('Hours')}</div>
                </div>

                {' '}
                <div>
                    <span className="minutes">{this.state.minutes}</span>
                    <div className="small-text">{i18n.t('Minutes')}</div>
                </div>

                {' '}
                <div>
                    <span className="seconds">{this.state.seconds}</span>
                    <div className="small-text">{i18n.t('Seconds')}</div>
                </div>
            </div>
        );
    }
}
