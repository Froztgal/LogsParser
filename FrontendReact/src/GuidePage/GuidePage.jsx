import React, { Component } from "react"
import "./GuidePage.css"

class GuidePage extends Component {
  render() {
    return (
      <>
        <div className="textHolder">
          <h1>Долгий способ:</h1>
          <ol>
            <li>Зайти на РДП</li>
            <li>Открыть MobaXterm</li>
            <li>Ввести в MobaXterm команду "ssh nvg@10.50.64.170" и нажать Enter</li>
            <li>Ввести в консоли "sudo bash" и нажать Enter</li>
            <li>Ввести в консоли "mc" и нажать Enter</li>
            <li>Копируем нужные файлы из /home/sysuser/greencode/StartDaemon/LOG в /home/nvg/@DIR@</li>
            <li>Закрываем терминал ("CTRL+O")</li>
            <li>Ввести в консоли "chown -R nvg:nvg /home/nvg/@DIR@" и нажать Enter</li>
            <li>В новом окне MobaXterm ввести команду "scp -r nvg@10.50.64.170:/home/nvg/@DIR@ ./@DIR@" и нажать Enter</li>
            <li>Скопировать с RDP (C:\Users\Administrator\Documents\MobaXterm\home\@DIR@) себе на рабочий стол папку с файлами</li>
          </ol>
        </div>

        <div className="textHolder">
          <h1>Быстрый способ:</h1>
          <ol>
            <li>Зайти на РДП</li>
            <li>Открыть MobaXterm</li>
            <li>Ввести в MobaXterm команду "./logs_extractor.sh" и нажать Enter</li>
            <li>Скопировать с RDP (C:\Users\Administrator\Documents\MobaXterm\home\myLog) себе на рабочий стол</li>
          </ol>
        </div>


        <img src="https://c.tenor.com/ckwiG8tPdsYAAAAi/tkthao219-capoo.gif" alt="" />
      </>
    )
  }
}

export default GuidePage