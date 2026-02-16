I include `main.py` and `keyboard_handler.py` below. It appears to accep characters `q`, `w` and `^C`, but doesn't reset the keyboard when done. Why?

```
$ ./@make
refreshing ./pbp
begin
install
init kbd
try
inject
<<>>
ch: /b'q'/
"Info" : "  @4  probe testkbd▹testkbd▹:?key₁: b'q'"
<<>>
ch: /b'w'/
"Info" : "  @7  probe testkbd▹testkbd▹:?key₁: b'w'"
<<>>
ch: /b'\x03'/
finalize
keyboard reset
fini 
     cat: example.sm: No such file or directory
                                               %                                $ 
```
