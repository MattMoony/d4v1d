import * as express from 'express';
import * as fs from 'fs';
import * as path from 'path';
import * as handlebars from 'handlebars';

var conf: any;
if (fs.existsSync(path.join(__dirname, '../config/conf.json'))) {
    conf = JSON.parse(fs.readFileSync(path.join(__dirname, '../config/conf.json')).toString());
} else {
    console.log(' [!] conf.json wasn\'t found!');
    process.exit(1);
}

const PUBLIC: string = path.join(__dirname, '../public');
const TMP: string = path.join(__dirname, '../../tmp');

const app: express.Express = express();
app.get('/', (req, res) => {
    fs.readFile(path.join(PUBLIC, 'index.html'), (err, data) => {
        if (err) return res.status(500).send('Internal Server Error!');
        let temp: handlebars.Template = handlebars.compile(data.toString());
        res.send(temp({
            users: [],
        }));
    });
});
app.get('/api/followers/:uname', (req, res) => {
    let upath: string = path.join(TMP, req.params.uname);
    fs.exists(upath, _ex => {
        if (!_ex) return res.status(400).send('User hasn\'t been scraped yet!');
        fs.readdir(upath, (err, files) => {
            if (err) return res.status(500).send('Internal Server Error!');
            let ogs: string[] = files.filter(f => f.startsWith('o')).sort();
            if (ogs.length === 0) return res.status(400).send('No records exist!');
            let og: string;
            do {
                og = path.join(upath, ogs.pop(), 'followers.json');
                console.log(og);
            } while (!fs.existsSync(og) && ogs.length > 0);
            if (!fs.existsSync(og)) return res.status(400).send('No records exist!');
            res.setHeader('Content-Type', 'application/json');
            res.send(fs.readFileSync(og).toString());
        });
    })
});
app.use('/', express.static(PUBLIC));
app.listen(conf.port, () => console.log(` [d4v1d-s3rv3r]: Listening on :${conf.port} ... `));