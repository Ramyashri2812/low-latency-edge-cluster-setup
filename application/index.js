const express = require('express');
const mongoose = require('mongoose');
const ejs = require('ejs');
const path = require('path');
const app = express();

const mongoUrl = process.env.MONGO_URL || 'mongodb://localhost:27017/Healthcheck';

mongoose.connect(mongoUrl, { useNewUrlParser: true });
const HealthCheckSchema = mongoose.Schema({
    name: String,
    date: String,
    time: String,
    heart_rate: Number
});

const HealthCheckModel = mongoose.model("Healthcheck", HealthCheckSchema, "Healthcheck");
app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

app.get('/:id', async (req, res) => {
    const userId = req.params.id;
    const dname = userId.replace(/_/g, ' ');

    try {
        const rec = await HealthCheckModel.find({ name: dname }).sort({ date: -1, time: -1 });
        let alertMessage = '';
        if (rec.length === 0) {
            alertMessage="RECORDS NOT FOUND !!";
            return res.render('index.ejs', { alertMessage });
        }
        let isAlert = false;

        for (let i = 0; i < Math.min(rec.length, 5); i++) {
            const record = rec[i];
            console.log(record.heart_rate);

            if (record.heart_rate >= 100) {
                alertMessage += `<b>Heart rate is abnormal on ${record.date} at ${record.time}!</b> <br>`;
                isAlert = true;
            }
        }

        if (isAlert) {
            return res.render('index.ejs', { alertMessage });
        } else {
            alertMessage = "Everything is normal for all records.";
            return res.render('index.ejs', { alertMessage });
        }
    } catch (err) {
        console.error(err);
        return res.status(500).send("Internal Server Error");
    }
});

app.listen(4011, () => {
    console.log("Server is running!");
});
