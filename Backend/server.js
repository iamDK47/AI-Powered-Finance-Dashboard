// import express from 'express'

const express = require('express');
const app = express();

const Port = 3001

app.get('/health', (req,res) => {
 res.send('hello World')
})

app.listen(Port , () => {
 console.log('server is running')
})