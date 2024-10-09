<h1 align="center">
  🌍 Language Learning App with Python 🌍
</h1>

<div align="center">

[![Total alerts](https://img.shields.io/lgtm/alerts/g/YOUR_GITHUB_USERNAME/language-learning-app.svg?logo=lgtm&logoWidth=18)](https://lgtm.com/projects/g/YOUR_GITHUB_USERNAME/language-learning-app/alerts/)

</div>

<table border="0">
  <tr>
    <td align="center">
      This app helps users practice reading, writing, and speaking in more than 100 languages. Built with Python, it provides an interactive experience for language learners of all levels. The app includes features like speech recognition, writing exercises, and user leaderboards.
    </td>
    <td align="center">
      YouTube video showcasing the app
      <a href="https://www.youtube.com/watch?v=JasEYgm9m14">
        <img src="https://img.youtube.com/vi/JasEYgm9m14/0.jpg" alt="YouTube thumbnail for Language Learning App" />
      </a>
    </td>
  </tr>
</table>

## Technologies Used

- [Python](https://www.python.org) for backend logic
- [KivyMD](https://kivymd.readthedocs.io/en/latest) for cross-platform GUI development
- [SpeechRecognition](https://pypi.org/project/SpeechRecognition/) for speech input processing
- [Google Translate API](https://cloud.google.com/translate/docs) for language translations
- [pypinyin](https://pypi.org/project/pypinyin/) for converting Chinese characters to Pinyin

## Features

- Supports more than 100 languages for reading, writing, and speaking practice.
- Writing practice with real-time feedback on grammar and syntax.
- Speaking exercises with speech recognition for pronunciation improvements.
- Progress tracking for each user across all languages.
- Multi-platform compatibility: works on desktop and mobile devices.

## GitHub Actions

| Tag | Name | Triggers | Results |
| :--- |  :---  |  :--- | :--- |
| [![CI status](https://github.com/YOUR_GITHUB_USERNAME/language-learning-app/workflows/CI/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/language-learning-app/actions/workflows/ci.yml) | Continuous Integration | Pushes & Pull Request | Run tests, build, and lint code |
| [![Docs status](https://github.com/YOUR_GITHUB_USERNAME/language-learning-app/workflows/Docs/badge.svg)](https://github.com/YOUR_GITHUB_USERNAME/language-learning-app/actions/workflows/docs.yml) | Docs | Pushes to main branch | Builds and deploys project documentation |

## Screenshot

![screenshot](https://user-images.githubusercontent.com/YOUR_USERNAME/language-learning-app/screenshot.png)

## Quickstart

1. Fork the project
2. Clone the project using `git clone git@github.com:<YOUR-USERNAME>/language-learning-app.git`
3. Navigate into the project using `cd language-learning-app`
4. Set up a virtual environment and install dependencies:
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
5. Run the app:
    ```bash
    python main.py
    ```
    
## Goals

This app aims to make language learning accessible to everyone, regardless of their native language. Whether you're learning a new language for fun or studying it for work or travel, this app provides a robust set of tools to help you improve.

## Vision

- Support even more languages and dialects.
- Expand features to include cultural insights and language-based games.
- Make language learning an enjoyable and immersive experience.

## Made with ❤️ for language learners!
