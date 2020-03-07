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
    let net = null;
    let ndata = {};
    let done = [];

    function set_cu(user) {
        cu._.href = `https://instagram.com/${user.username}`;
        cu.profile.src = user.profile_pic_url || `/media/anon.jpg`;
        cu.private.style.display = user.is_private ? 'inline' : 'none';
        cu.username.innerHTML = user.username;
        cu.verified.style.display = user.is_verified ? 'inline' : 'none';
        cu.fullname.innerHTML = user.full_name || '';
        net.focus(user.username);
    }

    function create_net(data) {
        let opts = {
            layout: {
                improvedLayout: false,
            },
            physics: {
                enabled: true,
                barnesHut: {
                    gravitationalConstant: -100_000,
                    damping: 1,
                    avoidOverlap: 1,
                },
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
        let netw = new vis.Network(co, data, opts);
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
        }
        ndata = {
            nodes: new vis.DataSet([]),
            edges: new vis.DataSet([]),
        };
        net = create_net(ndata);
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

    async function build_plot_r(user, d=2) {
        if (!ndata.nodes.get(user.username)) ndata.nodes.add({ 
            id: user.username, 
            label: user.username, 
            shape: user.profile_pic_url ? 'circularImage' : 'dot',
            image: user.profile_pic_url,
            user: user,
        });
        if (d > 0) {
            let reso = await get_followers(user.username);
            let resi = await get_following(user.username);
            done.push(user.username);
            for (let f of [...(reso.success ? reso.followers : []), ...(resi.success ? resi.following : []), ]) {
                if (!done.includes(f.username)) {
                    await build_plot_r(f, d-1);
                    if (reso.success && reso.followers.map(f => f.username).includes(f.username)) ndata.edges.add({ 
                        from: f.username, 
                        to: user.username, 
                    });
                    if (resi.success && resi.following.map(f => f.username).includes(f.username)) ndata.edges.add({ 
                        from: user.username, 
                        to: f.username, 
                    });
                }
            }
        }
    }

    async function plot_user(uname) {
        ndata = {
            nodes: new vis.DataSet([]),
            edges: new vis.DataSet([]),
        };
        done = [];
        net = create_net(ndata);
        build_plot_r({ username: uname, });
    }

    uin.onkeyup = e => {
        if (e.keyCode === 13) { // <Enter>
            let uname = uin.value;
            if (net && ndata.nodes.get(uname)) {
                net.selectNodes([ uname, ]);
                set_cu(ndata.nodes.get(uname).user);
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
        }
    };
};