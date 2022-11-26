<p align="center">
  <img alt="d4v1d" src="docs/media/logo.png" width="125" height="125" />
</p>
<h1 align="center">🅳4🆅1🅳</h1>
<p align="center">
  <img alt="GitHub" src="https://img.shields.io/github/license/MattMoony/d4v1d?style=for-the-badge">
  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/MattMoony/d4v1d?style=for-the-badge">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/MattMoony/d4v1d?style=for-the-badge&color=cecece">
</p>

---

## About

A social-media *social-engineering* tool. While originally inspired by one of my friends' Instagram  activities, starting from version `v4`, which was actually never fully releaed, the idea was for it to be a sort of *swiss army knife* for **multiple** social-media platforms.

> After over a year of not working on this project, I've decided to come back to it and start developing `v5` - maybe even with some extra help.

## Setup

*To run the older, but last complete version, `v2`, checkout the [`legacy`](https://github.com/MattMoony/d4v1d/tree/legacy) branch of this repository. It has its own `README.md` with all necessary setup steps.*

At the moment - as the current "version" of this tool isn't finished yet and therefore has no proper release, just *clone* the repo, install all pip dependencies and run `d4v1d.py` to be greated with an interactive shell.

### Linux / macOS

```bash
python3 -m pip install ./requirements-unix.txt
chmod 755 ./d4v1d.py
./d4v1d.py
```

### Windows

```bash
python -m pip install .\requirements-win.txt
python .\d4v1d.py
```

## Structure

The idea is to structure `d4v1d` as flexibly as possible, making it easy to exchange and add new components such as database connections, social-media platforms, etc. 

## Roadmap

Below is a list of things that I'm planning on incorporating / hoping to incorporate into this project. It'll probably change & grow over time. *Feel free to add more ideas if you feel like it.*

### <img src="https://instagram.com/favicon.ico" height="16em" width="auto" /> Instagram

<details>

<summary>Completion <progress max="100" value="0"></progress></summary>

- [ ] Data Collection
  - [ ] Profile Overview
  - [ ] Posts
    - [ ] Media
    - [ ] Comments
  - [ ] Followers / Following
  - [ ] Stories
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://tiktok.com/favicon.ico" height="16em" width="auto" /> TikTok

<details>

<summary>Completion <progress max="100" value="0"></progress></summary>

- [ ] Data Collection
  - [ ] Profile Overview
  - [ ] Posts
    - [ ] Media
    - [ ] Comments
  - [ ] Followers / Following
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://twitter.com/favicon.ico" height="16em" width="auto" /> Twitter

<details>

<summary>Completion <progress max="100" value="0"></progress></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://reddit.com/favicon.ico" height="16em" width="auto" /> Reddit

<details>

<summary>Completion <progress max="100" value="0"></progress></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://snapchat.com/images/favicon.png" height="16em" width="auto" /> Snapchat

<details>

<summary>Completion <progress max="100" value="0"></progress></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://facebook.com/favicon.ico" height="16em" width="auto" /> Facebook

<details>

<summary>Completion <progress max="100" value="0"></progress></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://www2.tellonym.me/assets/img/icon64x64.png" height="16em" width="auto" /> Tellonym

<details>

<summary>Completion <progress max="100" value="0"></progress></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

---

... m4ttm00ny (November 2022)
