const { Client, LocalAuth } = require('whatsapp-web.js');
const qrcode = require('qrcode-terminal');
const express = require('express');
const bodyParser = require('body-parser');

const app = express();
app.use(bodyParser.json());

const client = new Client({
    authStrategy: new LocalAuth(),
    puppeteer: { headless: true, args: ['--no-sandbox'] }
});

client.on('qr', (qr) => {
    console.log('--- SCAN THIS QR CODE WITH WHATSAPP ---');
    qrcode.generate(qr, { small: true });
});

client.on('ready', () => {
    console.log('WhatsApp Client is READY and Authenticated!');
});
app.post('/send-whatsapp', async (req, res) => {
    const { numbers, message } = req.body;

    if (!numbers || !message) {
        return res.status(400).json({ error: 'Missing numbers or message' });
    }

    let results = [];
    for (let number of numbers) {
        try {
            // Format number for India (91xxxxxxxxxx@c.us)
            const cleanNumber = number.replace(/\D/g, ''); 
            const chatId = cleanNumber.includes('91') ? `${cleanNumber}@c.us` : `91${cleanNumber}@c.us`;
            
            await client.sendMessage(chatId, message);
            results.push({ number, status: 'Sent' });
            console.log(`📨 WhatsApp sent to: ${number}`);
            await new Promise(resolve => setTimeout(resolve, 2000));
        } catch (err) {
            results.push({ number, status: 'Failed', error: err.message });
        }
    }

    res.json({ status: 'Process Complete', results });
});

app.listen(3000, () => {
    console.log('WhatsApp Gateway listening on http://localhost:3000');
});

client.initialize();