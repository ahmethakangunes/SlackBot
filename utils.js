module.exports = { belge, me, agu };
const { PythonShell } = require('python-shell');
const { WebClient, LogLevel } = require("@slack/web-api");
const eventsApi = require('@slack/events-api')
const fs = require('fs');
const { response } = require('express');


// SLACK BAĞLANTILARI //
require('dotenv').config({path: '.env'})
const token = process.env.BOT_TOKEN
const slackEvents = eventsApi.createEventAdapter(process.env.SIGNING_SECRET)
const client = new WebClient(token)




async function belge(id, login, mail){
    let options = {
      pythonPath: '/usr/bin/python3.8',
      scriptPath: '/root/slackbot',
      args: [login]
    };
    await PythonShell.run('!belge.py', options, async function (err, results) {
        if (err){
          const message = await client.chat.postMessage({
            channel: id,
            text: "Hata : Lütfen profilinizde bulunan \"Title\" bölümüne login bilginizi ekleyin."
          });
        }
        else{
          const file = await client.files.upload({
            channels: id,
            initial_comment: "Selam " + results[0] + ", belgeni getirdim.",
            file: fs.createReadStream("belge/" + login + ".pdf")
          });
      }
  });
  }
  
  async function me(id, login, mail){
    let options = {
      pythonPath: '/usr/bin/python3.8',
      scriptPath: '/root/slackbot',
      args: [login]
    };
    await PythonShell.run('!me.py', options, async function (err, results) {
        if (err){
          const message = await client.chat.postMessage({
            channel: id,
            text: "Hata : Lütfen profilinizde bulunan \"Title\" bölümüne login bilginizi ekleyin."
          });
        }
        else{
          var data = fs.readFileSync('me/' + login + ".txt", 'utf8');
          const result = await client.chat.postMessage({
            channel: id,
            text: data
          });
      }
  });
  }
  
  async function agu(id, login, mail){
    try {
      var data = fs.readFileSync('agu/' + login + ".txt", 'utf8');
        const result = await client.chat.postMessage({
          channel: id,
          text: data
        });
      }catch{
        const message = await client.chat.postMessage({
          channel: id,
          text: "İşlem bilgisi bulunamadı."
        });
      }
  }