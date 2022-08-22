import React, { Component } from "react"
import "./Dashboard.css"
import { DATABASE_API_URL } from "../static/config"
import axios from "axios"


function ThSLC(props) {
    return (
        <tr>
            <td>{props.info.id_datetime}</td>
            <td>{props.info.ip}</td>
            <td>{props.info.a}</td>
            <td>{props.info.b}</td>
            <td>{props.info.c}</td>
            <td>{props.info.d}</td>
            <td>{props.info.e_absolute}</td>
            <td>{props.info.f_percent}</td>
            <td className={props.info.color}>
                {props.info.e_percent}
            </td>
            <td>{props.info.latitude}</td>
            <td>{props.info.longitude}</td>
            <td>{props.info.height}</td>
        </tr>
    )
}

function ThInfo(props) {
    return (
        <tr>
            <td>{props.info.id_datetime}</td>
            <td>{props.info.ip}</td>
            <td>{props.info.a}</td>
            <td>{props.info.b}</td>
            <td>{props.info.c}</td>
            <td>{props.info.d}</td>
            <td>{props.info.e_absolute}</td>
            <td>{props.info.f_percent}</td>
            <td className={props.info.color}>
                {props.info.e_percent}
            </td>
        </tr>
    )
}

class Table extends Component {
    constructor(props) {
        super(props)
        this.state = {
            data: [],
            offset: 0,
            limit: 100,
            stopFetch: false
        }
    }

    componentDidMount() {
        this.updateState()
    }

    updateState() {
        if (!this.state.stopFetch) {
            axios.get(DATABASE_API_URL + this.props.url + this.props.date,
                {
                    params: {
                        offset: this.state.offset,
                        limit: this.state.limit
                    },
                    headers: {
                        'Content-Encoding': 'gzip'
                    }
                })
                .then(res => {
                    console.log(res)
                    if (res.data.length === 0) {
                        this.setState({ stopFetch: true })
                    }
                    this.state.data.push(...res.data)
                    this.setState((prevState) => ({ offset: prevState.offset + this.state.limit }))
                })
                .catch(err => {
                    console.log(`Error` + err)
                })
        }
    }

    onScroll = (e) => {
        if (e.target.offsetHeight + e.target.scrollTop - 17 === e.target.scrollHeight) {
            this.updateState()
        }
    }

    render() {
        if (!this.state.data.length) {
            return <></>
        }
        if (this.props.table === "SLC") {
            return (
                <div className="tableHolder" onScroll={this.onScroll} id={this.props.table}>
                    <table className="table">
                        <thead>
                            <tr key={"TableHead"}>
                                {this.props.columns.map(col => <th key={col}>{col}</th>)}
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.data.map(info => (<ThSLC key={info.id_datetime} info={info}></ThSLC>))}
                        </tbody>
                    </table>
                </div>
            )
        }
        if (this.props.table === "Info") {
            return (
                <div className="tableHolder" onScroll={this.onScroll} id={this.props.table}>
                    <table className="table">
                        <thead>
                            <tr key={"TableHead"}>
                                {this.props.columns.map(col => <th key={col}>{col}</th>)}
                            </tr>
                        </thead>
                        <tbody>
                            {this.state.data.map(info => (<ThInfo key={info.id_datetime} info={info}></ThInfo>))}
                        </tbody>
                    </table>
                </div>
            )
        }
    }
}

export default Table