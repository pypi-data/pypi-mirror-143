# ofxstatement-equabankcz
This is a parser for CSV transaction history exported from Equa Bank a.s. (Czech Republic) from within the report in Account History (CSV).

The expected field separator is semicolon (";") and character encoding UTF-8.

It is a plugin for [ofxstatement](https://github.com/kedder/ofxstatement).
I've based this on  the [ofxstatement-airbankcz](https://github.com/milankni/ofxstatement-airbankcz) plugin.

## Usage
```shell
$ ofxstatement convert -t equabankcz movements.csv equa.ofx
```
## Configuration
```shell
$ ofxstatement edit-config
```
And enter e.g. this:
```
[equabankcz]
plugin = equabankcz
currency = CZK
account = Equa Bank CZK
```

## Issues
I've created this to conform mainly to my needs, so it is possible that I haven't
covered all possible transaction types, etc. If you have an improvement, feel free
to open an issue or a pull request.
