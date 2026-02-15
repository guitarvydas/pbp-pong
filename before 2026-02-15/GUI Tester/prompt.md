I want a short article simply describing the current architecture based on the following seed text:

- we already have a built-in textual REPL 
	- it's the command line
	- we can type commands in manually, or, we can write scripts and programs that create commands
- we already have a standard GUI - the browser
- the idea is to treat the REPL and GUI as separate, isolated parts
	- the GUI is just a slave, waiting for commands and rendering them
	- the REPL sends commands to the GUI
	- the GUI simply renders
	- we can experiment with the system and get a visual representation of the results without needing to decipher just a stream of numbers
- We _could_ build a more sophisticated REPL
	- for example, a floating slider widget which creates JSON commands and sends them to the GUI directly or through the daemon
- we can test our physics by creating a sophisticated command-line program that sends commands to the GUI, we can watch what happens

---

Let's try a more how-to version, almost academic but not as dry. Include the idea that we already have a transport layer format - JSON.
