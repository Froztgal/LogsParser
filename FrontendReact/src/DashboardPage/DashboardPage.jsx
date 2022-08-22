import React, { Component } from "react"
import axios from "axios"
import "./Dashboard.css"
import { DATABASE_API_URL } from "../static/config"
import Waiter from "../static/Waiter"
import TableButton from "../Buttons/TableButton"
import ButtonX from "../Buttons/ButtonX"
import ModalWindow from "../Forms/ModalWindow"
import { APP_API_URL } from "../static/config"
import DashboardView from "../DashboardPage/DashboardView"
import Filter from "./Filter"
import Form from "../Forms/Form"


class DashboardPage extends Component {
  constructor(props) {
    super(props)
    this.state = {
      reportsTable: null,
      reportDate: null,
      modalUpload: false
    }
  }

  fetchReports = () => {
    axios.get(DATABASE_API_URL + "reports/get_all/")
      .then(res => {
        this.setState({
          reportsTable: res.data
        })
      })
      .catch(err => {
        console.log(`Error` + err)
      })
  }

  componentDidMount() {
    this.fetchReports()
  }

  // Handle click
  async handleClick(log, date, status) {
    switch (status) {

      // If file not uploaded - render modal window for file uploading
      case "none":
        this.handleModalUploadOpen()
        break

      // If file uploaded - process it
      case "uploaded":

        if (log === "info") {
          await axios.post(APP_API_URL + "process_info/" + date)
            .then(res => {
              console.log(res)
            })
            .catch(err => {
              console.log(`Error` + err)
            })
        }

        else {
          await axios.post(APP_API_URL + "process_coordinates/" + date)
            .then(res => {
              console.log(res)
            })
            .catch(err => {
              console.log(`Error` + err)
            })
        }

        this.fetchReports()

        break

      // If file processed - get dasboard
      case "processed":

        this.setState({ reportDate: date })
        break

      // Else log Error
      default:
        console.log("Error in JsonDataDisplay -- handleClick (unknown button text)!")
    }
  }

  // Handle delete
  async handleDelete(log, date, status) {
    console.log(log, date, status)

    if (status === 'none') {
      return
    }
   

    switch (log) {
      // Case - delete all
      case "all":
        // Delete info
        await axios({
          url: DATABASE_API_URL + "info/delete_on_date/" + date,
          method: 'delete'
        })
          .then(res => {
            console.log(res)
          })
          .catch(err => {
            console.log(`Error` + err)
          })

        // Delete coordinates
        await axios({
          url: DATABASE_API_URL + "coordinates/delete_on_date/" + date,
          method: 'delete'
        })
          .then(res => {
            console.log(res)
          })
          .catch(err => {
            console.log(`Error` + err)
          })

        // Delete report
        await axios({
          url: DATABASE_API_URL + "reports/delete/" + date,
          method: 'delete',
        })
          .then(res => {
            console.log(res)
          })
          .catch(err => {
            console.log(`Error` + err)
          })

        this.fetchReports()

        break

      // Case - Info
      case "info":
        // Delete Info
        await axios({
          url: DATABASE_API_URL + "info/delete_on_date/" + date,
          method: 'delete'
        })
          .then(res => {
            console.log(res)
          })
          .catch(err => {
            console.log(`Error` + err)
          })

        // Update report record
        await axios({
          url: DATABASE_API_URL + "reports/update/",
          method: 'put',
          data: {
            "id_date": date,
            "info_log": "none"
          }
        })
          .then(res => {
            console.log(res)
          })
          .catch(err => {
            console.log(`Error` + err)
          })

        this.fetchReports()
        break

      // Case - Coordinates
      default:
        // Delete Coordinates
        await axios({
          url: DATABASE_API_URL + "coordinates/delete_on_date/" + date,
          method: 'delete'
        })
          .then(res => {
            console.log(res)
          })
          .catch(err => {
            console.log(`Error` + err)
          })

        // Update report record
        await axios({
          url: DATABASE_API_URL + "reports/update/",
          method: 'put',
          data: {
            "id_date": date,
            "timed_coordinates": "none",
            "colored_coordinates": "none"
          }
        })
          .then(res => {
            console.log(res)
          })
          .catch(err => {
            console.log(`Error` + err)
          })

        this.fetchReports()
    }
  }

  backHandler = () => {
    this.setState({ reportDate: null })
  }

  handleModalUploadOpen = () => {
    this.setState({ modalUpload: true })
  }

  handleModalUploadClose = () => {
    this.setState({ modalUpload: false })
    this.fetchReports()
  }

  render() {
    if (!this.state.reportsTable) return (
      <Waiter></Waiter>
    )

    else if (!this.state.reportDate) return (

      <div>

        <Filter tableId="ReportsTable"></Filter>

        <ModalWindow
          visibility={this.state.modalUpload}
          closeFunction={this.handleModalUploadClose}
        >
          <Form></Form>
        </ModalWindow>

        <table className="table" id="ReportsTable">
          <thead>
            <tr key={"TableHead"}>
              <th>Дата</th>
              <th>Статус Info</th>
              <th>Статус TimedCoord</th>
              <th>Статус ColoredCoord</th>
            </tr>
          </thead>
          <tbody>
            {
              this.state.reportsTable.map(
                (info) => {
                  return (
                    <tr key={info.id_date}>
                      <td>
                        {info.id_date}
                        <ButtonX
                          onClick={() => this.handleDelete("all", info.id_date, 'all')}>
                        </ButtonX>
                      </td>
                      <td>
                        <TableButton
                          text={info.info_log}
                          onClick={
                            () => this.handleClick("info", info.id_date, info.info_log)
                          }>
                        </TableButton>
                        <ButtonX
                          onClick={() => this.handleDelete("info", info.id_date, info.info_log)}>
                        </ButtonX>
                      </td>
                      <td>
                        <TableButton
                          text={info.timed_coordinates}
                          onClick={
                            () => this.handleClick("timed_coordinates", info.id_date, info.timed_coordinates)
                          }>
                        </TableButton>
                        <ButtonX
                          onClick={() => this.handleDelete("timed_coordinates", info.id_date, info.timed_coordinates)}>
                        </ButtonX>
                      </td>
                      <td><TableButton
                        text={info.colored_coordinates}
                        onClick={
                          () => this.handleClick("colored_coordinates", info.id_date, info.colored_coordinates)
                        }>
                      </TableButton>
                        <ButtonX
                          onClick={() => this.handleDelete("colored_coordinates", info.id_date, info.colored_coordinates)}>
                        </ButtonX>
                      </td>
                    </tr>
                  )
                }
              )
            }
          </tbody>
        </table>
      </div>
    )

    return (
      <>
        <DashboardView date={this.state.reportDate} backHandler={this.backHandler}></DashboardView>
      </>
    )
  }
}

export default DashboardPage