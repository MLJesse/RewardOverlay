# RewardOverlay
Used to track rewards for a Twitch channel and show as an overlay.


# Setup
* Download and Install Python. https://www.python.org/ftp/python/3.8.3/python-3.8.3-amd64.exe
  *Link to pythons exe installer, you can go on their web-page and download it yourself if you prefer.
  *Ensure the version is the same if you choose to do this, no guarantees it will work with differnt versions.
* If you're cloning the git repo, ensure git is set up: https://git-scm.com/download/win
* Run the install.bat which will give install selenium for you, selenium is required by python to run the web driver.
* I've supplied a chromedriver for chrome version 83, but if you don't want to run a random exe or have a different version of chrome, you can find more here: https://chromedriver.chromium.org/downloads
  *You don't technically need to run the exe, but it is used in the code.
* Once Python is installed and the install.bat has finished, just run the python script.
  *You can view the code here in github, or you can edit it on your favorite text editor to ensure it's safe.

# Known Issues
* There is an awkard outline around the text without a border, to be honest I think the border looks better and solve this issue, so I added it.
* Only supports two channel rewards right now, easy to expand later.
* Code is sloppy due to non-professional needs.

# Whats Next
* If you want more functionality or something adjusted/changed, just reach out.
