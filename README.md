<p align="center">
  <img alt="d4v1d" src="docs/_static/logo.png" width="125" height="125" />
</p>
<h1 align="center">🅳4🆅1🅳</h1>
<p align="center">
  <img alt="GitHub" src="https://img.shields.io/github/license/MattMoony/d4v1d?style=for-the-badge">
  <img alt="GitHub top language" src="https://img.shields.io/github/languages/top/MattMoony/d4v1d?style=for-the-badge">
  <img alt="GitHub Repo stars" src="https://img.shields.io/github/stars/MattMoony/d4v1d?style=for-the-badge&color=cecece">
</p>

---

## ❓ About

A social-media *social-engineering* tool. While originally inspired by one of my friends' Instagram  activities, starting from version `v4`, which was actually never fully releaed, the idea was for it to be a sort of *swiss army knife* for **multiple** social-media platforms.

> After over a year of not working on this project, I've decided to come back to it and start developing `v5` - maybe even with some extra help.

For more info on how `d4v1d` works, how to extend it and how to use it, take a look at the [docs](https://mattmoony.github.io/d4v1d).

> ❗ **Note:** This project is still in development, which is why it is not impossible for there to be bugs or other unwanted behaviour. If you find any, please report them in the [issues](https://github.com/MattMoony/d4v1d/issues) section. Of course you can also decide to contribute and start working on your own fix.

## 👷 Setup

*To run the older, but last complete version, `v2`, checkout the [`legacy`](https://github.com/MattMoony/d4v1d/tree/legacy) branch of this repository. It has its own `README.md` with all necessary setup steps.*

At the moment, since `d4v1d` is still under active development, just clone the repo and run the following command ...

```bash
pip install .
```

... this will make `d4v1d` available as a command in your terminal, if you have `~/.local/bin` (at least on Linux) in your path, as this is where `pip` will put the script per default. In the future, as soon as the first release is available, you will be able to simply install `d4v1d` from PyPI or from [releases](https://github.com/MattMoony/d4v1d/releases).

## 🎮 Usage

Simply run the main script (`d4v1d.py`) to enter `d4v1d`'s terminal-like environment:

```bash
python3 -m d4v1d
```

To learn more about the commands and features you can use from here, take a look at [USAGE.md](docs/USAGE.md).

## 🏗️ Structure

The idea is to structure `d4v1d` as flexibly as possible, making it easy to exchange and add new components such as database connections, social-media platforms, etc. More about the structure of platforms can be found in [PLATFORMS.md](docs/PLATFORMS.md).

## 🛣️ Roadmap

Below is a list of things that I'm planning on incorporating / hoping to incorporate into this project. It'll probably change & grow over time. *Feel free to add more ideas if you feel like it.*

### <img src="https://instagram.com/favicon.ico" height="16em" width="auto" /> Instagram

<details>

<summary>Completion <img src="https://progress-bar.dev/15/" height="13em" /></summary>

- [ ] Data Collection
  - [x] Profile Overview
  - [ ] Posts
    - [x] Media
    - [ ] Comments
  - [ ] Followers / Following
  - [ ] Stories
- [ ] DB Controllers
  - [x] SQLite
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

## 💡 Ideas

As already mentioned above, `d4v1d` is supposed to be a sort of data aggregator for multiple social-media platforms. Obviously, once you have some data, you can start doing some cool things with it, like perhaps start tracing people across multiple networks using simple characteristics like their usernames, profile pictures, etc. or even using more advanced concepts like *facial recognition* ...

---

[⬆️ Back to top](#❓-about)

... m4ttm00ny (December 2022)
