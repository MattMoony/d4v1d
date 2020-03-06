window.onload = () => {
    function plot_user(uname) {
        
    }

    let sb = document.getElementsByClassName('sidebar')[0];
    let us = sb.getElementsByTagName('div');
    [...us].forEach(u => {
        u.onclick = () => plot_user(u.innerHTML);
    });
};