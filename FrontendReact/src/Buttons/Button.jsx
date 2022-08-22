import React, { Component } from "react"
import './Button.css'

class Button extends Component {
    constructor(props) {
        super(props)
        this.state = { Pressed: false }
        this.handleClick = this.handleClick.bind(this)
    }

    handleClick() {
        this.setState({ Pressed: true })
        this.props.onClick()
    }

    render() {
        const button = <div className={`button_container ${this.state.Pressed ? 'button_container_pressed' : ''}`}>
            <button
                type="button"
                className={"button"}
                onClick={this.handleClick}>
                {this.props.text}
            </button>
        </div >

        return (
            <div className="inline">
                {button}
            </div>
        )
    }
}

export default Button