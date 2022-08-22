import React, { Component } from "react"
import "./Dashboard.css"
import Table from "./Table"
import ModalWindow from "../Forms/ModalWindow"
import Button from "../Buttons/Button"
import { APP_API_URL } from "../static/config"
import Coordinates from "../Forms/Coordinates"
import TimeRequest from "../Forms/TimeRequest"
import axios from "axios"


class DashboardView extends Component {
  constructor(props) {
    super(props)
    this.state = {
      modalPlot: false,
      modalErrors: false
    }
  }

  handleDownloadKML = () => {
    axios({
      url: APP_API_URL + "dashboard/get_kml/" + this.props.date,
      method: 'get'
    })
      .then(res => {
        console.log(res)
        const url = window.URL.createObjectURL(new Blob([res.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'map_' + this.props.date + '.kml')
        document.body.appendChild(link)
        link.click()
      })
      .catch(err => {
        console.log(`Error` + err)
        alert(err.response.data.detail)
      })
  }

  handleModalPlotOpen = () => {
    this.setState({ modalPlot: true })
  }

  handleModalPlotClose = () => {
    this.setState({ modalPlot: false })
  }

  handleModalErrorsOpen = () => {
    this.setState({ modalErrors: true })
  }

  handleModalErrorsClose = () => {
    this.setState({ modalErrors: false })
  }

  render() {
    return (
      <>
        <div className="subMenu">
          <Button text="Назад" onClick={this.props.backHandler}></Button>
          <Button text="Скачать errors" onClick={this.handleModalErrorsOpen}></Button>
          <Button text="Скачать график" onClick={this.handleModalPlotOpen}></Button>
          <Button text="Скачать KML" onClick={this.handleDownloadKML}></Button>
        </div>

        <ModalWindow
          visibility={this.state.modalPlot}
          closeFunction={this.handleModalPlotClose}
        >
          <Coordinates date={this.props.date}></Coordinates>
        </ModalWindow>

        <ModalWindow
          visibility={this.state.modalErrors}
          closeFunction={this.handleModalErrorsClose}
        >
          <TimeRequest date={this.props.date}></TimeRequest>
        </ModalWindow>

        {/* <div className="graphHolder">
            <Plot
              data={[
                {
                  x: x,
                  y: RCV,
                  type: 'scatter',
                  mode: 'lines+markers',
                  marker: {
                    color: color,
                    size: 6
                  },
                  line: {
                    color: 'rgba(68, 68, 68, 0.3)',
                    width: 1
                  }
                }
              ]}
              className="graphGolder"
              layout={{ width: window.innerWidth, height: 400, title: 'RCV', font: { family: "JetBrainsMono" } }}
            />
          </div> */}

        <Table
          table="SLC"
          columns={["Время", "IP", "a", "b", "c", "d", "e_absolute", "f, %", "e, %", "Широта", "Долгота", "Высота"]}
          url="slc/get_on_date/"
          date={this.props.date}
        >
        </Table>

        <Table
          table="Info"
          columns={["Время", "IP", "a", "b", "c", "d", "e_absolute", "f, %", "e, %"]}
          url="info/get_on_date/"
          date={this.props.date}
        >
        </Table>

      </>
    )
  }
}

export default DashboardView