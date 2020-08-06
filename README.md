# org2html

converts a basic orgfile to html with formatting based on slate-gray bg + aurora-theme.

script is a rough draft, still contains site-specific settings and fixed fonts.

# usage: 
- copy to same dir as orgfile
- open a terminal and type:
```python3 org.py orgfile.org```
# notes:
- sources should be in the same dir as the orgfile, or in a subdirectory.
- pub dir is volatile, it will be cleared every time before copying over files.

# todo
- [X] find most reliable folding mechanism
- [X] translate org folding to html
- [X] use indentation level colors from aurora theme
- [X] style checkboxes to match org
- [X] fix page scaling issues on mobile
- [X] fix font scaling issues on mobile
- [X] write src and example blocks as xmp blocks
- [X] exclude `:noexport:` items & sub-items 
- [X] fix org-table rendering issues on mobile & chrome
- [X] supply org file as an arg
- [ ] grab title info from org file
- [ ] make pub dir if it doesn't exist
- [ ] harvest all linked files, copy to pub
- [ ] clear pub before copying files to it, with confirmation
- [ ] allow fonts to be supplied as args
- [ ] allow fonts to be defined in the org file
- [ ] golf the script and test in an org src block
- [ ] (maybe) use active emacs theme colors
- [ ] (maybe) headline todo and priority formatting (ransack emacs config)
- [ ] (maybe) tag display, filter by tags
- [ ] (maybe) clickable dates to show timeline in split screen

# screenie

![](/org2html_screenie.png?raw=true)
