window.onload = () => {
    let sb = document.getElementsByClassName('sidebar')[0];
    let co = document.getElementsByClassName('content')[0];
    let graph_user = '';
    let us = sb.getElementsByTagName('div');
    [...us].forEach(u => {
        u.onclick = () => {
            let prev = u.parentElement.getElementsByClassName('active')[0];
            if (prev) prev.classList.remove('active');
            u.classList.add('active');
            plot_user(u.innerHTML);
            graph_user = u.innerHTML;
        }
    });
    let cu = {
        _: document.getElementById('cu-user'),
        profile: document.getElementById('cu-profile'),
        private: document.getElementById('cu-private'),
        username: document.getElementById('cu-username'),
        verified: document.getElementById('cu-verified'),
        fullname: document.getElementById('cu-fullname'),
    };
    let uin = document.getElementById('user-in');
    let fin = document.getElementById('file-input');
    fin.onchange = () => {
        let reader = new FileReader();
        if (fin.files.length) {
            let f = fin.files[0];
            if (f.type !== 'application/json') {
                window.alert('Only JSON files, please!');
                return;
            }
            reader.readAsText(f);
            reader.onload = () => load_net(JSON.parse(reader.result));
        }
    };
    let opf = document.getElementById('open-file');
    opf.onclick = () => {
        fin.click();
    };
    let prog = document.getElementById('progress');
    let cons = document.getElementsByClassName('cons')[0];
    let net = null;
    let ndata = {};
    let can = null;
    const OPTIONS = {
        autoResize: false,
        layout: {
            improvedLayout: false,
        },
        physics: {
            enabled: true,
            barnesHut: {
                gravitationalConstant: -10_000,
                damping: 1,
                // avoidOverlap: 1,
            },
            maxVelocity: 100,
            minVelocity: 50,
        },
        nodes: {
            size: 10,
            borderWidth: 0.5,
            color: {
                background: '#33FFD1',
                border: '#13604E',
            },
        },
        edges: {
            arrows: {
                to: true,
            },
            smooth: {
                enabled: true,
                type: 'continuous',
            },
            color: {
                color: '#e0e0e0',
                highlight: '#FF33C7',
            },
        },
        interaction: {
            dragNodes: true,
            hideEdgesOnDrag: false,
        }
    };
    let opts = OPTIONS;
    let users = {};
    
    const SCALEF = 2500;
    const TIMEOUT = 1500;

    class InstaUser {
        constructor(username, depth, data=null) {
            this.username = username;
            this.depth = depth;
            this.scraped = true;
            if (data) {
                this.id = data.id;
                this.full_name = data.full_name;
                this.is_private = data.is_private;
                this.is_verified = data.is_verified;
                this.profile_pic_url = data.profile_pic_url;
                this.scraped = data.scraped;
            }
            this.followers = [];
            this.following = [];
        }
    }

    function set_cu(user, focus=false) {
        cu._.href = `https://instagram.com/${user.username}`;
        cu.profile.src = user.profile_pic_url || `/media/anon.jpg`;
        cu.private.style.display = user.is_private ? 'inline' : 'none';
        cu.username.innerHTML = user.username;
        cu.verified.style.display = user.is_verified ? 'inline' : 'none';
        cu.fullname.innerHTML = user.full_name || '';
        if (focus) net.focus(user.username);
        if (Object.keys(users).length > 0) {
            cons.innerHTML = '';
            let h = document.createElement('h3');
            h.innerHTML = 'Followers';
            cons.appendChild(h);
            for (let o of users[user.username].followers) {
                let d = document.createElement('div');
                d.innerHTML = o;
                cons.appendChild(d);
            }
            h = document.createElement('h3');
            h.innerHTML = 'Following';
            cons.appendChild(h);
            for (let i of users[user.username].following) {
                let d = document.createElement('div');
                d.innerHTML = i;
                cons.appendChild(d);
            }
        }
    }

    function create_net(data) {
        opts = OPTIONS;
        let netw = new vis.Network(co, data, opts);
        can = co.getElementsByTagName('canvas')[0];
        netw.on('click', params => {
            let nid = params.nodes[0];
            if (typeof nid === 'undefined') return;
            set_cu(ndata.nodes.get(nid).user);
        });
        return netw;
    }

    function save_net() {
        let a = document.createElement('a');
        a.style.display = 'none';
        a.setAttribute('href', `data:application/json;charset=utf-8,${encodeURIComponent(JSON.stringify({
            nodes: ndata.nodes.get(),
            edges: ndata.edges.get(),
        }))}`);
        a.setAttribute('download', `${graph_user}.d4v1dnet.${new Date().toISOString().replace(/:/g, '-').replace(/\./g, '_')}.json`);
        document.body.appendChild(a);
        a.click();
        document.body.removeChild(a);
    }

    function load_net(saved) {
        if (net) {
            net.destroy();
            net = null;
            can = null;
        }
        ndata = {
            nodes: new vis.DataSet([]),
            edges: new vis.DataSet([]),
        };
        net = create_net(ndata);
        opts.physics.barnesHut.gravitationalConstant = -ndata.nodes.length*SCALEF;
        window.onresize();
        net.addNodeMode();
        (async () => {
            for (let n of saved.nodes) {
                ndata.nodes.add(n);
            }
            for (let e of saved.edges) {
                ndata.edges.add(e);
            }
            net.disableEditMode();
        })();
    }

    async function get_followers(uname) {
        return await (await fetch(`/api/followers/${uname}`)).json();
    }

    async function get_following(uname) {
        return await (await fetch(`/api/following/${uname}`)).json();
    }

    function add_node(user) {
        ndata.nodes.add({
            id: user.username,
            label: user.username,
            shape: user.profile_pic_url ? 'circularImage' : 'dot',
            image: user.profile_pic_url,
            user: user,
        });
    }

    function add_edge(fuser, tuser) {
        ndata.edges.add({
            from: fuser.username,
            to: tuser.username,
        });
    }
    
    function cedge(fuser, tuser) {
        return {
            from: fuser.username,
            to: tuser.username,
        };
    }

    async function build_plot_r(user, d=2) {
        let q = [new InstaUser(user.username, 0),];
        add_node(q[0]);
        let a = [user.username];
        let p = [];
        let c = null;
        let i = 0;
        users = {};
        while (q.length > 0) {
            prog.max = i+q.length;
            prog.value = i++;

            c = q.shift();
            users[c.username] = c;
            if (!c.scraped) continue;
            
            let reso = await get_followers(c.username),
                resi = await get_following(c.username);
            let _followers = reso.success ? reso.followers : [],
                _following = resi.success ? resi.following : [];
            let followers = _followers.map(f => f.username),
                following = _following.map(f => f.username);
            let all = [..._followers, ..._following.filter(f => !followers.includes(f.username)), ];

            if (all.length > 0) p.push(c.username);

            let amount = followers.length+following.length;
            opts.physics.barnesHut.gravitationalConstant -= amount*SCALEF;
            net.setOptions(opts);

            for (let f of all) {
                f = new InstaUser(f.username, c.depth+1, f);
                if (!a.includes(f.username)) {
                    add_node(f);
                    a.push(f.username);
                    users[f.username] = f;
                    if (f.depth < d) q.push(f);
                }
                if (!p.includes(f.username)) {
                    if (followers.includes(f.username)) {
                        add_edge(f, c);
                        users[c.username].followers.push(f.username);
                        users[f.username].following.push(c.username);
                    }
                    if (following.includes(f.username)) {
                        add_edge(c, f);
                        users[c.username].following.push(f.username);
                        users[f.username].followers.push(c.username);
                    }
                }
            }

            await (async () => new Promise(resolve => window.setTimeout(resolve, TIMEOUT)))();
        }
    }

    async function plot_user(uname) {
        ndata = {
            nodes: new vis.DataSet([]),
            edges: new vis.DataSet([]),
        };
        net = create_net(ndata);
        window.onresize();
        build_plot_r({ username: uname, });
    }

    uin.onkeyup = e => {
        if (e.keyCode === 13) { // <Enter>
            let uname = uin.value;
            if (net && ndata.nodes.get(uname)) {
                net.selectNodes([ uname, ]);
                set_cu(ndata.nodes.get(uname).user, true);
                uin.value = '';
                uin.blur();
            } 
        }
    };

    document.onkeydown = e => {
        if (e.keyCode === 27) { // <Esc>
            if (net) {
                net.releaseNode();
                net.selectNodes([]);
                net.selectEdges([]);
            }
        } else if (e.keyCode === 83 && e.ctrlKey) { // <Ctrl> + s
            e.preventDefault();
            save_net();
        } else if (e.keyCode === 71 && e.ctrlKey) { // <Ctrl> + g
            e.preventDefault();
            let g = +window.prompt('Enter new gravitational constant: ');
            if (!isNaN(g) && net) {
                opts.physics.barnesHut.gravitationalConstant = g;
                net.setOptions(opts);
                net.redraw();
            }
        }
    };

    let i = 0;
    window.onresize = () => {
        // console.log(`${i++}: ${Boolean(can) && Boolean(net)}`);
        if (can && net) {
            let { width, height } = co.getBoundingClientRect();
            let w = `${width}px`, h = `${height}px`;
            // console.log(w, h);
            can.style.width = w;
            can.style.height = h;
            net.setSize(w, h);
            net.redraw();
        }
    };
};