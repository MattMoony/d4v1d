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

## Usage

Simply run the main script (`d4v1d.py`) to enter `d4v1d`'s terminal-like environment:

```bash
python3 ./d4v1d.py
```

To learn more about the commands and features you can use from here, take a look at the [docs](docs/USAGE.md).

## Structure

The idea is to structure `d4v1d` as flexibly as possible, making it easy to exchange and add new components such as database connections, social-media platforms, etc.

## Roadmap

Below is a list of things that I'm planning on incorporating / hoping to incorporate into this project. It'll probably change & grow over time. *Feel free to add more ideas if you feel like it.*

### <img src="https://instagram.com/favicon.ico" height="16em" width="auto" /> Instagram

<details>

<summary>Completion <img src="https://progress-bar.dev/0/" height="13em" /></summary>

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

<summary>Completion <img src="https://progress-bar.dev/0/" height="13em" /></summary>

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

<summary>Completion <img src="https://progress-bar.dev/0/" height="13em" /></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://reddit.com/favicon.ico" height="16em" width="auto" /> Reddit

<details>

<summary>Completion <img src="https://progress-bar.dev/0/" height="13em" /></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://snapchat.com/images/favicon.png" height="16em" width="auto" /> Snapchat

<details>

<summary>Completion <img src="https://progress-bar.dev/0/" height="13em" /></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://facebook.com/favicon.ico" height="16em" width="auto" /> Facebook

<details>

<summary>Completion <img src="https://progress-bar.dev/0/" height="13em" /></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://www2.tellonym.me/assets/img/icon64x64.png" height="16em" width="auto" /> Tellonym

<details>

<summary>Completion <img src="https://progress-bar.dev/0/" height="13em" /></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://bere.al/favicon.ico" height="16em" width="auto" /> BeReal

<details>

<summary>Completion <img src="https://progress-bar.dev/0/" height="13em" /></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

### <img src="https://tinder.com/favicon.ico" height="16em" width="auto" /> Tinder

<details>

<summary>Completion <img src="https://progress-bar.dev/0/" height="13em" /></summary>

- [ ] Data Collection
- [ ] DB Controllers
  - [ ] SQLite
  - [ ] MySQL
  - [ ] Postgres

</details>

## Ideas

As already mentioned above, `d4v1d` is supposed to be a sort of data aggregator for multiple social-media platforms. Obviously, once you have some data, you can start doing some cool things with it, like perhaps start tracing people across multiple networks using simple characteristics like their usernames, profile pictures, etc. or even using more advanced concepts like *facial recognition* ...

---

... m4ttm00ny (November 2022)
