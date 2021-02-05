
<p align="center">
    <img src="https://user-images.githubusercontent.com/59141234/93002341-ff261d00-f553-11ea-874d-19ab5cb1068f.png" height="70px" />
</p>
<h4 align="center">
    Lenovo Auction Site
</h4>
<p align="center">
    Scraper to fetch details of acutions of Lenovo Laptop
    <br />
    <a href="https://www.upwork.com/ab/f/contracts/26121831">
        Project Contract
    </a>
    &nbsp;&nbsp;·&nbsp;&nbsp;
    <a href="#">
        Client - Robert
    </a>
    &nbsp;&nbsp;·&nbsp;&nbsp;
    <a href="#">
        Status - Completed
    </a>
</p>

<br />

<!-- Details of Content -->
## Table of contents

 * [Prerequisite](#Prerequisite)
 * [Unpacking](#Unpacking)
 * [Installation Dependencies](#Installation-Dependencies)
 * [Understanding Project File](#Understanding-Project-File)
 * [Running The Script](#Running-The-Script)
 * [Show Your Support](#Show-Your-Support)
 * [Contact Me](#Contact-Me)

<br />

<!-- Prerequisite -->
## Prerequisite
    - Windows
    - Python 3.6 or above
    - Chrome Webdriver

[Install Python on Windows 10](https://phoenixnap.com/kb/how-to-install-python-3-windows)

[Get Chrome WebDriver according to your Google Chrome Version](https://chromedriver.chromium.org/downloads)

<br />

<!-- Unpacking -->
## Unpacking
 - Unzip the LenovoAuction_Scrapper.zip in desired location. Let's assume that we unzip the file in location *E:\LenovoAuction*
 - After this the path of the Project lookes like *E:\LenovoAuction*
 - The project folder should look something like this:

![Lenovo-Auction](https://user-images.githubusercontent.com/59141234/106892475-21daed00-6712-11eb-83f7-3eba48682f14.png)


<!-- Instalation -->
## Installation Dependencies
 - Start terminal and type below command in terminal to point to the project folder:

 ```
 ~$ E:\
 ~$ cd LenovoAuction
 ```

 - Now we need to download all the dependencies required to run the script. For this we will type below command in terminal:

 ```
 ~$ pip3 install -r requirements.txt
 ```


<!-- Understanding File -->
## Understanding Project File

#### Data Folder 🚫
All outpoutl files will be stored in this folder.

#### requirement.txt 🚫
This file contains all the dependencies that we need to install on our system. You can delete this file but its Ok to keep it there and forget that it exists.

#### script.py 🚫
This file is the main script that we need to run to get the desired output. **Please never touch this file**.

#### selectors.config 🚫
This file contains all the selectors for different elements nodes from which data is fetched. **Please never touch this file**.

#### chomedriver.exe ⚠️
This is a chome webdriver. This is version 88.0.4324.146 and is supported by MacOs. In case you have different version of Chrome installed in your system or you have OS other than MacOs then, please replace it with the one that you will get [from here](https://chromedriver.chromium.org/downloads). Make sure you download the driver that supports your OS and have same version as that of chrome installed on your system.

#### config.json ✍️
This file needs to be edited everytime you run the script and so it needs some explation...

 - **base_url** => base url of the website *No Need to edit this*.

 - **auction_and_lot_details** => List of details of auction and lot number that are to be scrapped.

 - **strip_part_number** => Describes the format of Part Number. If *true* then script will remove any text in parenthesis – for example it will remove “(SN:276354-56)” and “(276354-56)”.

 - **output** =>  This is the format in which output is required. It can have a value of *excel* or *csv*.

 - **Processor** =>  This is the list of word which allows script to determine if the value belongs to *processor* category. Please add any word if require.

 - **Memory** =>  This is the list of word which allows script to determine if the value belongs to *memory* category. Please add any word if require.

 - **Storage** =>  This is the list of word which allows script to determine if the value belongs to *storage* category. Please add any word if require.

 - **Part** =>  This is the list of word which allows script to determine if the value belongs to *part number* category. Please add any word if require.


<!-- Running the script -->
## Running The Script
 So before running the script please make sure of two things:

 - You have edited the config file properly.
 - The pointer in terminal is pointing to the project forlder. If not then use below code:

 ```
 ~$ E:\
 ~$ cd LenovoAuction
 ```

Now we need to enter below code to execute the script.

```
~$ python3 script.py
```

Now just grab yourself a pint of 🍺 and let the script do its task.


<!-- Asking for Supports -->
## Show Your Support
If you are happy with my work then please give me :star::star::star::star::star: rating and also leave really nice recommendation/feedback on upwork. This will help me a lot in getting more project. A small and happy bonus is always appreciated 🤩. Also kindly rememeber me if you have any such project or any scraping projects. <p />Thank You for giving me opportunity to work on this project.


<!-- Displaying message about me -->
## Contact Me

**Siddhant Shah** - Please feel free to connect to me in case there is any issue in the script or any changes are required. You can contact on below mentioned connects

>🌐 [Website](https://gist.github.com/siddhantshah1986 "My Website")
&emsp;&emsp; 📮 [Mail Me](mailto:siddhant.shah.1986@gmail.com "siddhant.shah.1986@gmail.com")
&emsp;&emsp; 💹 [UpWork](https://www.upwork.com/fl/geekysid "Upwork")
&emsp;&emsp; 🌇 [Instagram](https://www.instagram.com/geekysid "Instagram")
&emsp;&emsp; 🟢 [WhatsApp](https://api.whatsapp.com/send?phone=+918584852091 "WhatsApp")
