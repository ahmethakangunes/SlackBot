module.exports = { belge, me, agu, info, unban};
const { PythonShell } = require('python-shell');
const { WebClient, LogLevel } = require("@slack/web-api");
const eventsApi = require('@slack/events-api')
const fs = require('fs');
const axios = require('axios');
const { response } = require('express');


// SLACK BAĞLANTILARI //
require('dotenv').config({path: '.env'})
const token = process.env.BOT_TOKEN
const slackEvents = eventsApi.createEventAdapter(process.env.SIGNING_SECRET)
const client = new WebClient(token)




async function belge(event, id, login, mail){
  axios({
    method: 'post',
    url: "http://localhost:2424/belge",
    data: {
      login: login,
      mail: mail,
      id: id
    }
  }).then((response) => {
    const file = client.files.upload({
      channels: id,
      initial_comment: "Selam " + response['data'] + ", belgeni getirdim.",
      file: fs.createReadStream("belge/" + login + ".pdf")
    });
    const emoji = client.reactions.add({
      channel: event.channel,
      name: "white_check_mark",
      timestamp: event.event_ts
    });
  }, (error) => {
    const message = client.chat.postMessage({
      channel: id,
      text: "Hata : Lütfen profilinizde bulunan \"Title\" bölümüne login bilginizi ekleyin."
    });
    const emoji = client.reactions.add({
      channel: event.channel,
      name: "x",
      timestamp: event.event_ts
    });
  });
}
  
async function me(event, id, login, mail){
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
        const emoji = await client.reactions.add({
          channel: event.channel,
          name: "white_check_mark",
          timestamp: event.event_ts
          });
    }
});
}

async function unban(event, mail, login){
  botid = event.bot_profile.id
  if (botid == "B04AVNR1K16" || mail == "ahmethakangunes24@gmail.com"){
    let options = {
      pythonPath: '/usr/bin/python3.8',
      scriptPath: '/root/slackbot',
      args: [login]
    };
    await PythonShell.run('!unban.py', options, async function (err, results) {
      if (err){
        await client.chat.postMessage({
          channel: event.id,
          text: "Ban kaldırılamadı. Lütfen manuel olarak kaldırınız."
        });
      }
      else{
      const emoji = await client.reactions.add({
        channel: event.channel,
        name: "white_check_mark",
        timestamp: event.event_ts
        });
      }
    });
  }
  else
    return ;
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

async function info(id, channelid){
  let options = {
    pythonPath: '/usr/bin/python3.8',
    scriptPath: '/root/slackbot',
    args: [command[1]]
  };
  await PythonShell.run('!info.py', options, async function (err, results) {
      if (err){
        const message = await client.chat.postMessage({
          channel: channelid,
          text: "Kullanıcı bulunamadı."
        });
      }
      else{
        var data = fs.readFileSync('info/' + command[1] + ".txt", 'utf8');
        const result = await client.chat.postMessage({
          channel: channelid,
          text: data
        });
    }
});
}