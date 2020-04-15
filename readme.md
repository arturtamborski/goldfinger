## goldfinger
<br>

It's a multi-processing scraper for `finger(1)`. You can run it like so:
```
python3 goldfinger.py "s{1}" 1 99999999
```

where `"s{1}"` is the username pattern and numbers are used for range.  
The program will use that to go trough every user named `s<something>`  
(in this case `s1`, `s2`, `s3`, ..., `s99999998`, `s99999999`)


It might be bit overengineered, but hey, it was fun to write it like that.  
Output is a json list with dictionaries representing users.


Also, there's some weird bug in finger, it can't print unicode characters  
correctly, so I'm translating it like so.