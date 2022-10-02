# Find Raspberry Pi's Locally in India
## raspi-instock

## Limited Availability of Raspberry Pi

Availability of Raspberry Pi SBCs was limited in 2021 through 2022, with various online stores having limited stock, or single-unit order restrictions in place. If you have existing projects needing a Raspberry Pi or if you are building a project requiring multiple Raspberry Pis (like a cluster) then you are left looking for Raspberry Pi on various online stores. 

Internationally the [Rpi Locator project](https://rpilocator.com/) tracks availability for US and EU retailers. However there is no support for Indian retailers.

### Supported Retailers

- Robu
- <s>Silverline</s> See https://github.com/salian/raspi-instock/issues/6
- <s>Robocraze</s>

## Using this script

For testing purposes you can run this script from the command line after installing the requirements.

## Setting up a cron job

Ideally you will run this every ten minutes or so, using some sort of scheduler. `cron-task.sh` is a shell script that you can run via your cron or scheduler. It will enable you to launch the virtual environment as well as this script.

## Notifications

This script supports Mac OS X notifications. If you are on your Mac when the item comes in stock, it will notify you as well as launch a webpage showing the item on the retailer's site.

---

## Not a Scalping Tool

This is not a scalping tool. The prices shown will be set by retailers and are most likely going to be higher than the MRP/MSRP prices, so this tool may not be useful if you are looking to resell the SBCs for a profit.
