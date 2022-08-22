import React, { Component } from "react"
import axios from "axios"
import { APP_API_URL } from "../static/config"
import Button from "../Buttons/Button"
import './Form.css'
import Waiter from "../static/Waiter"


class Coordinates extends Component {
    constructor(props) {
        super(props)
        this.state = {
            coordinates: null
        }
    }

    componentDidMount() {
        axios.get(APP_API_URL + "dashboard/get_base_time/" + this.props.date)
            .then(res => {
                console.log(res)
                this.setState({
                    coordinates: res.data
                })
            })
            .catch(err => {
                console.log(`Error` + err)
            })
    }

    handleChange = (e) => {
        let coord = this.state.coordinates
        coord[e.target.id] = e.target.value
        this.setState({
            coordinates: coord
        })
    }

    handleDownloadPlot = () => {
        axios({
            url: APP_API_URL + "dashboard/download_plot/" + this.props.date,
            method: 'post',
            data: {
                timestamps: this.state.coordinates
            }
        })
            .then(res => {
                console.log(res)
                const url = window.URL.createObjectURL(new Blob([res.data]))
                const link = document.createElement('a')
                link.href = url
                link.setAttribute('download', 'analize_' + this.props.date + '.html')
                document.body.appendChild(link)
                link.click()
            })
            .catch(err => {
                console.log(`Error` + err)
                alert(err.response.data.detail)
            })
    }

    render() {
        if (!this.state.coordinates) {
            return <Waiter></Waiter>
        }
        else {
            return (
                <>
                    <h1 style={{ color: "#FFFFFF" }}>Временные метки</h1>
                    <form className="timeForm">
                        {Object.entries(this.state.coordinates).map(
                            ([key, value]) => {
                                return (
                                    <>
                                        <label htmlFor={key} key={key}>
                                            <input
                                                onChange={this.handleChange}
                                                className="inputTime"
                                                type="time"
                                                id={key}
                                                value={value}
                                                required
                                            />
                                            {key}
                                        </label>
                                        <br></br>
                                    </>
                                )
                            }
                        )}
                    </form>
                    <Button text="Построить график" onClick={this.handleDownloadPlot}></Button>
                </>
            )
        }
    }
}

export default Coordinates