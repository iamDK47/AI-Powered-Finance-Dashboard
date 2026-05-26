const express = require('express');
const app = express();

const Port = 3001

app.use(express.json())

app.get('/health', (req,res) => {
 res.json({ health : 'OK'})
})

app.listen(Port , () => {
 console.log('server is running')
})