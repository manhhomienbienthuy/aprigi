/**
 * --------------------------------------------------------------------------
 * Aprigi: Navigation component
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import React from 'react';
import {NavigationAction as Action} from '../actions/NavigationAction';
import Store from '../stores/NavigationStore';
import i18n from '../libs/i18n';

export default class Navigation extends React.Component {
    constructor(props) {
        super(props);
        this.state = Store.all;
    }

    componentDidMount() {
        Store.addListener(() => {
            this.setState(Store.all);
        });
    }

    onClickHandler() {
        Action.toggleClass();
    }

    renderAccountLink() {
        const logoutLink = `/accounts/logout?next=${window.location.pathname}`;
        const loginLink = `/accounts/login?next=${window.location.pathname}`;
        if (this.state.loggedIn) {
            return (
                <li><a href={logoutLink}>
                  {i18n.t('logout')}
                </a></li>
            );
        } else {
            return (
                <li><a href={loginLink}>
                    {i18n.t('login')}
                </a></li>
            );
        }

    }

    render() {
        let menuClassName = 'navigation';
        if (this.state.showMenu) {
            menuClassName += ' active';
        }

        let savingsClassName;
        if (window.location.pathname.indexOf('savings') !== -1) {
            savingsClassName = 'active';
        }

        let expensesClassName;
        if (window.location.pathname.indexOf('expenses') !== -1) {
            expensesClassName = 'active';
        }

        return (
            <div className='container'>
                <a
                    href={window.location.pathname.slice(0, 4)}
                    className='logo'>
                    Aprigi
                </a>
                <p className='meta'>
                    {i18n.t('appMeta')}
                </p>

                <div
                    className='navigation-button'
                    onClick={this.onClickHandler}>
                    <i className='apricon apricon-bars'></i>
                </div>

                <div className={menuClassName}>
                    <ul>
                        <li className={savingsClassName}>
                            <a href='/savings'>{i18n.t('savings')}</a>
                        </li>
                        <li className={expensesClassName}>
                            <a href='/expenses'>{i18n.t('expenses')}</a>
                        </li>
                        {this.renderAccountLink()}
                    </ul>
                </div>
            </div>
        );
    }
}
