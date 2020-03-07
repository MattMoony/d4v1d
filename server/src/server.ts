import * as express from 'express';
import * as http from 'http';
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

function dirs_with(uname: string, c: string, fname: string, dir: string = TMP): Promise<string> {
    let upath: string = path.join(TMP, uname);
    return new Promise((resolve, reject) => {
        fs.exists(upath, _ex => {
            if (!_ex) return reject({ msg: 'Not scraped', });
            fs.readdir(upath, (err, files) => {
                if (err) return reject({ code: 500, msg: 'Internal error', });
                let qgs: string[] = files.filter(f => f.startsWith(c)).sort();
                if (qgs.length === 0) return reject({ msg: 'Not scraped', });
                let qg: string;
                do {
                    qg = path.join(upath, qgs.pop(), fname);
                } while (!fs.existsSync(qg) && qgs.length > 0);
                if (!fs.existsSync(qg)) return reject({ msg: 'No valid files', });
                resolve(`{ "success": true, "${fname.split('.')[0]}": ${fs.readFileSync(qg).toString()} }`);
            });
        });
    });
}

const app: express.Express = express();
app.get('/', (req, res) => {
    fs.readFile(path.join(PUBLIC, 'index.html'), (err, data) => {
        if (err) return res.status(500).send('Internal Server Error!');
        fs.readdir(TMP, (err, files) => {
            if (err) return res.status(500).send('Internal Server Error!');
            let temp: handlebars.Template = handlebars.compile(data.toString());
            res.send(temp({
                users: files.filter(f => fs.lstatSync(path.join(TMP, f)).isDirectory()).map(f => { return { name: f, }; }),
            }));
        });
    });
});
app.get('/api/followers/:uname', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    dirs_with(req.params.uname, 'o', 'followers.json')
        .then(msg => res.send(msg))
        .catch(msg => res.status(msg.code ? msg.code : 200).send(JSON.stringify({ success: false, msg: msg.msg, })));
});
app.get('/api/following/:uname', (req, res) => {
    res.setHeader('Content-Type', 'application/json');
    dirs_with(req.params.uname, 'i', 'following.json')
        .then(msg => res.send(msg))
        .catch(msg => res.status(msg.code ? msg.code : 200).send(JSON.stringify({ success: false, msg: msg.msg, })));
});
app.use('/', express.static(PUBLIC));

const server: http.Server = http.createServer(app);
server.listen(conf.port, () => console.log(` [d4v1d-s3rv3r]: Listening on :${conf.port} ... `));

process.on('SIGTERM', () => {
    console.log('Closing ... ');
    server.close();
});