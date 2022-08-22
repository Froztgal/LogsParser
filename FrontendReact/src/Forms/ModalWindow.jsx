import React, { Component } from "react"
import ButtonX from "../Buttons/ButtonX"

class ModalWindow extends Component {
    state = {
        modalVisible: this.props.visibility
    }

    changeVisibility = () => {
        this.props.closeFunction()
    }

    changeVisibilityEscape = (event) => {
        if (event.key === "Escape") {
            this.props.closeFunction()
        }
    }

    componentWillReceiveProps(props) {
        this.setState({ modalVisible: props.visibility })
    }

    componentDidMount() {
        document.addEventListener("keydown", this.changeVisibilityEscape, false)
    }

    render() {
        const { modalVisible } = this.state

        if (modalVisible) {
            return (
                <div className="modalArea">
                    <div className="modalForm">
                        <div className="modalButtonHolder">
                            <ButtonX onClick={this.changeVisibility}></ButtonX>
                        </div>
                        {this.props.children}
                    </div>
                </div>
            )
        }
    }
}

export default ModalWindow