import React, { Component } from "react"
import { BrowserRouter, Route, Routes } from "react-router-dom"
import { NavLink } from "react-router-dom"
import UploadPage from "../UploadPage/UploadPage"
import DashboardPage from "../DashboardPage/DashboardPage"
import GuidePage from "../GuidePage/GuidePage"
import MenuButton from "../Buttons/MenuButton"
import "./Main.css"


const menus = [
    { to: "/upload", text: "Загрузить" },
    { to: "/dashboard", text: "Отчеты" },
    { to: "/guide", text: "Инструкции" },
]

class Main extends Component {
    render() {
        return (
            <BrowserRouter>
                <div>
                    <div className="menu">
                        {menus.map((button) => {
                            return (
                                <NavLink to={button.to} key={button.to}>
                                    <MenuButton text={button.text}></MenuButton>
                                </NavLink>
                            )
                        })}
                    </div>
                    <div className="content">
                        <Routes>
                            <Route path="/upload" element={<UploadPage />} />
                            <Route path="/dashboard" element={<DashboardPage />} />
                            <Route path="/guide" element={<GuidePage />} />
                        </Routes>
                    </div>
                </div>
            </BrowserRouter>
        )
    }
}

export default Main