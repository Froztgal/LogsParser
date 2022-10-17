import React, { Component } from "react"
import axios from "axios"
import { APP_API_URL } from "../static/config"
import Button from "../Buttons/Button"
import './Form.css'

const images = [
    require("../static/upload_icon.png"),
    require("../static/ready_icon.png"),
    require("../static/uploded_icon.png")
]

class Form extends Component {
    constructor(props) {
        super(props)
        this.state = {
            files: null,
            image: 0
        }
    }

    // Prevent default
    myPreventDefault = (e) => {
        e.preventDefault()
    }

    // On add files
    handleFileSelect = (e) => {
        let files = e.target.files

        this.setState({
            files: files,
            image: 1
        })
    }

    // On drag and drop
    handleFilesDrop = (e) => {
        e.preventDefault()

        let files = []
        const items = e.dataTransfer.items

        if (items) {
            for (const item of items)
                if (item.kind === 'file')
                    files.push(item.getAsFile())
        }

        this.setState({
            files: files,
            image: 1
        })
    }

    // File Submit Handler
    handleSubmitFile = () => {

        if (this.state.files !== null) {
            let formData = new FormData()

            for (const item of this.state.files)
                formData.append('files', item)

            axios.post(
                APP_API_URL + "upload_files/",
                formData,
                {
                    headers: {
                        "Content-type": "multipart/form-data",
                    },
                }
            )
            .then(function (response) {
                console.log(response.status, response.data)
                
            })

            this.setState({image: 2})
        }
    }

    render() {
        return (
            <div>
                <form>

                    <h1>Выберите файлы</h1>

                    <label htmlFor="file" onDrop={this.handleFilesDrop} onDragOver={this.myPreventDefault}>
                        <input
                            id="file"
                            type="file"
                            onChange={this.handleFileSelect}
                            multiple
                            hidden />
                        <div className="ImageHolder">
                            <img src={images[this.state.image]} style={{ width: "350px" }}/>
                        </div>
                    </label>

                    <Button text="Выгрузить файлы" onClick={this.handleSubmitFile} type="submit"></Button>

                </form>
            </div>
        )
    }
}

export default Form