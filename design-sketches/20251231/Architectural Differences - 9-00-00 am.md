# Architectural Differences - Dec 31, 2025 9:00.00 am

I started going down the let-Claude-build-the-GUI rabbit hole...

Claude built a _whole_ browser-based Pong game, but,,,

I see an architectural difference that I haven't been verbalizing, between PBP thinking and state-of-the-art thinking.

Claude jammed all of the ball and paddle motion logic into the GUI and provided a very milque toast API for changing it, e.g. set ball speed, set paddle size, etc.

In PBP, I think of the GUI as just a GUI, with no programming / dynamic logic inside of it. The GUI is a slave. It gets told where to draw the ball and where to draw each paddle. All of the motion calculation is done elsewhere, outside of the GUI, and not as JS in the HTML of the GUI.

This kind of view makes it extremely simple to implement GUI part. The GUI just draws things. It's akin to thinking about building this using only simple ICs.

In this case, the GUI also grabs keyboard input (gestures like left paddle up/down, right paddle up/down - probably arrow keys, and/or some other QWERTY keystrokes) and sends it back to the controller.

If this were an MVC arrangement - Model, View, Controller - the GUI is View and the Controller, but not Model.

At present, I think that I can put the Model in a ball of code on the command line and ship small messages (JSON?) to the GUI and receive small messages back from the GUI, e.g. for keystrokes, via websockets. This alternate arrangement should make it trivial to convert this game to be multiplayer and distributed. That will probably bring in the question about latency, but, I'm going to ignore that for now. If it's a problem, it will become apparent and I'll have to tweak something to make it perform better. But, for now, let's see where this gets us. I have hope, since, in the past, I already built an experimental REPL using 5 processes and windows talking to a browser via websockets. It worked better than I'd hoped. Playing a game and sending ball movement messages very frequently is at a finer grain and might require optimizing, but, keeping the design chunked in this way will make the design usable on better hardware, and, can be immediately usable on current hardware. And, "optimization" means just moving Parts from "over here" to "over there" instead of tinkering with the internals of the GUI.

We'll see...

