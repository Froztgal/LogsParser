import React from "react"
import './Button.css'

export default props => (
    <button
        type={"button"}
        className={"XButton"}
        onClick={props.onClick}>
        X
    </button>
)

