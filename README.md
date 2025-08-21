# bot-reCaptcha

### Web Page

#### Requirements
- PHP >= 7.4
- Composer
- `php-curl` extension

#### Check if `php-curl` is installed
Run the command:
```bash
php -m | grep curl
````

* If `"curl"` is listed, cURL is enabled.
* If not, install it with:

```bash
sudo apt-get update && sudo apt-get install php-curl
```

#### Install Dependencies

Navigate to the project directory and install dependencies with Composer:

```bash
cd app

composer --version
composer install
```

#### Environment File

Copy the environment configuration file:

```bash
cp .env.example .env
```

Update `.env` with your project’s credentials and configurations.

### Bot

#### Requirements

* Python >= 3.8
* Virtual environment support (`venv`)

#### Setup

Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

Install required dependencies:

```bash
pip install -r requirements.txt
```

Deactivate the virtual environment when finished:

```bash
deactivate
```

## Reference
https://www.youtube.com/watch?v=kG_3LZ2OgBI&ab_channel=WDEV</br>
https://www.google.com/recaptcha/admin/</br>
https://developers.google.com/recaptcha/docs/display</br>
https://developers.google.com/recaptcha/docs/verify</br>
https://www.selenium.dev/documentation/</br>
https://www.browserstack.com/guide/python-selenium-webdriver-manager</br>
https://anti-captcha.com/pt/apidoc</br>
https://configu.com/blog/env-in-php-the-basics-and-a-quick-tutorial/</br>
