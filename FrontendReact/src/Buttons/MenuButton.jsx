import React, { Component } from "react"
import './Button.css'

class MenuButton extends Component {
    render() {
        return (
            <div className={"inline"}>
                <div className={'button_container'}>
                    <button type={"button"} className={"button"}>
                        {this.props.text}
                    </button>
                </div>
            </div>
        )
    }
}

export default MenuButton