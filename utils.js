module.exports = { belge, me, info, unban, exam};
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




async function belge(event, id, login, slackmail){
  belgechannel = "C04AYAGL8UA"
  axios({
    method: 'post',
    url: "http://localhost:2424/belge",
    data: {
      login: login,
      mail: slackmail,
      id: id
    }
  }).then(async (response) => {
    if (response.data == "0"){
      const message = await client.chat.postMessage({
        channel: id,
        text: "Title ve mail uyumsuz. Gerekli düzenlemeyi yaptıktan sonra tekrar deneyin."
      });
      const emoji = await client.reactions.add({
        channel: event.channel,
        name: "x",
        timestamp: event.event_ts
        });
      return ;
    }
    try {
      const emoji = client.reactions.add({
        channel: event.channel,
        name: "white_check_mark",
        timestamp: event.event_ts
      });
      const file = client.files.upload({
        channels: id,
        initial_comment: "Selam " + response['data'] + ", belgeni getirdim.",
        file: fs.createReadStream("belge/" + login + ".pdf")
      });
    }
    catch (error){
    }
  }, async (error) => {
    try{
    const message = client.chat.postMessage({
      channel: id,
      text: "Lütfen biraz sonra tekrar deneyin."
    });
    const emoji = client.reactions.add({
      channel: event.channel,
      name: "x",
      timestamp: event.event_ts
      });
    }
    catch(error){

    }
  });
}
  
async function me(event, id, login, slackmail){
  let options = {
    pythonPath: '/usr/bin/python3.8',
    scriptPath: '/root/SlackBot',
    args: [login, slackmail]
  };
  await PythonShell.run('me.py', options, async function (err, results) {
      if (err){
        console.log(err)
        const message = await client.chat.postMessage({
          channel: id,
          text: "Lütfen biraz sonra tekrar deneyin."
        });
        try {
        const emoji = await client.reactions.add({
          channel: event.channel,
          name: "x",
          timestamp: event.event_ts
          });
        }
        catch(error){

        }
      }
      else if (results != 0)
      {
        try{
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
      catch (error){
        const emoji = await client.reactions.add({
          channel: event.channel,
          name: "x",
          timestamp: event.event_ts
        });
      }
    }
    else{
      const message = await client.chat.postMessage({
        channel: id,
        text: "Title ve mail uyumsuz. Gerekli düzenlemeyi yaptıktan sonra tekrar deneyin."
      });
      const emoji = await client.reactions.add({
        channel: event.channel,
        name: "x",
        timestamp: event.event_ts
      });
    }
});
}

async function unban(event, mail, login){
  if (botid == "B04AVNR1K16" || mail == "ahmethakangunes24@gmail.com"){
    let options = {
      pythonPath: '/usr/bin/python3.8',
      scriptPath: '/root/SlackBot',
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

async function exam(event, id, login, slackmail){
  channelid = "C04B78G6MKM"
  examname = event['text'].replace("!", "");
  axios({
    method: 'post',
    url: "http://localhost:2424/exam",
    data: {
      login: login,
      mail: slackmail,
    }
  }).then(async (response) => {
    if (response.data == "0"){
      const message = await client.chat.postMessage({
        channel: id,
        text: "Title ve mail uyumsuz. Gerekli düzenlemeyi yaptıktan sonra tekrar deneyin."
      });
      const emoji = await client.reactions.add({
        channel: event.channel,
        name: "x",
        timestamp: event.event_ts
      });
      return ;
    }
    try {
      const message = await client.chat.postMessage({
        channel: channelid,
        text: examname + " " + login
      });
      const emoji = client.reactions.add({
        channel: event.channel,
        name: "white_check_mark",
        timestamp: event.event_ts
      });
    }
    catch (error){
    }
  });
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