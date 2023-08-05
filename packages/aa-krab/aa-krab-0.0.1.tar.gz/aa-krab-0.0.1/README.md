# Fittings
![pypi latest version](https://img.shields.io/pypi/v/aa-krab?label=latest)
![python versions](https://img.shields.io/pypi/pyversions/aa-krab)
![django versions](https://img.shields.io/pypi/djversions/aa-krab?label=django)
![license](https://img.shields.io/pypi/l/aa-krab?color=green)

A wormhole krab fleet management and tracking app for [allianceauth](https://gitlab.com/allianceauth/allianceauth).

## Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Screenshots](#screenshots)
- [Installation](#installation)
- [Updating](#updating)
- [Settings](#settings)
- [Permissions](#permissions)


## Overview
This app provides a method of tracking krab fleet member contributions and payouts.

## Key Features
AA-Krab offers the following features:

* Scheduling of krab fleets
* Fleet registration and position selection
* Payout Tracking

## Screenshots

<!---
### Dashboard/Doctrine List
![dashboard/doctrine list](https://i.imgur.com/AUla6oR.png)

### Add Fitting
![add fitting](https://i.imgur.com/09Ht3Zy.png)

### Fitting List
![fitting list](https://i.imgur.com/JTyaot7.png)

### View Fitting
![view fitting](https://i.imgur.com/3H2PgXC.png)

### Add Doctrine
![add doctrine](https://i.imgur.com/WWSJHmb.png)

### View Doctrine
![view doctrine](https://i.imgur.com/9IJN3jt.png)

### Add a Category
![add category](https://i.imgur.com/0ytpF66.png)

### View all Categories
![view all categories](https://i.imgur.com/kRyr34p.png)

### View a Category
![view category](https://i.imgur.com/hs7DDqp.png)

-->

## Installation
### 1. Install App
Install the app into your allianceauth virtual environment via PIP.

```bash
$ pip install aa-krab
```

### 2. Configure AA settings

Configure your AA settings (`local.py`) as follows:

- Add `'fittings',` to `INSTALLED_APPS`

### 3. Finalize Install
Run migrations and copy static files. 

```bash
$ python manage.py migrate
$ python manage.py collectstatic
```

Restart your supervisor tasks.

## Updating
To update your existing installation of AA-Krab first enable your virtual environment.

Then run the following commands from your allianceauth project directory (the one that contains `manage.py`).

```bash
$ pip install -U aa-krab
$ python manage.py migrate
$ python manage.py collectstatic
```

Lastly, restart your supervisor tasks.

*Note: Be sure to follow any version specific update instructions as well. These instructions can be found on the `Tags` page for this repository.*

## Settings
Setting | Default | Description
--- | --- | ---
`No settings` | `-` | There are no settings right now

## Permissions

Permission | Description
-- | --
`aakrab.basic_access` | This permission gives users access to the app.

## Active Developers
* [Belial Morningstar](http://gitlab.com/jtrenaud1s)
-