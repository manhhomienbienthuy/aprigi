/**
 * --------------------------------------------------------------------------
 * Aprigi: ScrollToTop component
 * This file is distributed under the same license as the aprigi package.
 * --------------------------------------------------------------------------
 */

'use strict';

import React from 'react';
import {ScrollToTopAction as Action} from '../actions/ScrollToTopAction';
import Store from '../stores/ScrollToTopStore';
import {getPageHeight, scrollTop} from '../libs/doms';

export default class ScrollToTop extends React.Component {
    constructor(props) {
        super(props);
        this.offset = window.innerHeight * 0.75;
        this.onScrollHandler = this.onScrollHandler.bind(this);
        this.state = Store.all;
    }

    componentDidMount() {
        Store.addListener(() => {
            this.setState(Store.all);
        });

        window.addEventListener('scroll', this.onScrollHandler);
    }

    componentWillUnmount() {
        window.removeEventListener('scroll', this.onScrollHandler);
    }

    onScrollHandler() {
        let hidden;

        if (scrollTop() > this.offset) {
            hidden = false;
        } else {
            hidden = true;
        }

        if (hidden !== this.state.hidden) {
            Action.toggleHidden();
        }
    }

    onClickHandler(event) {
        event.preventDefault();
        window.scrollTo(0, 0);
    }


    render() {
        if (this.state.hidden || getPageHeight() < window.innerHeight * 2) {
            return null;
        }

        return (
            <a href="#top"
                className="back-to-top"
                onClick={this.onClickHandler}>
                <i className="apricon apricon-chevron-up"></i>
            </a>
        );
    }
}
