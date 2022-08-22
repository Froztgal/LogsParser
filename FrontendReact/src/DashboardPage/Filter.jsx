import React, { Component } from "react"
import Button from "../Buttons/Button"

class Filter extends Component {
    // On select date
    handleDateSelect = (e) => {
        const date = e.target.value

        const table = document.getElementById(this.props.tableId)
        const tr = table.getElementsByTagName("tr")

        if (date) {
            for (let i = 0; i < tr.length; i++) {
                const td = tr[i].getElementsByTagName("td")[0]
                if (td) {
                    const txtValue = td.textContent || td.innerText
                    if (txtValue.indexOf(date) > -1) {
                        tr[i].style.display = ""
                    } else {
                        tr[i].style.display = "none"
                    }
                }
            }
        }
        else {
            for (let i = 0; i < tr.length; i++) {
                tr[i].style.display = ""
            }
        }
    }

    clearFilter = () => {
        const table = document.getElementById(this.props.tableId)
        const tr = table.getElementsByTagName("tr")
        const filter = document.getElementById("date")

        for (let i = 0; i < tr.length; i++) {
            tr[i].style.display = ""
        }

        filter.value = null

    }
    render() {
        return (
            <fieldset>

                <legend>Фильтровать:</legend>

                <div className="datepicker">
                    <label htmlFor="date">Выберите дату:</label>
                    <input type="date" id="date" onChange={this.handleDateSelect} />
                </div>

                <Button text="Сбросить фильтр" onClick={this.clearFilter}></Button>

            </fieldset>
        )
    }
}

export default Filter