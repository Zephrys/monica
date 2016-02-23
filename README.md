# monica

![](http://i.imgur.com/mfJa6zi.jpg?1)
:fork_and_knife: monica is a command line chef that brings you tasty food

## Demo
![]()

## Features

- Written in Python
- Uses the Zomato API, so works in 23 countries.
- Works on Linux, Windows and Mac.

## Installation

### 1: [PiP]()

```bash
$ pip install monica
```

### 2: From Source

```bash
$ git clone https://github.com/Zephrys/monica
$ cd monica/
$ python setup.py install
```

## Usage

### Search for a restaurant

```bash
$ monica search Good Chinese Food
```

### Get surprised by something random in your budget

```bash
$ monica surprise
```

### Get restaurants that support a specific cuisine

```bash
$ monica cuisine Indian
```

Or to get a list of cuisines

```bash
$ monica cuisine list
```

### Get a list of restaurants in your budget.

```bash
$ monica budget 500
```

### Get details of a particular restaurant by id

```bash
$ monica restaurant 310543
```

### Get reviews of a restaruant by id

```bash
$ monica reviews 310543
```

### Reconfigure Monica

```bash
$ monica configure
```

### Help

```bash
$ monica --help
```

## Contributing

Use the [issue tracker](https://github.com/Zephrys/monica) to file bugs or push new features.

## License

Open sourced under the **MIT License**