const { PythonShell } = require('python-shell');
const { WebClient, LogLevel } = require("@slack/web-api");
const eventsApi = require('@slack/events-api')
const express = require("express")
const axios = require('axios');
const app = express()
const utils = require("./utils.js")
const bodyParser = require('body-parser');
const fs = require('fs');
const { response } = require('express');
const { info } = require('console');
const PORT = process.env.PORT || 3000


// SLACK BAĞLANTILARI //
require('dotenv').config({path: '.env'})
const token = process.env.BOT_TOKEN
const slackEvents = eventsApi.createEventAdapter(process.env.SIGNING_SECRET)
const client = new WebClient(token)
app.use('/slack/events', slackEvents.expressMiddleware())
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


app.post('/blackhole', async (req, res) => {
    res.send("İzinler kontrol ediliyor. Lütfen bekleyiniz.")
    user = req.body.user_name
    if (user == "42turkiyepedago" || user == "ahmethakangunes24" || user == "42turkiyeteknik" || user == "nkahrima"){
    var channel_id = "C04AR4L5RE1";
    var text = req.body.text;
    text = text.split(" ");
    var login = text[0];
    var command = text[1];
    var list = []
    axios({
      method: 'post',
      url: "http://localhost:2424/clear",
    }).then(async (response) => {
      response.data.map(async (element) => {
        await new Promise(resolve => setTimeout(resolve, 5000));
        try{
        list = await client.users.lookupByEmail({
          email: element
        })
        }
        catch (error) {
          return [];
        }
      const message = await client.chat.postMessage({
        channel: channel_id,
        text: list['user']['profile']['email']
      });
      })
    })
  }
  else
    res.end("Bu komut için yetkiniz bulunmamaktadır.")
})

app.post('/info', async (req, res) => {
    res.send("İzinler kontrol ediliyor. Lütfen bekleyiniz.")
    user = req.body.user_name
    if (user == "42turkiyepedago" || user == "ahmethakangunes24" || user == "42turkiyeteknik" || user == "nkahrima"){
    const result = await client.users.info({
      user: req.body.user_id
    })
    mail = result.user.profile.email
    id = req.body.user_id
    channel = req.body.channel_id
    command = req.body.text.split(" ")
    if (Object.keys(command).length != 1)
      res.end("Komutu yanlış girdiniz. Lütfen \"ban login day\" şeklinde kullanın.")
    else{
      login = command[0]
      axios({
        method: 'post',
        url: "http://localhost:2424/info",
        data: {
          login: login,
        }
      }).then(async (response) => {
        try {
        var data = fs.readFileSync('info/' + login + ".txt", 'utf8');
        const result = await client.chat.postMessage({
          channel: id,
          text: data
          });
        }
        catch(error){
          
        }
      }, (error) => {
        print(error)
        const message = client.chat.postMessage({
          channel: id,
          text: "Bu logine ait bir kullanıcı bulunamadı."
        });
      });
    }
  }
  else
    res.end("Bu komut için yetkiniz bulunmamaktadır.")
})


slackEvents.on("message", async(event) => {
  if (event.bot_id != "B04ABUBKSAK" && event.subtype != "message_deleted" && event.text != ""){
    try {
      var id = event.user
      const result = await client.users.info({
        user: id
      });
      login = result.user.profile.title
      mail = result.user.profile.email
      command = event['text'].split(" ")
       if (event['text'] == "!belge")
        utils.belge(event, id, login, mail);
      if (event['text'] == "!me")
        utils.me(event, id, login, mail);
        
    }
    catch (error) {
      const result = await client.chat.postMessage({
        channel: id,
        text: "Slack kaynaklı bir sorun yüzünden talebinize cevap veremiyorum. Biraz bekledikten sonra tekrar deneyin."
      });
    }
  }
})

app.listen(PORT, () => {
    console.log("Running..")
})