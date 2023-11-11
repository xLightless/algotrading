
# Algotrading

A 'simple' solution for integrating algorithmic and machine learning trading. Ever wanted to manage your capital with just a click of a button? Well now you can, simply become a script kiddie and connect your brokerage details to the bot. Additionally, select your indicators, strategy, and thresholds then go on vacation in about a month! It really is that simple.


![Logo](https://i.imgur.com/OTvXp3a.png)


## Installation

Installing 'algotrading' using git/bash

```
  git clone https://github.com/xLightless/algotrading.git
  cd algotrading
  pip install -r requirements.txt
```
    
## API Reference http://developers.xstore.pro/documentation/2.5.0

#### Login

```http
  POST /api/login

{
	"command": "login",
	"arguments": {
		"userId": "1000",
		"password": "PASSWORD"
	}
}
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `userId` | `int` | **Required**. Your account ID. |
| `password` | `string` | **Required**. Your emails password. |

## Authors

Many thanks to the contributers and authors below:
- [@xlightless](https://www.github.com/xlightless)


## Acknowledgements

 - [@pawelkin](https://github.com/pawelkn/xapi-python/tree/master)
