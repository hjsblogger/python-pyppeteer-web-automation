<img width="2200" height="400"alt="Pyppeteer-logo" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/11df6f89-6af9-4473-a36d-7733a48ec469">

<div align="center"><a href="https://pythonfix.com/pkg/p/pyppeteer/pyppeteer-banner.webp">Image Credit</a></div>
<br/>

In this <b>Web Automation with Pyppeteer</b> repo, we have covered the following scenarios:

* Handling dynamic web content
* Web Scraping using Pyppeteer
* Web automation using Pyppeter with Pyunit (or <em>unittest</em>)
* Web automation using Pyppeter with Pytest
* Handling Button Clicks
* Custom Chromium Configurations for automation
* Capturing full-page & element screenshots
* Generating pdf's with Pyppeteer
* Handling dialog-boxes
* Handling iFrames
* Customizing view ports
* Setting user-agents

## Pre-requisites for test execution

**Step 1**

Create a virtual environment by triggering the *virtualenv venv* command on the terminal

```bash
virtualenv venv
```
<img width="1418" alt="VirtualEnvironment" src="https://github.com/hjsblogger/web-scraping-with-python/assets/1688653/89beb6af-549f-42ac-a063-e5f715018ef8">

**Step 2**

Navigate the newly created virtual environment by triggering the *source venv/bin/activate* command on the terminal

```bash
source venv/bin/activate
```
**Step 3**

Procure the LambdaTest User Name and Access Key by navigating to [LambdaTest Account Page](https://accounts.lambdatest.com/security). You might need to create an an account on LambdaTest since it is used for running tests (or scraping) on the cloud Grid.

<img width="1288" alt="LambdaTestAccount" src="https://github.com/hjsblogger/web-scraping-with-python/assets/1688653/9b40c9cb-93a1-4239-9fe5-99f33766a23a">

**Step 4**

Add the LambdaTest User Name and Access Key in the *Makefile* that is located in the parent directory. Once done, save the Makefile.

![Makefile_Screenshot](https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/5a76d0a0-f74e-45d8-ab93-cdc8faa00b5d)

## Dependency/Package Installation

All the configuration settings are located in [pypoject.toml](https://github.com/hjsblogger/web-automation-with-pyppeteer/blob/main/pyproject.toml)

Run the ```make install``` command on the terminal to install the desired packages (or dependencies) - <em>pytest</em>, <em>pytest-asyncio</em>,  <em>flake8</em>, and more.

```bash
make install
```

<img width="1413" alt="poetry-install-command" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/03843263-748a-449d-8a4e-cbd9adfe9bdf">

Once the dependencies are installed, set the <em>EXEC_PLATFORM</em> to either of the following:

- local : Execution on local grid (or machine) by triggering *export EXEC_PLATFORM=local* on the terminal
- cloud : Execution on LambdaTest cloud grid by triggering *export EXEC_PLATFORM=cloud* on the terminal

<img width="1187" alt="Command" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/fba97591-4217-4770-9994-5d7a15677f30">

## Custom Chromium Versions

As mentioned in the [Official Documentation of Pyppeteer](https://miyakogi.github.io/pyppeteer/reference.html#environment-variables), there is a way to specify a particular Chromium version for web automation with Pyppeteer.

For the [Custom Configuration scenario](https://github.com/hjsblogger/web-automation-with-pyppeteer/tree/main/tests/custom-configuration), we have downloaded Chromium versions (for macOS Intel) - latest, 121, and 113 from [AppSpot](https://gsdview.appspot.com/chromium-browser-snapshots/Mac/).

Please copy the above mentioned Chromium versions and paste it in <repo-folder>/mac-chrome folder. You can find the different Chromium versions [here](https://drive.google.com/drive/folders/1CDBGc2PmbiOKZtH66BSqwmyt3JzMnfF3)

<img width="1106" alt="Chromium-Version" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/b44ca93b-e9dd-4d46-b04d-2747aec487c8">


<img width="1272" alt="Chromium-Version-Terminal" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/6a7be3ec-8027-4ec5-b4f7-6f4fb08c7318">

# Execution

By default, all the tests using Pyppeteer are executed with the non-headless Chromium version. However, involving custom Chromium version(s) and headless browser testing can be executed in headless and non-headless mode.

- non-headless (default) : Execution on Chromium browser in headed mode. ```export BROWSER_MODE=non-headless``` on the terminal
- headless : Execution on Chromium browser in headless mode. ```export BROWSER_MODE=headless``` on the terminal

<img width="1272" alt="Browser-Mode-Setting" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/041f7d77-fe59-42d8-8797-1b35eed3ad5a">

Irrespective of whether the tests are run on local machine or LambdaTest grid, simply trigger the respective command along with *make* on the terminal for test execution. Run the command ```make help``` to get a list of the available test operations that can be performed with Pyppeteer:

<img width="1161" alt="make-help" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/04b3a6b5-8b7e-4e19-944f-59dd7916e42c">

Let's take the case of *Web Scraping with Pyppeteer* on local machine & LambdaTest Grid.

## Scraping using Pyppeteer on local machine

Run the command *export EXEC_PLATFORM=local* on the terminal. Since you would have triggered ```make install``` earlier, downloaded Chromium version will already be present in the */Users/<username>/Library/Application Support/pyppeteer* folder (on macOS)

<img width="1168" alt="local-Chromium" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/c5826b46-fe10-47e9-b0de-e1014be43e6c">

In case you are using some other OS, please refer to [Environment variables](https://miyakogi.github.io/pyppeteer/reference.html#environment-variables) section in Pyppeteer official documentation to know more about the download location of Chromium browser.

Run the command *make pyppeteer-web-scraping* for scraping content from the test website using local Chromium browser.

<img width="1409" alt="local-scraping-1" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/b171e8c0-89bd-4b2e-bd1e-73a79ba62ef8">

<img width="1409" alt="local-scraping-2" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/c302f1e5-7b00-45a6-a54e-99d2b0a59a11">

<img width="1440" alt="local-scraping-browser" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/73a00cec-3139-4c1a-96d7-da5ffdca3749">

The same test can also be executed using the *browserWSEndpoint* set to *"wss://cdp.lambdatest.com/puppeteer"*. For running Pyppeteer tests on LambdaTest, set the environment variable *EXEC_PLATFORM* to cloud by running the command ```export EXEC_PLATFORM=cloud``` on the terminal

Run the command *make pyppeteer-web-scraping* for scraping content from the test website with Pyppeteer on LambdaTest. Shown below are the test execution snapshots on LambdaTest:

<img width="1440" alt="cloud-scraping-1" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/cd0c4823-4b84-4045-ba45-519f8dd6698d">

<img width="1440" alt="cloud-scraping-2" src="https://github.com/hjsblogger/web-automation-with-pyppeteer/assets/1688653/d7f103f2-0fbf-41d3-b50e-b1e6456b3c60">

On similar lines, you can run web automation tests (or operations like handling dialog boxes, iFrames, buttons, etc.) using Pyppeteer on local Chromium as well as LambdaTest cloud grid. For more information on the commands, simply trigger ```make help``` on the terminal and run the relevant *make* option after setting the *EXEC_PLATFORM* and/or *BROWSER_MODE* & *CHROMIUM_VERSION* environment variables on the terminal.

## Have feedback or need assistance?
Feel free to fork the repo and contribute to make it better! Email to [himanshu[dot]sheth[at]gmail[dot]com](mailto:himanshu.sheth@gmail.com) for any queries or ping me on the following social media sites:

<b>LinkedIn</b>: [@hjsblogger](https://linkedin.com/in/hjsblogger)<br/>
<b>Twitter</b>: [@hjsblogger](https://www.twitter.com/hjsblogger)