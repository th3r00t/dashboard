![alt text](https://github.com/th3r00t/dashboard/blob/master/intro.png?raw=true)
# dashboard

## A single file, minimal dependency terminal dashboard

- Reader for HackerNews

## Dependencies
- Python
- Lynx Browser

## Configuration
Configuration file lives at ~/.config/dashboard/config.ini. It will be auto
generated on first run. Currently it has only one configuration option, and
that is wx_loc. Replace Paris with the correct code as per wttr.in

## Usage
Right now the dashboard will respond to Ctrl+N & Ctrl+P for Next & Previous
articles, up & down arrow keys (& Mouse Scroll) for navigting the article 
F1 for Menu (Currently unused), and q for quit.

## TODO

## Done
- [x] Fix out of bounds error when redrawing article list $id{6e608640-5ac1-43a6-972b-ecae726a3d83}
