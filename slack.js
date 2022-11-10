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
const PORT = process.env.PORT || 3000

// SLACK BAĞLANTILARI //
require('dotenv').config({path: '.env'})
const token = process.env.BOT_TOKEN
const slackEvents = eventsApi.createEventAdapter(process.env.SIGNING_SECRET)
const client = new WebClient(token)
app.use('/slack/events', slackEvents.expressMiddleware())
app.use(bodyParser.urlencoded({ extended: true }));
app.use(bodyParser.json());


app.post('/ban', async (req, res) => {
  const result = await client.users.info({
    user: req.body.user_id
  })
  mail = result['user']['profile']['email']
  var channel_id = req.body.channel_id;
  var text = req.body.text;
  text = text.split(" ");
  var login = text[0];
  var command = text[1];
  if (mail != "ahmethakangunes24@gmail.com")
      res.end("Bu işlem için yetkiniz yoktur.")
  else if (Object.keys(text).length != 2)
    res.end('Komutu yanlış girdiniz. Lütfen "/ban login day" şeklinde kullanın.');
  else{
    let options = {
      pythonPath: '/usr/bin/python3.8',
      scriptPath: '/root/slackbot',
      args: [login, command]
    };
    await PythonShell.run('ban.py', options, async function (err, results) {
      if (err)
        res.end("Login veya işlem tipi yanlış.")
      else
        res.end(login + " hesabı " + text[1] + " gün kapatıldı.")
  });
  }
})

app.post('/agu', async (req, res) => {
    const result = await client.users.info({
      user: req.body.user_id
    })
    mail = result['user']['profile']['email']
    var channel_id = req.body.channel_id;
    var text = req.body.text;
    text = text.split(" ");
    var login = text[0];
    var command = text[1];
    if (mail != "ahmethakangunes24@gmail.com")
        res.end("Bu işlem için yetkiniz yoktur.")
    else if (Object.keys(text).length != 2)
      res.end('Komutu yanlış girdiniz. Lütfen "/agu login işlem" şeklinde kullanın.');
    else{
      let options = {
        pythonPath: '/usr/bin/python3.8',
        scriptPath: '/root/slackbot',
        args: [login, command]
      };
      await PythonShell.run('agu.py', options, async function (err, results) {
        if (err)
          res.end("Login veya işlem tipi yanlış.")
        else
          res.end("Öğrenci agu talep bilgisi güncellendi.")
    });
    }
})

slackEvents.on("message", async(event) => {
    var id = event['user']
    try {
      const result = await client.users.info({
        user: id
      });
      login = result['user']['profile']['title']
      mail = result['user']['profile']['email']
      if (event['text'] == "!belge")
        utils.belge(id, login, mail);
      if (event['text'] == "!me")
        utils.me(id, login, mail);
      if (event['text'] == "!agu")
        utils.agu(id, login, mail);
    }
    catch (error) {
      console.log(error)
      const result = await client.chat.postMessage({
        channel: id,
        text: "Slack kaynaklı bir sorun yüzünden talebinize cevap veremiyorum. Biraz bekledikten sonra tekrar deneyin."
      });
    }
})



app.listen(PORT, () => {
    console.log("Çalışıyor bremin...")
})