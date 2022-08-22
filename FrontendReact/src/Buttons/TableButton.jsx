import React from "react"
import './Button.css'

export default props => (
    <button type={"button"}
        className={`tableButtonDefault ${props.text === "uploaded" ? "tableButtonUploaded" : ""} ${props.text === "processed" ? "tableButtonProcessed" : ""} shadow`}
        onClick={props.onClick}>
        {props.text}
    </button>
)

