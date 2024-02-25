<br/>
<p align="center">
  <a href="https://github.com/devmehmetakifv/CTFSetup">
    <img src="ctfsetup.png" alt="Logo" width="240" height="135">
  </a>

  <h3 align="center">CTFSetup</h3>

  <p align="center">
    CTFSetup automates CTF setup, seamlessly creating target directories and initiating fundamental information-gathering scans.
    <br/>
    <br/>
    <a href="https://github.com/devmehmetakifv/CTFSetup"><strong>Explore the docs »</strong></a>
    <br/>
    <br/>
    <a href="https://github.com/devmehmetakifv/CTFSetup">View Demo</a>
    .
    <a href="https://github.com/devmehmetakifv/CTFSetup/issues">Report Bug</a>
    .
    <a href="https://github.com/devmehmetakifv/CTFSetup/issues">Request Feature</a>
  </p>

![Contributors](https://img.shields.io/github/contributors/devmehmetakifv/CTFSetup?color=dark-green) ![Issues](https://img.shields.io/github/issues/devmehmetakifv/CTFSetup) ![License](https://img.shields.io/github/license/devmehmetakifv/CTFSetup)
  
</p>

## About The Project

![Screen Shot](https://imgur.com/a/ZkjJlLJ)

CTFSetup is a command-line tool designed to accelerate Capture the Flag (CTF) competition preparation. Eliminate tedious setup tasks by automatically generating target directories and launching essential information-gathering scans. Focus on strategy and exploit development, not on the groundwork.

## Built With

CTFSetup is built with Python3 and requires no external libraries. Pure Python3!

## Getting Started

Using CTFSetup is very easy. Let's dive into the prerequisites and installation.

### Prerequisites

Install Python3

* apt

```sh
sudo apt install python3
```

### Installation

1. Clone the repo

```sh
git clone https://github.com/devmehmetakifv/ctfsetup
```

2. Place the project to the directory you want to store your CTF files.

3. Edit config.jsonc for your desires. You should set your username, wordlist directories etc.

4. Run the script
```sh
sudo python3 ctfsetup.py --name "CTF Name" --ip TARGET_IP
```

## Usage

Example usages:
* sudo python3 ctfsetup.py --name "Kabo CTF" --ip 10.10.10.180
* sudo python3 ctfsetup.py --name "Locked CTF" --ip 10.15.92.160

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.
* If you have suggestions for adding or removing projects, feel free to [open an issue](https://github.com/devmehmetakifv/CTFSetup/issues/new) to discuss it, or directly create a pull request after you edit the *README.md* file with necessary changes.
* Please make sure you check your spelling and grammar.
* Create individual PR for each suggestion.
* Please also read through the [Code Of Conduct](https://github.com/devmehmetakifv/CTFSetup/blob/main/CODE_OF_CONDUCT.md) before posting your first idea as well.

### Creating A Pull Request

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

Distributed under the MIT License. See [LICENSE](https://github.com/devmehmetakifv/CTFSetup/blob/main/LICENSE.md) for more information.

## Authors

* **Mehmet Akif VARDAR** - *Software Engineering Student & Cybersecurity Enthusiast* - [Mehmet Akif VARDAR](https://github.com/devmehmetakifv/) - *Project Owner*
