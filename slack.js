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



app.post('/ban', async (req, res) => {
  if (req.body.user_name != "ahmethakangunes24")
    res.end("Bu komut için yetkiniz bulunmamaktadır.")
  const result = await client.users.info({
    user: req.body.user_id
  })
  mail = result.user.profile.email
  var channel_id = req.body.channel_id;
  var text = req.body.text;
  text = text.split(" ");
  var login = text[0];
  var day = text[1];
  if (Object.keys(text).length != 2)
    res.end('Komutu yanlış girdiniz. Lütfen "/ban login day" şeklinde kullanın.');
  else if (isNaN(text[1]))
    res.end('Gün tipi yanlış. Lütfen kontrol ediniz')
  else if (Number(text[1] < 1) || Number(text[1] > 20))
    res.end("Gün en az 1 en fazla 20 olmalı.")
  else{
    let options = {
      pythonPath: '/usr/bin/python3.8',
      scriptPath: '/root/slackbot',
      args: [login, day]
    };
    await PythonShell.run('ban.py', options, async function (err, results) {
      if (err)
        res.end("Bu logine ait bir kullanıcı bulunamadı. Lütfen kontrol ediniz.")
      else{
        const unban = await client.chat.scheduleMessage({
          channel: req.body.channel_id,
          post_at: parseInt((Date.now() / 1000) + 86400 * text[1]),
          text: "!unban " + login
        });
        res.end(login + " hesabı " + text[1] + " gün kapatıldı.")
      }
  });
  }
})


app.post('/clear', async (req, res) => {
    if (req.body.user_name != "ahmethakangunes24")
    res.end("Bu komut için yetkiniz bulunmamaktadır.")
    else
    res.send("İşlem başladı. Tahmini süre 3 dakika.")
      const result = await client.users.info({
        user: req.body.user_id
      })
    mail = result.user.profile.email
    var channel_id = req.body.channel_id;
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
          try{
          list = await client.users.lookupByEmail({
            email: element
          })
        }
        catch (error) {
          return [];
        }
          const message = client.chat.postMessage({
            channel: req.body.user_id,
            text: list['user']['profile']['email']
          });
        })
      })
})

app.post('/info', async (req, res) => {
    if (req.body.user_name != "ahmethakangunes24")
      res.end("Bu komut için yetkiniz bulunmamaktadır.")
    else
      res.send("Lütfen mesaj kutunuzu kontrol edin.")
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
        var data = fs.readFileSync('info/' + login + ".txt", 'utf8');
        const result = await client.chat.postMessage({
          channel: id,
          text: data
        });
      }, (error) => {
        const message = client.chat.postMessage({
          channel: id,
          text: "Bu logine ait bir kullanıcı bulunamadı."
        });
      });
    }
})


slackEvents.on("message", async(event) => {
    var id = event.user
    try {
      const result = await client.users.info({
        user: id
      });
      login = result.user.profile.title
      mail = result.user.profile.email
      command = event['text'].split(" ")
      if (event['text'] == "!belge")
        utils.belge(event, id, login, mail);
      else if (event['text'] == "!me")
        utils.me(event, id, login, mail);
      else if (command['text'] == "!agu")
        utils.agu(id, login, mail);
      else if (command[0] == "!info")
        utils.info(event, id, command)
      else if (command[0] == "!unban")
        utils.unban(event, mail, command[1])
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