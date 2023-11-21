const express = require('express');
const bodyParser = require('body-parser');
const { exec } = require('child_process');

const app = express();
const port = 4000;

app.use(bodyParser.json());

app.post('/grafana/alert', (req, res) => {
    const scriptPath = 'script.py';
    exec(`python3 ${scriptPath}`, (error, stdout, stderr) => {
        if (error) {
          console.error(`Error executing the script: ${error}`);
          //res.status(500).send(`Error executing the script: ${error}`);
          return;
        }
        console.log(`Script executed successfully. Output: ${stdout}`);
        //console.log(res);
        console.log(req);
        //res.send(`Script executed successfully. Output: ${stdout}`);
    });
});
    
app.get('/',(req,res)=>{
    res.send("hello");
});

app.get('/grafana/alert',(req,res)=>{
    res.send("hello");
});

app.listen(port, () => {
  console.log(`Server is running on port ${port}`);
});
