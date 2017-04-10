/**
 * --------------------------------------------------------------------------
 * Aprigi: LanguageSwitcher component
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import React from 'react';
import {LanguageSwitcherAction as Action} from '../actions/LanguageSwitcherAction';
import Store from '../stores/LanguageSwitcherStore';

export default class LanguageSwitcher extends React.Component {
    constructor(props) {
        super(props);
        this.state = Store.all;
    }

    componentDidMount() {
        Store.addListener(() => {
            this.setState(Store.all);
        });
    }

    componentDidUpdate() {
        Action.submitForm();
    }

    onClickHandler(event, languageCode) {
        event.preventDefault();
        Action.changeLanguage(languageCode);
    }

    render() {
        const languageLinks = this.state.availableLanguages.map((language) => {
            return (
                <li key={language.code}>
                    <a
                        href="#!"
                        onClick={(e) => this.onClickHandler(e, language.code)}>
                        {language.name} ({language.code})
                    </a>
                </li>
            );
        });

        return (
            <ul>
                <input
                    name="language"
                    type="hidden"
                    value={this.state.currentLanguage}
                />
                <li><i className='apricon apricon-globe'></i></li>
                {languageLinks}
            </ul>
        );
    }
}
