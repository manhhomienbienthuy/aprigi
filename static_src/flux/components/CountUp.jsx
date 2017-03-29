/**
 * --------------------------------------------------------------------------
 * Aprigi: CountUp component
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import React from 'react';
import Store from '../stores/CountUpStore';
import i18n from '../libs/i18n';

export default class CountUp extends React.Component {
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
            <div>
                {this.state.weeks} {i18n.t('Weeks')}
                {' '}
                {this.state.days} {i18n.t('Days')}
                {' '}
                {this.state.hours} {i18n.t('Hours')}
                {' '}
                {this.state.minutes} {i18n.t('Minutes')}
                {' '}
                {this.state.seconds} {i18n.t('Seconds')}
            </div>
        );
    }
}
