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

    componentWillUnMount() {
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
        if (getPageHeight() < window.innerHeight * 2) {
            return null;
        }

        let className = 'back-to-top';
        className += this.state.hidden ? ' hidden' : '';

        return (
            <a href="#top"
                className={className}
                onClick={this.onClickHandler}>
                <i className="fa fa-chevron-up"></i>
            </a>
        );
    }
}
