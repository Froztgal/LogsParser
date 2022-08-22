import React, { Component } from "react"
import axios from "axios"
import { APP_API_URL } from "../static/config"
import UploadIcon from "../static/uplod_icon.png"
import ReadyIcon from "../static/ready_icon.png"
import UploadedIcon from "../static/uploded_icon.png"
import Button from "../Buttons/Button"
import './Form.css'

class Form extends Component {
    constructor(props) {
        super(props)
        this.state = {
            files: null,
            image: UploadIcon
        }
    }

    // Prevent default
    myPreventDefault = (e) => {
        e.preventDefault()
    }

    // On add files
    handleFileSelect = (e) => {
        let files = e.target.files
        console.log(files)

        this.setState({
            files: files,
            image: ReadyIcon
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
        console.log(files)

        this.setState({
            files: files,
            image: ReadyIcon
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
                    this.setState({image: UploadedIcon})
                    console.log(response.status, response.data)
                })
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
                            <img src={this.image} style={{ width: "350px" }}/>
                        </div>
                    </label>

                    <Button text="Выгрузить файлы" onClick={this.handleSubmitFile} type="submit"></Button>

                </form>
            </div>
        )
    }
}

export default Form