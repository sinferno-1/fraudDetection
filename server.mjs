import express from 'express';
import axios from 'axios';
import { fileURLToPath } from 'url';
import { dirname } from 'path';
import path from 'path';
import fs from 'fs/promises';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

const app = express();
const PORT = process.env.PORT || 3000;

app.use(express.json());

app.use(express.static(path.join(__dirname, 'sample.html')));
app.get('/', async (req, res) => {
  try {
    const ngrokIp = req.headers['x-forwarded-for'] || req.connection.remoteAddress;
    console.log('Ngrok Public IP Address:', ngrokIp);

    console.log('Incoming Headers:', req.headers);

    const ipApiResponse = await axios.get(`http://ip-api.com/json/${ngrokIp}?fields=status,message,continent,continentCode,country,countryCode,region,regionName,city,district,zip,lat,lon,timezone,offset,currency,isp,org,as,asname,reverse,mobile,proxy,hosting,query`);

    
    const timestamp = new Date().toISOString();
    
    console.log('ipApiResponse:', ipApiResponse.data);

    const logEntry = {
      timestamp: timestamp,
      ip: ipApiResponse.data.query || '',
      status: ipApiResponse.data.status || '',
      continent: ipApiResponse.data.continent || '',
      continentCode: ipApiResponse.data.continentCode || '',
      country: ipApiResponse.data.country || '',
      countryCode: ipApiResponse.data.countryCode || '',
      region: ipApiResponse.data.region || '',
      regionName: ipApiResponse.data.regionName || '',
      city: ipApiResponse.data.city || '',
      district: ipApiResponse.data.district || '',
      zip: ipApiResponse.data.zip || '',
      lat: ipApiResponse.data.lat || 0,
      lon: ipApiResponse.data.lon || 0,
      timezone: ipApiResponse.data.timezone || '',
      offset: ipApiResponse.data.offset || 0,
      currency: ipApiResponse.data.currency || '',
      isp: ipApiResponse.data.isp || '',
      org: ipApiResponse.data.org || '',
      as: ipApiResponse.data.as || '',
      asname: ipApiResponse.data.asname || '',
      reverse: ipApiResponse.data.reverse || '',
      mobile: ipApiResponse.data.mobile || false,
      proxy: ipApiResponse.data.proxy || false,
      hosting: ipApiResponse.data.hosting || false,
      bot: false,
      headers: req.headers,
    };

    const logFilePath = path.join(__dirname, 'iplog.json');
    
    let existingLogs = [];

    try {
      const fileContent = await fs.readFile(logFilePath, 'utf-8');
      existingLogs = JSON.parse(fileContent);
     
    } catch (readError) {
      console.error('Error reading iplog.json:', readError);
    }

   
    existingLogs.push(logEntry);

    try {
      await fs.writeFile(logFilePath, JSON.stringify(existingLogs, null, 2));
      console.log('Log entry successfully saved to iplog.json');
    } catch (writeError) {
      console.error('Error writing to iplog.json:', writeError);
     
    }

    res.json({
      ...logEntry,
      ngrokIp: ngrokIp,
    });
  } catch (error) {
    console.error(error);
    res.status(500).json({ error: 'Internal Server Error' });
  }
});


app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
