import React, { Component } from "react"
import { APP_API_URL } from "../static/config"
import Button from "../Buttons/Button"
import './Form.css'
import axios from "axios"


class TimeRequest extends Component {
    constructor(props) {
        super(props)
        this.state = {
            timeStart: '00:00',
            timeEnd: '23:59'
        }
    }

    handleChange = (e) => {
        // console.log(e.target.value)
        if (e.target.id === "startTime") {
            this.setState({ timeStart: e.target.value })
        }
        else {
            this.setState({ timeEnd: e.target.value })
        }
    }

    handleDownloadErrors = () => {
        axios({
            url: APP_API_URL + "dashboard/download_errors/" + this.props.date,
            method: 'get',
            params: {
                start: this.state.timeStart,
                end: this.state.timeEnd
            }
        })
            .then(res => {
                console.log(res)
                const url = window.URL.createObjectURL(new Blob([res.data]))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', 'errors_' + this.props.date + '.txt')
                document.body.appendChild(link)
                link.click()
            })
            .catch(err => {
                console.log(`Error` + err)
                alert(err.response.data.detail)
            })
    }

    render() {
        return (
            <>
                <h1 style={{ color: "#FFFFFF" }}>Временные метки</h1>
                <form className="timeForm">
                    <label htmlFor="startTime">
                        <input
                            onChange={this.handleChange}
                            className="inputTime"
                            type="time"
                            id="startTime"
                            value={this.state.timeStart}
                            required
                        />
                        Время начала полета
                    </label>
                    <br></br>
                    <label htmlFor="endTime">
                        <input
                            onChange={this.handleChange}
                            className="inputTime"
                            type="time"
                            id="endTime"
                            value={this.state.timeEnd}
                            required
                        />
                        Время конца полета
                    </label>
                </form>
                <Button text="Скачать errors" onClick={this.handleDownloadErrors}></Button>
            </>
        )
    }
}

export default TimeRequest